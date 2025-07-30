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
"""A schedule rule for sqrt"""
from typing import List, Union
import tvm
from tvm import tir
from tvm.target import Target
from tvm.tir import Block, BufferStore
from tvm.tir.expr import Call
from .base import RISCVScheduleRule


def identify_sqrt_block(block: Block) -> bool:
    if len(block.reads) != 1 or len(block.writes) != 1:
        return False

    if not isinstance(block.body, BufferStore):
        return False
    store = block.body

    if not isinstance(store.value, Call):
        return False
    call = store.value
    op = call.op

    return op == tvm.ir.op.Op.get("tir.sqrt")


class Sqrt(RISCVScheduleRule):
    """A rule for sqrt."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
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
        root = sch.get_block(name="root", func_name="main")
        blocks = sch.get_child_blocks(root)
        if not any([identify_sqrt_block(sch.get(block)) for block in blocks]):
            return None

        sqrt_blocks = []
        for block in blocks:
            if identify_sqrt_block(sch.get(block)):
                sqrt_blocks.append(block)

        for sqrt_block in sqrt_blocks:
            loops = sch.get_loops(sqrt_block)
            fused = sch.fuse(*loops)
            _, li = sch.split(fused, [None, pack2n])
            sch.vectorize(li)

        return sch
