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
"""A schedule rule for global maxpool"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from tvm.tir import IterVar
from tvm.tir.schedule.schedule import BlockRV
from ..base import analysis
from .base import RISCVScheduleRule
from .global_avgpool import get_reduction_axis_count, get_rf_block, is_nchw


def contain_global_max_block(sch, blocks) -> bool:
    for block in blocks:
        block_stmt = sch.get(block)
        if block_stmt.name_hint == "adaptive_pool_max":
            return True
    return False


def get_max_block(sch, blocks):
    def is_max_block(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "max" in block_stmt.name_hint

    max_blocks = [block for block in blocks if is_max_block(block)]
    if max_blocks and len(max_blocks) != 1:
        return None
    return max_blocks[0]


class Global_MaxPool(RISCVScheduleRule):
    """A rule for global maxpool."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
        root_block = analysis.get_root_block(sch)
        blocks = sch.get_child_blocks(root_block)
        if not contain_global_max_block(sch, blocks):
            return None

        max_block = get_max_block(sch, blocks)
        loops = sch.get_loops(max_block)
        buffer_map = func.buffer_map
        buffer_values = list(buffer_map.values())
        dtype = buffer_values[0].dtype
        vlen = target.vlen
        if dtype == "float32":
            typelen = 32
        elif dtype == "float16":
            typelen = 16
        else:
            typelen = 32
        packn = int(vlen / typelen)
        pack2n = packn * 2
        in_shape = list(buffer_values[0].shape)
        out_shape = list(buffer_values[1].shape)
        reduction_axis_count = get_reduction_axis_count(sch, max_block)

        # schedule for pool1d
        if reduction_axis_count == 1:
            if in_shape[-1] > 64:
                r = loops[-1]
                _, ri = sch.split(r, [None, pack2n])
                sch.rfactor(ri, -1)
                blocks = sch.get_child_blocks(root_block)
                rf_block = get_rf_block(sch, blocks)
                rf_loops = sch.get_loops(rf_block)
                sch.vectorize(rf_loops[-1])
                sch.annotate(rf_loops[-2], "pragma_loop_partition_hint", 1)
                if tir.ceildiv(in_shape[-1], 8) < 100:
                    sch.unroll(rf_loops[-2])
                return sch

            c, r = loops[-3], loops[-1]
            _, ci = sch.split(c, [None, pack2n])
            sch.vectorize(ci)
            sch.unroll(r)

        # schedule for pool2d
        elif reduction_axis_count == 2:
            r0, r1 = loops[-2], loops[-1]
            # layout is NCHW and kernel size is bigger than 8
            if is_nchw(out_shape) and in_shape[-1] > 8 and in_shape[-2] > 8:
                r = sch.fuse(r0, r1)
                _, ri = sch.split(r, [None, pack2n])
                sch.rfactor(ri, -1)
                blocks = sch.get_child_blocks(root_block)
                rf_block = get_rf_block(sch, blocks)
                rf_loops = sch.get_loops(rf_block)
                sch.vectorize(rf_loops[-1])
                sch.annotate(rf_loops[-2], "pragma_loop_partition_hint", 1)
                if tir.ceildiv(in_shape[-1] * in_shape[-2], 8) < 100:
                    sch.unroll(rf_loops[-2])
                return sch

            if not is_nchw(out_shape):
                c = loops[-3]
                sch.reorder(r0, r1, c)  # if layout is NHWC, reorder
            else:
                c = loops[-5]
            _, ci = sch.split(c, [None, pack2n])
            sch.vectorize(ci)

            # if layout is NCHW, unroll
            if is_nchw(out_shape):
                sch.unroll(r0)
                sch.unroll(r1)

        return sch
