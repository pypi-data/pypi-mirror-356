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
"""A schedule rule for mean"""

from typing import List, Union
from tvm import tir
from tvm.target import Target
from ..base import analysis
from .base import RISCVScheduleRule
from .global_avgpool import get_reduction_axis_count


def is_mean(sch, blocks) -> bool:
    if len(blocks) != 2:
        return False

    block0_stmt = sch.get(blocks[0])
    block1_stmt = sch.get(blocks[1])
    return block0_stmt.name_hint == "A_red" and block1_stmt.name_hint == "T_divide"


def get_reduction_index(in_shape, out_shape):
    for i in range(len(out_shape)):
        if in_shape[i] != 1 and out_shape[i] == 1:
            return i
    return len(in_shape) - 1


class Mean(RISCVScheduleRule):
    """A rule for mean."""

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
        if not is_mean(sch, blocks):
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
        red_block = blocks[0]
        reduction_axis_count = get_reduction_axis_count(sch, red_block)

        if reduction_axis_count == 2:
            if in_shape[-1] > 8 and in_shape[-2] > 8:
                return sch
            red_loops = sch.get_loops(red_block)
            l, r0, r1 = red_loops[-3], red_loops[-2], red_loops[-1]
            _, li = sch.split(l, [None, pack2n])
            sch.vectorize(li)
            sch.unroll(r0)
            sch.unroll(r1)

        elif reduction_axis_count == 1:
            reduction_index = get_reduction_index(in_shape, out_shape)
            if reduction_index == len(in_shape) - 1 and in_shape[reduction_index] >= 8:
                red_loop = sch.get_loops(red_block)[-1]
                _, li = sch.split(red_loop, [None, pack2n])
                sch.rfactor(li, -1)
                rf_block = sch.get_block("A_red_rf")
                rf_loops = sch.get_loops(rf_block)
                if in_shape[-1] % pack2n == 0:
                    sch.vectorize(rf_loops[-1])

        div_block = sch.get_block("T_divide")
        div_loops = sch.get_loops(div_block)
        fused = sch.fuse(*div_loops)
        _, fi = sch.split(fused, [None, pack2n])
        sch.vectorize(fi)

        return sch
