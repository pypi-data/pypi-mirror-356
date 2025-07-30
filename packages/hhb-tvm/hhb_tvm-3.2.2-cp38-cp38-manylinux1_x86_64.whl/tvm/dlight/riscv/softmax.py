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
"""A schedule rule for softmax"""

from typing import List, Union
from tvm import tir
from tvm.target import Target
from ..base import normalize_prim_func
from .base import RISCVScheduleRule


class Softmax(RISCVScheduleRule):
    """A rule for softmax."""

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
        if blocks[0].name != "T_softmax_maxelem":
            return None

        in_shape = list(buffer_values[0].shape)
        if in_shape[-1] <= pack2n:
            return None

        max_block = sch.get_block("T_softmax_maxelem")
        max_loops = sch.get_loops(max_block)
        _, max_li = sch.split(max_loops[-1], [None, pack2n])
        sch.rfactor(max_li, -1)
        max_rf_block = sch.get_block("T_softmax_maxelem_rf")
        max_rf_loops = sch.get_loops(max_rf_block)
        sch.vectorize(max_rf_loops[-1])
        sch.annotate(max_rf_loops[-2], "pragma_loop_partition_hint", 1)
        if tir.ceildiv(in_shape[-1], 8) < 100:
            sch.unroll(max_rf_loops[-2])

        delta_block = sch.get_block("T_softmax_delta")
        delta_loops = sch.get_loops(delta_block)
        _, delta_li = sch.split(delta_loops[-1], [None, pack2n])
        sch.vectorize(delta_li)

        # TODO problem: vsetvl redundant
        # exp_block = sch.get_block("T_more_fast_exp")
        # exp_loops = sch.get_loops(exp_block)
        # exp_fused = sch.fuse(*exp_loops)
        # _, exp_fi = sch.split(exp_fused, [None, pack2n])
        # sch.vectorize(exp_fi)

        sum_block = sch.get_block("T_softmax_expsum")
        sum_loops = sch.get_loops(sum_block)
        _, sum_fi = sch.split(sum_loops[-1], [None, pack2n])
        sch.rfactor(sum_fi, -1)
        sum_rf_block = sch.get_block("T_softmax_expsum_rf")
        sum_rf_loops = sch.get_loops(sum_rf_block)
        sch.vectorize(sum_rf_loops[-1])
        sch.annotate(sum_rf_loops[-2], "pragma_loop_partition_hint", 1)
        if tir.ceildiv(in_shape[-1], 8) < 100:
            sch.unroll(sum_rf_loops[-2])

        norm_block = sch.get_block("T_softmax_norm")
        norm_loops = sch.get_loops(norm_block)
        _, norm_li = sch.split(norm_loops[-1], [None, pack2n])
        sch.vectorize(norm_li)

        return sch
