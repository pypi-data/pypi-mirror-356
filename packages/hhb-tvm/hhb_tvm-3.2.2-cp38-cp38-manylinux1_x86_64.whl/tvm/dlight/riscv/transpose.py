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
"""A schedule rule for transpose"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from .base import RISCVScheduleRule


def get_transpose_tail(in_perm, out_perm):
    tail = 0
    for i in range(len(in_perm) - 1, -1, -1):
        if in_perm[i] == out_perm[i]:
            tail += 1
        else:
            break
    return tail


class Transpose(RISCVScheduleRule):
    """A rule for transpose."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
        root_block = sch.get_block("root")
        blocks = sch.get_child_blocks(root_block)
        transpose_blocks = []
        for block in blocks:
            if "T_transpose" in sch.get(block).name_hint:
                transpose_blocks.append(block)
        if len(transpose_blocks) == 0:
            return None

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

        in_shape = buffer_values[0].shape
        out_shape = buffer_values[1].shape

        strs = str(sch.mod).splitlines()[-1]
        in_index1 = strs.rfind("[")
        in_index2 = strs.rfind("]")
        in_perm = strs[in_index1 + 1 : in_index2]
        in_perm = in_perm.split(", ")
        out_index1 = strs.find("[")
        out_index2 = strs.find("]")
        out_perm = strs[out_index1 + 1 : out_index2]
        out_perm = out_perm.split(", ")
        transpose_block = transpose_blocks[0]
        loops = sch.get_loops(transpose_block)
        tail = get_transpose_tail(in_perm, out_perm)

        if tail != 0:
            if (
                tail == 1
                or tail == 2
                and tir.ceildiv(in_shape[-2] * in_shape[-1], pack2n)
                >= in_shape[-2] * tir.ceildiv(in_shape[-1], pack2n)
            ):
                # (1) last axis not modified, e.g. [3, 49, 64, 32] -> [3, 64, 49, 32].
                # (2) fuse has no effect on reduing the number of vle.
                # Vectorize directly.
                last_axis = loops[-1]
                _, li = sch.split(last_axis, [None, pack2n])
                sch.vectorize(li)
            else:
                # multi tail axes not modified, e.g. [2, 58, 14, 28] -> [58, 2, 14, 28].
                # Fuse first and then split, vectorize.
                fused = sch.fuse(*loops[len(loops) - tail :])
                _, fi = sch.split(fused, [None, pack2n])
                sch.vectorize(fi)

        else:
            # last axis modified, e.g. [1, 96, 3136] -> [1, 3136, 96].
            # Reorder the loops to utilize vle and vsse.
            transpose_axes = [in_perm.index(out_perm[i]) for i in range(len(out_perm))]
            reorder_axes = [out_perm.index(in_perm[i]) for i in range(len(out_perm))]
            list_loops = [loops[i] for i in reorder_axes]
            sch.reorder(*list_loops)

            if len(transpose_axes) == 4 and transpose_axes == [0, 2, 3, 1]:
                # NCHW -> NHWC
                n, c, h, w = sch.get_loops(transpose_block)
                hw = sch.fuse(h, w)
                if in_shape[-2] * in_shape[-1] > 2048:
                    hw_o, hw_i = sch.split(hw, [None, 2048])
                    sch.reorder(hw_o, c, hw_i)

            if len(transpose_axes) == 5 and transpose_axes == [0, 1, 3, 4, 2]:
                # NCDHW -> NCHWD
                n, c, d, h, w = sch.get_loops(transpose_block)
                hw = sch.fuse(h, w)
                if in_shape[-2] * in_shape[-1] > 2048:
                    hw_o, hw_i = sch.split(hw, [None, 2048])
                    sch.reorder(hw_o, d, hw_i)

            loops = sch.get_loops(transpose_block)
            _, li = sch.split(loops[-1], [None, pack2n])
            sch.vectorize(li)
        return sch
