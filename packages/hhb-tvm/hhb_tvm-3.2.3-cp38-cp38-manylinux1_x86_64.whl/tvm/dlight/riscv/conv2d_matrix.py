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
# pylint: disable=missing-docstring, invalid-name
"""A Conv2d schedule rule for RISCV CPU with Matrix unit operators."""
from dataclasses import dataclass

from tvm import tir
from tvm.target import Target
from tvm.tir import IterVar
from tvm.tir.schedule.schedule import BlockRV
from typing import Optional
from ..base import analysis
from .base import RISCVMatrixScheduleRule
from tvm.tir.tensor_intrin.rvm import (
    get_rvm_intrinsics,
    RVM_MACC_FP16_RLEN128_INTRIN,
    RVM_FILL_ZEERO_FP16_RLEN128_INTRIN,
)
from ..base import normalize_prim_func


def get_reduction_blocks(sch, blocks) -> bool:
    # Get the main computation block
    def is_reduction(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        iter_types = {iter_var.iter_type for iter_var in block_stmt.iter_vars}
        return iter_types == {IterVar.CommReduce, IterVar.DataPar}

    def is_spatial(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        iter_types = {iter_var.iter_type for iter_var in block_stmt.iter_vars}
        return iter_types == {IterVar.DataPar}

    # NOTE: We assume there is only one reduction block in the function
    # all blocks are required to be spatial or reduction
    if not all([is_reduction(block) or is_spatial(block) for block in blocks]):
        return None

    reduction_blocks = [block for block in blocks if is_reduction(block)]
    return reduction_blocks


def get_load_st_blocks(sch, blocks) -> bool:
    # Get the load and st blocks
    def is_global(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "global" in block_stmt.name_hint

    def is_spatial(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        iter_types = {iter_var.iter_type for iter_var in block_stmt.iter_vars}
        return iter_types == {IterVar.DataPar}

    global_blocks = [block for block in blocks if is_global(block)]
    for block in global_blocks:
        if not is_spatial(block):
            return None
    if global_blocks:
        if len(global_blocks) != 3:
            return None
    return global_blocks


def get_init_blocks(sch, blocks) -> bool:
    # Get the init block
    def is_init(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "init" in block_stmt.name_hint

    init_blocks = [block for block in blocks if is_init(block)]
    return init_blocks


class Conv2dIm2ColMatrix(RISCVMatrixScheduleRule):
    """The schedule rule for Conv2d computation with matrix instructions"""

    @dataclass
    class Config:

        micro_size_x: int = 8
        micro_size_y: int = 8
        micro_size_k: int = 8
        vector_size: int = 8
        macc_intrinsic = RVM_MACC_FP16_RLEN128_INTRIN
        init_intrinsic = RVM_FILL_ZEERO_FP16_RLEN128_INTRIN

        def __init__(self, rlen, vlen):
            """Initialize the config"""
            if rlen not in [128, 256]:
                raise ValueError("rlen must be one of [128, 256]")
            intrinsics = get_rvm_intrinsics(rlen)
            self.micro_size_x *= int(rlen / 128)
            self.micro_size_y *= int(rlen / 128)
            self.micro_size_k *= int(rlen / 128)
            self.vector_size *= int(rlen / 128)
            self.macc_intrinsic = intrinsics[0]
            self.init_intrinsic = intrinsics[1]

    def get_configs(self, target: Target) -> Config:
        """Get the schedule config for the target"""
        if target.kind.name == "llvm" and target.mcpu == "c907fdvm":
            return Conv2dIm2ColMatrix.Config(target.rlen, target.vlen)
        else:
            raise ValueError("Target not supported")

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Optional[tir.Schedule]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
        root_block = analysis.get_root_block(sch)
        blocks = sch.get_child_blocks(root_block)
        reduction_blocks = get_reduction_blocks(sch, blocks)
        if reduction_blocks is None:
            return None
        config = self.get_configs(target)

        # for main_block in reduction_blocks:
        buffer_map = list(func.buffer_map.values())
        data_shape = list(buffer_map[0].shape)

        main_block = reduction_blocks[0]
        sch.pad_einsum(
            main_block,
            [config.micro_size_x, config.micro_size_y, config.micro_size_k],
        )

        m, n, k = sch.get_loops(main_block)
        i0, i1 = sch.split(m, [None, config.micro_size_x])
        j0, j1 = sch.split(n, [None, config.micro_size_y])
        k0, k1 = sch.split(k, [None, config.micro_size_k])
        sch.reorder(i0, j0, k0, i1, j1, k1)
        sch.decompose_reduction(main_block, k0)

        blocks = sch.get_child_blocks(root_block)
        init_block = get_init_blocks(sch, blocks)
        # load_st_block = get_load_st_blocks(sch, blocks)
        if init_block is None:
            return None

        sch.tensorize(i1, config.macc_intrinsic)
        sch.tensorize(sch.get_loops(init_block[-1])[-2], config.init_intrinsic)

        blocks = sch.get_child_blocks(analysis.get_root_block(sch))

        for block in blocks:
            loops = sch.get_loops(block)
            block_stmt = sch.get(block)
            if block_stmt.name_hint in [
                "data_col",
                "data_padded",
                # "conv",
            ]:
                hw = loops[-1]
                if (
                    data_shape[-1] >= config.vector_size * 2
                    or data_shape[-2] >= config.vector_size * 2
                ):
                    _, li = sch.split(hw, [None, config.vector_size * 2])
                else:
                    _, li = sch.split(hw, [None, config.vector_size])
                sch.vectorize(li)

            if block_stmt.name_hint in [
                "kernel_flat",
                "kernel_flat_pad",
                "data_col_pad",
                # "conv2d_compute_pad",
            ]:
                hw = loops[-1]
                _, li = sch.split(hw, [None, config.vector_size * 2])
                sch.vectorize(li)

        return sch


class Conv2dMatrix(RISCVMatrixScheduleRule):
    """The schedule rule for Conv2d computation with matrix instructions"""

    def is_1x1_conv(self, func) -> bool:
        """Whether the conv is 1x1"""
        kernel_shape = list(func.buffer_map.values())[1].shape
        if len(kernel_shape) != 4:
            return False
        return (kernel_shape[-2].value == 1) and (kernel_shape[-1].value == 1)

    def is_dw_conv(self, sch, block: BlockRV) -> bool:
        """Whether the conv is depth wise"""
        block_stmt = sch.get(block)
        return "DepthwiseConv" in block_stmt.name_hint

    def is_3x3_conv(self, func) -> bool:
        """Whether the conv is 3x3"""
        kernel_shape = list(func.buffer_map.values())[1].shape
        if len(kernel_shape) != 4:
            return False
        return (kernel_shape[-2].value == 3) and (kernel_shape[-1].value == 3)

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Optional[tir.Schedule]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)

        blocks = sch.get_child_blocks(analysis.get_root_block(sch))

        conv2d_blocks = []
        for block in blocks:
            if "conv2d" in sch.get(block).name_hint:
                if self.is_dw_conv(sch, block):
                    continue
                conv2d_blocks.append(block)

        if conv2d_blocks:
            return Conv2dIm2ColMatrix().apply(func, target, _)
        else:
            return None
