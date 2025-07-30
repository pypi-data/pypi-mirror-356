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
"""A schedule rule for layer_norm"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from tvm.tir import IterVar
from tvm.tir.schedule.schedule import BlockRV
from ..base import analysis
from .base import RISCVScheduleRule
from .global_avgpool import get_rf_block


def get_red_temp_block(sch, blocks):
    def is_red_temp_block(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "red_temp" in block_stmt.name_hint

    red_temp_blocks = [block for block in blocks if is_red_temp_block(block)]
    if red_temp_blocks and len(red_temp_blocks) != 1:
        return None
    return red_temp_blocks[0]


def get_norm_block(sch, blocks):
    def is_norm_block(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "layer_norm" in block_stmt.name_hint

    norm_blocks = [block for block in blocks if is_norm_block(block)]
    if norm_blocks and len(norm_blocks) != 1:
        return None
    return norm_blocks[0]


def contain_layer_norm_block(sch, blocks) -> bool:
    for block in blocks:
        block_stmt = sch.get(block)
        if block_stmt.name_hint == "T_layer_norm":
            return True
    return False


class LayerNorm(RISCVScheduleRule):
    """A rule for layer_norm."""

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
        if not contain_layer_norm_block(sch, blocks):
            return None

        red_temp_block = get_red_temp_block(sch, blocks)
        norm_block = get_norm_block(sch, blocks)

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

        # red_temp_loops = sch.get_loops(red_temp_block)
        # _, ri = sch.split(red_temp_loops[-1], [None, pack2n])
        # sch.rfactor(ri, -1)
        # new_blocks = sch.get_child_blocks(root_block)
        # rf_block = get_rf_block(sch, new_blocks)
        # rf_loop = sch.get_loops(rf_block)
        # sch.vectorize(rf_loop[-1])
        # sch.annotate(rf_loop[-2], "pragma_loop_partition_hint", 1)

        norm_loop = sch.get_loops(norm_block)
        fused = sch.fuse(*norm_loop)
        _, fi = sch.split(fused, [None, pack2n])
        sch.vectorize(fi)

        return sch
