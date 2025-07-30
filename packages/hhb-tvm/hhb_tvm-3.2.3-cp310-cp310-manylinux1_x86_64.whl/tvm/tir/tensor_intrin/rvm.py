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
# pylint: disable=invalid-name,missing-function-docstring
"""Intrinsics for RISC-V tensorization."""
from tvm.script import tir as T
from .. import TensorIntrin, IntImm


@T.prim_func
def rvm_macc_8x8_fp16_desc(
    a: T.handle,
    b: T.handle,
    c: T.handle,
) -> None:
    A = T.match_buffer(a, (8, 8), "float16", offset_factor=8)
    B = T.match_buffer(b, (8, 8), "float16", offset_factor=8)
    C = T.match_buffer(c, (8, 8), "float16", offset_factor=8)

    with T.block("root"):
        T.reads(C[0:8, 0:8], A[0:8, 0:8], B[0:8, 0:8])
        T.writes(C[0:8, 0:8])
        for i, j, k in T.grid(8, 8, 8):
            with T.block(""):
                vii, vjj, vkk = T.axis.remap("SSR", [i, j, k])
                T.reads(C[vii, vjj], A[vii, vkk], B[vjj, vkk])
                T.writes(C[vii, vjj])
                C[vii, vjj] = C[vii, vjj] + A[vii, vkk] * B[vjj, vkk]


@T.prim_func
def rvm_macc_8x8_fp16_impl(a: T.handle, b: T.handle, c: T.handle) -> None:
    sa = T.int32()
    sb = T.int32()
    sc = T.int32()
    A = T.match_buffer(a, (8, 8), "float16", offset_factor=8, strides=[sa, 1])
    # for rlen128， b is（2xm，k）
    B = T.match_buffer(b, (8, 8), "float16", offset_factor=8, strides=[sb, 1])
    C = T.match_buffer(c, (8, 8), "float16", offset_factor=8, strides=[sc, 1])
    with T.block("root"):
        T.reads(C[0:8, 0:8], A[0:8, 0:8], B[0:8, 0:8])
        T.writes(C[0:8, 0:8])
        T.evaluate(
            T.riscv_mma(
                8,
                8,
                8,
                A.data,
                sa,
                A.elem_offset,
                B.data,
                sb,
                B.elem_offset,
                C.data,
                sc,
                C.elem_offset,
                dtype="handle",
            )
        )


@T.prim_func
def rvm_fill_8x8_zero_fp16_desc(a: T.handle) -> None:
    C_warp = T.match_buffer(a, [8, 8], dtype="float16")

    with T.block("root"):
        T.reads()
        T.writes(C_warp[0:8, 0:8])
        for i0, i1 in T.grid(8, 8):
            with T.block("C"):
                i, j = T.axis.remap("SS", [i0, i1])
                C_warp[i, j] = T.float16(0)


@T.prim_func
def rvm_fill_8x8_zero_fp16_impl(a: T.handle) -> None:
    sc = T.int32()
    d0 = T.int32()
    C_warp = T.match_buffer(a, (8, 8), "float16", offset_factor=8, strides=[sc, d0])
    with T.block("root"):
        T.reads()
        T.writes(C_warp[0:8, 0:8])
        T.evaluate(
            T.tvm_fill_fragment(
                C_warp.data,
                8,
                8,
                sc,
                C_warp.elem_offset,
                IntImm("int32", 0).astype("float16"),
                dtype="handle",
            )
        )


RVM_MACC_FP16_RLEN128_INTRIN = "rvm_macc_8x8_fp16"
TensorIntrin.register(RVM_MACC_FP16_RLEN128_INTRIN, rvm_macc_8x8_fp16_desc, rvm_macc_8x8_fp16_impl)

RVM_FILL_ZEERO_FP16_RLEN128_INTRIN = "rvm_fill_8x8_zero_fp16"
TensorIntrin.register(
    RVM_FILL_ZEERO_FP16_RLEN128_INTRIN, rvm_fill_8x8_zero_fp16_desc, rvm_fill_8x8_zero_fp16_impl
)


@T.prim_func
def rvm_macc_16x16_fp16_desc(
    a: T.handle,
    b: T.handle,
    c: T.handle,
) -> None:
    A = T.match_buffer(a, (16, 16), "float16", offset_factor=16)
    B = T.match_buffer(b, (16, 16), "float16", offset_factor=16)
    C = T.match_buffer(c, (16, 16), "float16", offset_factor=16)

    with T.block("root"):
        T.reads(C[0:16, 0:16], A[0:16, 0:16], B[0:16, 0:16])
        T.writes(C[0:16, 0:16])
        for i, j, k in T.grid(16, 16, 16):
            with T.block(""):
                vii, vjj, vkk = T.axis.remap("SSR", [i, j, k])
                T.reads(C[vii, vjj], A[vii, vkk], B[vjj, vkk])
                T.writes(C[vii, vjj])
                C[vii, vjj] = C[vii, vjj] + A[vii, vkk] * B[vjj, vkk]


@T.prim_func
def rvm_macc_16x16_fp16_impl(a: T.handle, b: T.handle, c: T.handle) -> None:
    sa = T.int32()
    sb = T.int32()
    sc = T.int32()
    A = T.match_buffer(a, (16, 16), "float16", offset_factor=16, strides=[sa, 1])
    # for rlen128， b is（2xm，k）
    B = T.match_buffer(b, (16, 16), "float16", offset_factor=16, strides=[sb, 1])
    C = T.match_buffer(c, (16, 16), "float16", offset_factor=16, strides=[sc, 1])
    with T.block("root"):
        T.reads(C[0:16, 0:16], A[0:16, 0:16], B[0:16, 0:16])
        T.writes(C[0:16, 0:16])
        T.evaluate(
            T.riscv_mma(
                16,
                16,
                16,
                A.data,
                sa,
                A.elem_offset,
                B.data,
                sb,
                B.elem_offset,
                C.data,
                sc,
                C.elem_offset,
                dtype="handle",
            )
        )


@T.prim_func
def rvm_fill_16x16_zero_fp16_desc(a: T.handle) -> None:
    C_warp = T.match_buffer(a, [16, 16], dtype="float16")

    with T.block("root"):
        T.reads()
        T.writes(C_warp[0:16, 0:16])
        for i0, i1 in T.grid(16, 16):
            with T.block("C"):
                i, j = T.axis.remap("SS", [i0, i1])
                C_warp[i, j] = T.float16(0)


@T.prim_func
def rvm_fill_16x16_zero_fp16_impl(a: T.handle) -> None:
    sc = T.int32()
    d0 = T.int32()
    C_warp = T.match_buffer(a, (16, 16), "float16", offset_factor=16, strides=[sc, d0])
    with T.block("root"):
        T.reads()
        T.writes(C_warp[0:16, 0:16])
        T.evaluate(
            T.tvm_fill_fragment(
                C_warp.data,
                16,
                16,
                sc,
                C_warp.elem_offset,
                IntImm("int32", 0).astype("float16"),
                dtype="handle",
            )
        )


RVM_MACC_FP16_RLEN256_INTRIN = "rvm_macc_16x16_fp16"
TensorIntrin.register(
    RVM_MACC_FP16_RLEN256_INTRIN, rvm_macc_16x16_fp16_desc, rvm_macc_16x16_fp16_impl
)

RVM_FILL_ZEERO_FP16_RLEN256_INTRIN = "rvm_fill_16x16_zero_fp16"
TensorIntrin.register(
    RVM_FILL_ZEERO_FP16_RLEN256_INTRIN, rvm_fill_16x16_zero_fp16_desc, rvm_fill_16x16_zero_fp16_impl
)


def get_rvm_intrinsics(rlen):
    if rlen == 128:
        return [RVM_MACC_FP16_RLEN128_INTRIN, RVM_FILL_ZEERO_FP16_RLEN128_INTRIN]
    elif rlen == 256:
        return [RVM_MACC_FP16_RLEN256_INTRIN, RVM_FILL_ZEERO_FP16_RLEN256_INTRIN]
