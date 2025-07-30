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
"""A GEMM schedule rule for RISCV CPU with Matrix unit operators."""
import numpy as np
from dataclasses import dataclass

from tvm import tir
from tvm.target import Target
from tvm.tir import IterVar
from tvm.tir.schedule.schedule import BlockRV
from typing import Optional
from ..base import analysis
from .base import RISCVMatrixScheduleRule
from tvm.tir.tensor_intrin.rvm import get_rvm_intrinsics
from tvm.tir.tensor_intrin.rvm import (
    RVM_MACC_FP16_RLEN128_INTRIN,
    RVM_FILL_ZEERO_FP16_RLEN128_INTRIN,
)


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

    # There is only one reduction block
    reduction_blocks = [block for block in blocks if is_reduction(block)]
    if len(reduction_blocks) != 1:
        return None

    return reduction_blocks


def get_padding_blocks(sch, blocks) -> bool:
    # Get the pad block
    def is_padding(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        if "B_pad" == block_stmt.name_hint:
            return False
        return "pad" in block_stmt.name_hint

    def is_data_st(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "matmul_pad" in block_stmt.name_hint

    pad_blocks = [block for block in blocks if is_padding(block)]
    if pad_blocks:
        if is_data_st(pad_blocks[-1]):
            return pad_blocks

    return pad_blocks


def get_init_blocks(sch, blocks) -> bool:
    # Get the init block
    def is_init(block: BlockRV) -> bool:
        block_stmt = sch.get(block)
        return "init" in block_stmt.name_hint

    init_blocks = [block for block in blocks if is_init(block)]
    if init_blocks and len(init_blocks) != 1:
        return None
    return init_blocks


class MatmulMatrix(RISCVMatrixScheduleRule):
    """The schedule rule for matmul-like computation with matrix instructions"""

    @dataclass
    class Config:

        micro_size_x: int = 8
        micro_size_y: int = 8
        micro_size_k: int = 8
        vector_size: int = 8
        macc_intrinsic = RVM_MACC_FP16_RLEN128_INTRIN
        init_intrinsic = RVM_FILL_ZEERO_FP16_RLEN128_INTRIN

        def __init__(self, rlen):
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
            return MatmulMatrix.Config(target.rlen)
        else:
            raise ValueError("Target not supported")

    def need_transpose(self, sch, reduction_block: BlockRV) -> bool:
        """Whether the function needs to be transposed"""
        block_stmt = sch.get(reduction_block)
        k0 = block_stmt.reads[0].region[-1].min
        k1 = block_stmt.reads[1].region[-1].min
        return k0 == k1

    def is_matmul(self, sch, block: BlockRV) -> bool:
        return "matmul" in sch.get(block).name_hint

    def process_input(self, shape, sch, block, index):
        if len(shape) == 2:
            return
        elif len(shape) == 3:
            sch.transform_layout(block, ("read", index), lambda n, i, j: ((n * shape[1] + i), j))
        elif len(shape) == 4:
            sch.transform_layout(
                block,
                ("read", index),
                lambda n, i, j, k: ((n * shape[1] * shape[2] + i * shape[2] + j), k),
            )
        else:
            raise ValueError("Invalid number of loops")
        return

    def process_output(self, shape, sch, block):
        if len(shape) == 2:
            return
        elif len(shape) == 3:
            sch.transform_layout(block, ("write", 0), lambda n, i, j: ((n * shape[1] + i), j))
        elif len(shape) == 4:
            sch.transform_layout(
                block,
                ("write", 0),
                lambda n, i, j, k: ((n * shape[1] * shape[2] + i * shape[2] + j), k),
            )
        else:
            raise ValueError("Invalid number of loops")
        return

    def get_padded_shape(self, sch, block):
        def _get_shape(region, iter_map):
            out = []
            for x in region:
                if isinstance(x.min, tir.expr.IntImm):
                    out.append(1)
                else:
                    out.append(iter_map[x.min])
            return out

        block_stmt = sch.get(block)
        iter_map = {x.var: tir.expr.const(x.dom.extent.value) for x in block_stmt.iter_vars}

        a_shape = _get_shape(block_stmt.reads[0].region, iter_map)
        b_shape = _get_shape(block_stmt.reads[1].region, iter_map)
        c_shape = _get_shape(block_stmt.writes[0].region, iter_map)

        return a_shape, b_shape, c_shape

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

        matmul_blocks = []
        for block in blocks:
            if self.is_matmul(sch, block):
                matmul_blocks.append(block)
        if not matmul_blocks:
            return None

        reduction_blocks = get_reduction_blocks(sch, blocks)
        if reduction_blocks is None:
            return None
        config = self.get_configs(target)
        main_block = reduction_blocks[0]

        buffer_map = list(func.buffer_map.values())
        a_shape = list(buffer_map[0].shape)
        b_shape = list(buffer_map[1].shape)
        c_shape = list(buffer_map[2].shape)
        transpose_b = False
        if self.need_transpose(sch, main_block):
            transpose_b = True

        loops = sch.get_loops(main_block)
        if len(loops) < 3:
            raise ValueError("The number of loops must be greater than 3")
        pad_list = [1 for _ in range(len(loops))]
        pad_list = pad_list[:-3] + [config.micro_size_x, config.micro_size_y, config.micro_size_k]
        sch.pad_einsum(main_block, pad_list)

        a_shape_new, b_shape_new, c_shape_new = self.get_padded_shape(sch, main_block)

        if a_shape_new == a_shape and len(a_shape) != 2:
            sch.cache_read(main_block, 0, "global")
        if b_shape_new == b_shape:
            sch.cache_read(main_block, 1, "global")
        if c_shape_new == c_shape and len(c_shape) != 2:
            sch.cache_write(main_block, 0, "global")

        self.process_input(a_shape_new, sch, main_block, 0)
        self.process_input(b_shape_new, sch, main_block, 1)
        self.process_output(c_shape_new, sch, block)

        tail = config.vector_size

        if "NT" in sch.get(main_block).name_hint or transpose_b:
            sch.transform_layout(
                main_block,
                ("read", 1),
                lambda n, k: (
                    n // tail,
                    k // tail,
                    n % tail,
                    k % tail,
                ),
            )
            dim_k = b_shape_new[-1]
        else:
            sch.transform_layout(
                main_block,
                ("read", 1),
                lambda k, n: (
                    n // tail,
                    k // tail,
                    n % tail,
                    k % tail,
                ),
            )
            dim_k = np.prod(b_shape_new[:-1])

        sch.transform_layout(
            main_block, ("read", 1), lambda i, j, k, l: (i * dim_k + j * tail + k, l)
        )
        blocks = sch.get_child_blocks(root_block)
        b_names = [sch.get(block).name_hint for block in blocks]
        if "B_global" in b_names:
            b_reindex_block = sch.get_block("B_global", "main")
        elif "B_pad" in b_names:
            b_reindex_block = sch.get_block("B_pad", "main")
        elif "B_reindex_reindex" in b_names:
            b_reindex_block = sch.get_block("B_reindex_reindex", "main")
        r_loops = sch.get_loops(b_reindex_block)
        hw = sch.fuse(*r_loops)
        _, li = sch.split(hw, [None, tail])
        sch.vectorize(li)

        i, j, k = sch.get_loops(main_block)[-3:]
        i0, i1 = sch.split(i, [None, config.micro_size_x])
        j0, j1 = sch.split(j, [None, config.micro_size_y])
        k0, k1 = sch.split(k, [None, config.micro_size_k])
        sch.reorder(i0, j0, k0, i1, j1, k1)
        sch.decompose_reduction(main_block, k0)

        blocks = sch.get_child_blocks(analysis.get_root_block(sch))
        init_block = get_init_blocks(sch, blocks)
        if init_block is None:
            return None

        sch.tensorize(i1, config.macc_intrinsic)
        sch.tensorize(sch.get_loops(init_block[0])[-2], config.init_intrinsic)

        blocks = sch.get_child_blocks(analysis.get_root_block(sch))
        pad_blocks = get_padding_blocks(sch, blocks)

        for pad_block in pad_blocks:
            pad_loops = sch.get_loops(pad_block)
            hw = sch.fuse(*pad_loops)
            _, li = sch.split(hw, [None, tail * 2])
            sch.vectorize(li)

        return sch
