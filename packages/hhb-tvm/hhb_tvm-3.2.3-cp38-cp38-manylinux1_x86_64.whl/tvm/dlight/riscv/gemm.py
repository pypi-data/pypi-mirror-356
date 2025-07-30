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
"""A schedule rule for gemm"""
from dataclasses import dataclass
from typing import List, Union

from tvm import tir
from tvm.target import Target
from tvm.tir.schedule import BlockRV
from ..base import analysis
from .base import RISCVScheduleRule


def get_block_size(m, n, k, block_m, block_n, block_k):
    if m <= block_m and n <= block_n and k < block_k:
        return block_m, block_n, block_k


class Gemm(RISCVScheduleRule):
    """A rule for gemm."""

    @dataclass
    class Config:
        micro_size_m: int = 8
        micro_size_n: int = 8
        vlen: int = 128
        packn: int = 4
        pack2n: int = 8

        def __init__(self, vlen) -> None:
            """Initialize the config"""
            self.vlen = vlen
            self.packn = int(vlen / 32)
            self.pack2n = self.packn * 2
            self.micro_size_n = self.pack2n

    def get_configs(self, target: Target) -> Config:
        return Gemm.Config(target.vlen)

    def is_matmul(self, sch, block: BlockRV) -> bool:
        return "matmul" in sch.get(block).name_hint

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        matmul_blocks = []
        sch = tir.Schedule(func)
        root_block = analysis.get_root_block(sch)
        blocks = sch.get_child_blocks(root_block)

        for block in blocks:
            if self.is_matmul(sch, block):
                matmul_blocks.append(block)
        if not matmul_blocks:
            return None
        config = self.get_configs(target)

        a_shape = list(func.buffer_map.values())[0].shape
        b_shape = list(func.buffer_map.values())[1].shape

        m = a_shape[-2]
        k = a_shape[-1]
        n = b_shape[-1]
        if n < config.packn:
            return sch
        if len(a_shape) == 2 and len(b_shape) == 2:
            if a_shape[-1] != b_shape[-2]:
                # schedule dense here
                return sch
            else:
                try:
                    block = sch.get_block("matmul")
                except:
                    return sch

            if m == 1:
                block = sch.get_block("matmul")
                sch.reindex_cache_read(
                    block,
                    1,
                    "global",
                    lambda i, j, k: (j // config.micro_size_n, k, j % config.micro_size_n),
                )
                i, j, k = sch.get_loops(block)
                n0, n1 = sch.split(j, [None, config.micro_size_n])
                sch.reorder(n0, k, n1)
                sch.vectorize(n1)
                sch.decompose_reduction(block, k)

                block_b = sch.get_block("B_global")
                j, k = sch.get_loops(block_b)
                j0, j1 = sch.split(j, [None, config.micro_size_n])
                sch.vectorize(j1)
                sch.reorder(j0, k, j1)
                return sch
            else:
                block = sch.get_block("matmul")
                sch.reindex_cache_read(
                    block,
                    1,
                    "global",
                    lambda i, j, k: (j // config.micro_size_n, k, j % config.micro_size_n),
                )
                sch.reindex_cache_read(
                    block,
                    0,
                    "global",
                    lambda i, j, k: (i // config.micro_size_m, k, i % config.micro_size_m),
                )
        elif len(a_shape) == 4 and len(b_shape) == 4:
            block = sch.get_block("matmul")
            sch.reindex_cache_read(
                block,
                1,
                "global",
                lambda a, b, i, j, k: (a, b, j // config.micro_size_n, k, j % config.micro_size_n),
            )
            sch.reindex_cache_read(
                block,
                0,
                "global",
                lambda a, b, i, j, k: (a, b, i // config.micro_size_m, k, i % config.micro_size_m),
            )
        elif len(a_shape) == 3 and len(b_shape) == 3:
            block = sch.get_block("matmul")
            if a_shape[0] != 1 and b_shape[0] == 1:
                sch.reindex_cache_read(
                    block,
                    1,
                    "global",
                    lambda a, i, j, k: (j // config.micro_size_n, k, j % config.micro_size_n),
                )
            else:
                sch.reindex_cache_read(
                    block,
                    1,
                    "global",
                    lambda a, i, j, k: (a, j // config.micro_size_n, k, j % config.micro_size_n),
                )
            sch.reindex_cache_read(
                block,
                0,
                "global",
                lambda a, i, j, k: (a, i // config.micro_size_m, k, i % config.micro_size_m),
            )

        elif len(a_shape) == 3 and len(b_shape) == 2:
            block = sch.get_block("matmul")
            sch.reindex_cache_read(
                block,
                1,
                "global",
                lambda a, i, j, k: (j // config.micro_size_n, k, j % config.micro_size_n),
            )
            sch.reindex_cache_read(
                block,
                0,
                "global",
                lambda a, i, j, k: (a, i // config.micro_size_m, k, i % config.micro_size_m),
            )
        block = sch.get_block("matmul")
        loops = sch.get_loops(block)
        i, j, k = loops[-3:]
        m0, m1 = sch.split(i, [None, config.micro_size_m])
        n0, n1 = sch.split(j, [None, config.micro_size_n])
        sch.annotate(m0, "pragma_loop_partition_hint", 1)
        sch.annotate(n0, "pragma_loop_partition_hint", 1)

        if n % config.packn == 0:
            l0, l1 = sch.split(n1, [None, config.packn])
            sch.reorder(m0, n0, k, l0, m1, l1)
            sch.unroll(m1)
            sch.unroll(l0)
            sch.vectorize(l1)
            sch.decompose_reduction(block, k)
        else:
            sch.reorder(m0, n0, k, m1, n1)
            sch.unroll(m1)
            sch.vectorize(n1)
            sch.decompose_reduction(block, k)

        block_a = sch.get_block("A_global")
        loops = sch.get_loops(block_a)
        i, k = loops[-2:]
        k0, k1 = sch.split(k, [None, config.micro_size_n])
        sch.vectorize(k1)
        i0, i1 = sch.split(i, [None, config.micro_size_n])
        sch.unroll(i1)
        sch.reorder(i0, k0, i1, k1)

        block_b = sch.get_block("B_global")
        loops = sch.get_loops(block_b)
        j, k = loops[-2:]
        j0, j1 = sch.split(j, [None, config.micro_size_n])
        sch.vectorize(j1)
        sch.reorder(j0, k, j1)
        return sch
