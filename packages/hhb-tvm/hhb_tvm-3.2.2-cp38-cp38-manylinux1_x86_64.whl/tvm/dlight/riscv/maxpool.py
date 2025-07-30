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
"""A schedule rule for maxpool"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from ..base import normalize_prim_func
from .base import RISCVScheduleRule


def is_maxpool(sch, blocks) -> bool:
    for block in blocks:
        if sch.get(block.block_rv).name_hint == "pool_max":
            return True
    return False


def get_stride(in_shape, out_shape) -> int:
    in_w = (int)(in_shape[-1])
    out_w = (int)(out_shape[-1])
    return round(in_w / out_w)


class MaxPool(RISCVScheduleRule):
    """A rule for maxpool."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
        blocks = normalize_prim_func(sch)
        if not is_maxpool(sch, blocks):
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
        in_shape = list(buffer_values[0].shape)
        out_shape = list(buffer_values[1].shape)

        target_cpu = target.mcpu
        cpu_vector_1_0_list = ["c907fdvm", "c908v"]
        if target_cpu in cpu_vector_1_0_list or get_stride(in_shape, out_shape) == 1:
            block_max = sch.get_block("pool_max", "main")
            loops = sch.get_loops(block_max)
            w, r0, r1 = loops[-3], loops[-2], loops[-1]
            _, wi = sch.split(w, [None, pack2n])
            sch.vectorize(wi)
            sch.unroll(r0)
            sch.unroll(r1)

        return sch
