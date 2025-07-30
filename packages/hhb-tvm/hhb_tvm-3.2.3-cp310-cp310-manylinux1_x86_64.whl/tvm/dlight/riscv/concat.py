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
"""A schedule rule for concat"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from ..base import analysis
from .base import RISCVScheduleRule


def is_concat_block(sch, blocks) -> bool:
    block_stmt = sch.get(blocks[0])
    return block_stmt.name_hint == "T_concat"


def get_join_axis(shape1, shape2):
    for i in range(len(shape1)):
        if shape1[i] != shape2[i]:
            return i
    return -1


class Concat(RISCVScheduleRule):
    """A rule for concat."""

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
        if not is_concat_block(sch, blocks):
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
        shape1 = list(buffer_values[0].shape)
        for i in range(len(buffer_values)):
            if list(buffer_values[i].shape) != shape1:
                shape2 = list(buffer_values[i].shape)
                break
        join_axis = get_join_axis(shape1, shape2)

        block = blocks[0]
        loops = sch.get_loops(block)
        if join_axis != len(shape1) - 1:
            fused = sch.fuse(*loops[(join_axis + 1) :])
            _, fi = sch.split(fused, [None, pack2n])
            sch.vectorize(fi)
        else:
            _, li = sch.split(loops[-1], [None, 8])
            sch.vectorize(li)

        return sch
