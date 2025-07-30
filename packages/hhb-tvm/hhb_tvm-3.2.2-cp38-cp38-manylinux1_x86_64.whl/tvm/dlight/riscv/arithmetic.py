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
"""A schedule rule for binary"""

from typing import List, Union

from tvm import tir
from tvm.target import Target
from ..base import normalize_prim_func
from .base import RISCVScheduleRule
from ..base import analysis


class Arithmetic(RISCVScheduleRule):
    """A rule for elementwise."""

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
        arithmetic_block = []

        for block in blocks:
            if sch.get(block).name_hint in ["T_add", "T_multiply", "T_divide", "T_subtract"]:
                arithmetic_block.append(block)
        if not arithmetic_block:
            return None

        block = arithmetic_block[0]

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

        length = len(buffer_values)
        if length == 3:
            a_shape = list(buffer_values[0].shape)
            b_shape = list(buffer_values[1].shape)
            out_shape = list(buffer_values[2].shape)
            if a_shape == b_shape:
                loops = sch.get_loops(block)
                fused = sch.fuse(*loops)
                _, l1 = sch.split(fused, [None, pack2n])
                sch.vectorize(l1)
            else:
                if len(a_shape) != len(b_shape):
                    loops = sch.get_loops(block)
                    l0, l1 = sch.split(loops[-1], [None, pack2n])
                    sch.vectorize(l1)
                else:
                    length = len(out_shape)
                    axis = length - 1
                    while a_shape[axis] != b_shape[axis]:
                        axis = axis - 1
                    loops = sch.get_loops(block)
                    if axis == length - 1:
                        sch.fuse(*loops[0 : len(loops) - 1])
                        _, l1 = sch.split(loops[-1], [None, pack2n])
                        sch.vectorize(l1)
                    else:
                        sch.fuse(*loops[0 : axis + 1])
                        fused = sch.fuse(*loops[axis + 1 : length])
                        _, l1 = sch.split(fused, [None, pack2n])
                        sch.vectorize(l1)
        else:
            loops = sch.get_loops(block)
            fused = sch.fuse(*loops)
            _, l1 = sch.split(fused, [None, pack2n])
            sch.vectorize(l1)
        normalize_prim_func(sch)
        return sch
