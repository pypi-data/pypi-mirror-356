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
"""A schedule rule for relu"""

from typing import List, Union
from tvm import tir
from tvm.target import Target
from ..base import (
    normalize_prim_func,
)
from .base import RISCVScheduleRule


class Relu(RISCVScheduleRule):
    """A rule for elementwise."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
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

        sch = tir.Schedule(func)
        blocks = normalize_prim_func(sch)
        if blocks[0].name != "T_relu":
            return None
        block = blocks[0].block_rv
        block = sch.get_block("T_relu")
        loops = sch.get_loops(block)
        fused = sch.fuse(*loops)
        l0, l1 = sch.split(fused, [None, pack2n])
        sch.vectorize(l1)
        return sch
