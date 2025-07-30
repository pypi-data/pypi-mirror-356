# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""A schedule rule for conv2d"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from .base import RISCVScheduleRule
from ..base import analysis


def contain_conv2d_block(sch, blocks) -> bool:
    conv_name_hints = ["conv2d_nchw", "conv2d_1x1", "conv2d_winograd", "DepthwiseConv2d"]
    for block in blocks:
        block_stmt = sch.get(block)
        if block_stmt.name_hint in conv_name_hints:
            return True
    return False


def is_1x1_conv(weight_shape) -> bool:
    """Whether the conv is 1x1"""
    return len(weight_shape) == 3


def is_winograd(sch, blocks) -> bool:
    """Whether the conv is winograd"""
    for block in blocks:
        block_stmt = sch.get(block)
        if block_stmt.name_hint == "conv2d_winograd":
            return True
    return False


def is_depthwise(sch, blocks) -> bool:
    """Whether the conv is depthwise"""
    for block in blocks:
        block_stmt = sch.get(block)
        if block_stmt.name_hint == "DepthwiseConv2d":
            return True
    return False


def with_padding(IH, IW, OH, OW, packn) -> bool:
    """Whether the conv1x1 contains padding"""
    return ((IH * IW) % packn != 0) or ((OH * OW) % packn != 0)


def loop_tile(sch, m, n, kernel_m, kernel_n):
    m0, m1 = sch.split(m, [None, kernel_m])
    n0, n1 = sch.split(n, [None, kernel_n])
    sch.annotate(m0, "pragma_loop_partition_hint", 1)
    sch.annotate(n0, "pragma_loop_partition_hint", 1)
    return m0, m1, n0, n1


def gemm_m8n2xpackn(sch, conv2d_block, m0, m1, n0, n1, k, packn):
    """apply the schedule when n is divisible by packn"""
    l0, l1 = sch.split(n1, [None, packn])
    sch.reorder(m0, n0, k, m1, l0, l1)
    sch.unroll(m1)
    sch.unroll(l0)
    sch.vectorize(l1)
    sch.decompose_reduction(conv2d_block, k)
    _, ki = sch.split(k, [None, 2])
    sch.unroll(ki)


def gemm_m8npack2n(sch, conv2d_block, m0, m1, n0, n1, k):
    """apply the schedule when n is not divisible by packn"""
    sch.reorder(m0, n0, k, m1, n1)
    sch.unroll(m1)
    sch.vectorize(n1)
    sch.decompose_reduction(conv2d_block, k)
    _, ki = sch.split(k, [None, 2])
    sch.unroll(ki)


def transform_schedule(sch, block, factor):
    """apply the schedule in data transform of winograd"""
    loops = sch.get_loops(block)
    m, n, k = loops[-3:]
    sch.reorder(k, m, n)
    sch.unroll(k)
    sch.unroll(m)
    _, ni = sch.split(n, [None, factor])
    sch.vectorize(ni)


class Conv2d(RISCVScheduleRule):
    """A rule for conv2d."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        # if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
        #     return None

        sch = tir.Schedule(func)
        root_block = analysis.get_root_block(sch)
        blocks = sch.get_child_blocks(root_block)
        if not contain_conv2d_block(sch, blocks):
            return None

        vlen = target.vlen
        packn = int(vlen / 32)
        pack2n = packn * 2

        tile = 4
        kernel_m = 8
        kernel_n = pack2n

        _, IC, IH, IW = list(func.buffer_map.values())[0].shape
        _, _, OH, OW = list(func.buffer_map.values())[2].shape
        weight_shape = list(func.buffer_map.values())[1].shape
        if not is_1x1_conv(weight_shape) and not is_winograd(sch, blocks):
            OC, KIC, KH, KW = weight_shape
            K_area = KH * KW
            M = OC
            N = OH * OW
            K = IC * KH * KW

        if is_1x1_conv(weight_shape):
            if IH == 1 and IW == 1:
                return sch
            block = sch.get_block("conv2d_1x1")
            if with_padding(IH, IW, OH, OW, packn):
                stride = (IH + OH - 1) // OH
                I_pack = packn * stride
                IW_Pad = (IW + I_pack - 1) // I_pack * I_pack
                OW = (IW_Pad - 1) // stride + 1
                sch.transform_block_layout(
                    block, lambda b, oc, oh, ow, ic: (b, oc, (oh * OW + ow), ic)
                )
            else:
                sch.transform_block_layout(
                    block, lambda b, oc, oh, ow, ic: (b, oc, (oh * OW + ow), ic)
                )
            _, m, n, k = sch.get_loops(block)
            m0, m1, n0, n1 = loop_tile(sch, m, n, kernel_m, kernel_n)
            sch.reindex_cache_read(
                block, 0, "global", lambda b, m, n, k: (b, n // kernel_n, k, n % kernel_n)
            )

            if OH * OW % packn != 0:
                gemm_m8npack2n(sch, block, m0, m1, n0, n1, k)
            else:
                gemm_m8n2xpackn(sch, block, m0, m1, n0, n1, k, packn)

            if target.mcpu in ["c908v"] or (IW % kernel_n == 0 and OW % kernel_n == 0):
                try:
                    block_a = sch.get_block("A_global")
                except:
                    block_a = sch.get_block("padded_A_global")
                _, n0, n1, k = sch.get_loops(block_a)
                sch.vectorize(n1)
                sch.reorder(n0, k, n1)

        else:
            if is_winograd(sch, blocks):
                in_blocks = ((OH + tile - 1) // tile) * ((OW + tile - 1) // tile)
                block = sch.get_block("bgemm")
                sch.reindex_cache_read(
                    block,
                    0,
                    "global",
                    lambda a, b, i, j, k: (a, b, j // kernel_n, k, j % kernel_n),
                )
                loops = sch.get_loops(block)
                m, n, k = loops[-3:]
                m0, m1, n0, n1 = loop_tile(sch, m, n, kernel_m, kernel_n)

                # if in_blocks % packn == 0:
                #     gemm_m8n2xpackn(sch, block, m0, m1, n0, n1, k, packn)
                # else:
                #     gemm_m8npack2n(sch, block, m0, m1, n0, n1, k)

                gemm_m8n2xpackn(sch, block, m0, m1, n0, n1, k, packn)

                data_pack0_block = sch.get_block("data_pack0")
                transform_schedule(sch, data_pack0_block, 8)
                data_pack1_block = sch.get_block("data_pack1")
                transform_schedule(sch, data_pack1_block, 8)
                out_pack0_block = sch.get_block("output_pack0")
                transform_schedule(sch, out_pack0_block, packn)
                out_pack1_block = sch.get_block("output_pack1")
                transform_schedule(sch, out_pack1_block, packn)

                data_pack_block = sch.get_block("data_pack")
                eps, nu, ci, p = sch.get_loops(data_pack_block)
                eps_nu = sch.fuse(eps, nu)
                ci_p = sch.fuse(ci, p)
                sch.reorder(ci_p, eps_nu)
                a0, a1 = sch.split(eps_nu, [None, packn])
                sch.vectorize(a1)

                data_pack_block = sch.get_block("data_pack_global")
                eps, nu, p, ci = sch.get_loops(data_pack_block)
                sch.reorder(eps, nu, ci, p)
                p0, p1 = sch.split(p, [None, packn])
                sch.vectorize(p1)

                data_pack_block = sch.get_block("inverse")
                co, p, eps, nu = sch.get_loops(data_pack_block)
                sch.reorder(eps, nu, co, p)
                p0, p1 = sch.split(p, [None, pack2n])
                sch.vectorize(p1)

            elif is_depthwise(sch, blocks):
                stride = (IH + OH - 1) // OH
                if stride > 1:
                    return None
                block = sch.get_block("DepthwiseConv2d")
                b, c, ih, iw, kh, kw = sch.get_loops(block)
                l0, l1 = sch.split(iw, [None, pack2n])
                if IW > 160:
                    k0, k1 = sch.split(l0, [None, 4])
                    sch.unroll(k1)
                else:
                    sch.unroll(l0)
                sch.vectorize(l1)
                sch.unroll(kh)
                sch.unroll(kw)
            else:
                if N <= kernel_n:
                    return None
                block = sch.get_block("conv2d_nchw")
                sch.transform_block_layout(
                    block,
                    lambda b, oc, oh, ow, ic, kh, kw: (
                        b,
                        oc,
                        oh * OW + ow,
                        ic * K_area + kh * KW + kw,
                    ),
                )

                _, m, n, k = sch.get_loops(block)
                m0, m1, n0, n1 = loop_tile(sch, m, n, kernel_m, kernel_n)
                sch.reindex_cache_read(
                    block, 0, "global", lambda b, m, n, k: (b, n // kernel_n, k, n % kernel_n)
                )
                sch.reindex_cache_read(
                    block, 1, "global", lambda b, m, n, k: (m // kernel_m, k, m % kernel_m)
                )
                if (OH * OW) % packn == 0:
                    gemm_m8n2xpackn(sch, block, m0, m1, n0, n1, k, packn)
                else:
                    gemm_m8npack2n(sch, block, m0, m1, n0, n1, k)

                if IW % kernel_n == 0 and OW % kernel_n == 0:
                    block_a = sch.get_block("pad_temp_global")
                    _, n0, n1, k = sch.get_loops(block_a)
                    sch.vectorize(n1)
                    sch.reorder(n0, k, n1)

                block_b = sch.get_block("B_global")
                m0, m1, k = sch.get_loops(block_b)
                k0, k1 = sch.split(k, [None, kernel_n])
                sch.vectorize(k1)
                sch.unroll(m1)
                sch.reorder(m0, k0, m1, k1)

        return sch
