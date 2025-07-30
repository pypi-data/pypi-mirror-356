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
from .. import TensorIntrin
import tvm


VECTOR_LEN = 128
DTYPE_SHORT_MAP = {
    tvm.DataTypeCode.INT: "i",
    tvm.DataTypeCode.UINT: "u",
    tvm.DataTypeCode.FLOAT: "f",
}
INTRIN2LLVMIR = {}


def register_llvm_code(intrin_name, ll_code_func):
    if intrin_name not in INTRIN2LLVMIR:
        INTRIN2LLVMIR[intrin_name] = ll_code_func
    else:
        raise ValueError(f"{intrin_name} have not been registered llvm code.")


def get_llvm_code(intrin_name):
    llvm_code = None
    if intrin_name not in INTRIN2LLVMIR:
        raise ValueError(f"{intrin_name} have not been registered.")
    func_or_ir = INTRIN2LLVMIR[intrin_name]
    if isinstance(func_or_ir, str):
        # already compiled to llvm ir, just use it
        llvm_code = func_or_ir
    else:
        # need to compile to llvm ir and replace func with generated llvm ir
        llvm_code = func_or_ir()
        INTRIN2LLVMIR[intrin_name] = llvm_code
    return llvm_code


def register_rvv_intrin(intrin_name, intrin_impl):
    assert (
        isinstance(intrin_impl, (list, tuple)) and len(intrin_impl) == 3
    ), "Invalid intrin implemation, should be (desc_func, impl_func, ll_code)"
    desc, impl, ll_code_func = intrin_impl
    TensorIntrin.register(intrin_name, desc, impl)
    register_llvm_code(intrin_name, ll_code_func)


def get_rvv_vsetvl_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vsetvl_e{tvm_dtype.bits}m{lmul}"


def get_rvv_dtype(dtype, lmul):
    return f"v{dtype}m{lmul}_t"


def get_rvv_vle_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vle{tvm_dtype.bits}_v_{DTYPE_SHORT_MAP[tvm_dtype.type_code]}{tvm_dtype.bits}m{lmul}"


def get_rvv_vse_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vse{tvm_dtype.bits}_v_{DTYPE_SHORT_MAP[tvm_dtype.type_code]}{tvm_dtype.bits}m{lmul}"


def get_rvv_fadd_vv_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfadd_vv_f{tvm_dtype.bits}m{lmul}"


def get_rvv_add_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_add_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_add_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0:tile])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = A[vi] + B[vi]

    @T.prim_func
    def rvv_add_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0:tile])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    C.access_ptr("w"),
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *cc, #arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _in1 = #vle#(bb, vl);
            #v_dtype# _sum = #vfadd_vv#(_in0, _in1, vl);
            #vse#(cc, _sum, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfadd_vv#", get_rvv_fadd_vv_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_add_desc, rvv_add_impl, micro_kernel


RVV_ADD_FP32_M1_INTRIN = "rvv_add_fp32_m1"
register_rvv_intrin(RVV_ADD_FP32_M1_INTRIN, get_rvv_add_intrin_impl("float32", 1))

RVV_ADD_FP32_M2_INTRIN = "rvv_add_fp32_m2"
register_rvv_intrin(RVV_ADD_FP32_M2_INTRIN, get_rvv_add_intrin_impl("float32", 2))

RVV_ADD_FP32_M4_INTRIN = "rvv_add_fp32_m4"
register_rvv_intrin(RVV_ADD_FP32_M4_INTRIN, get_rvv_add_intrin_impl("float32", 4))

RVV_ADD_FP32_M8_INTRIN = "rvv_add_fp32_m8"
register_rvv_intrin(RVV_ADD_FP32_M8_INTRIN, get_rvv_add_intrin_impl("float32", 8))


# vfadd_vf
def get_rvv_fadd_vf_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfadd_vf_f{tvm_dtype.bits}m{lmul}"


def get_rvv_add_vf_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_add_vf_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_add_vf_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = A[vi] + B[0]

    @T.prim_func
    def rvv_add_vf_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    C.access_ptr("w"),
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *cc, #arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _sum = #vfadd_vf#(_in0, bb[0], vl);
            #vse#(cc, _sum, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfadd_vf#", get_rvv_fadd_vf_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_add_vf_desc, rvv_add_vf_impl, micro_kernel


RVV_ADD_VF_FP32_M2_INTRIN = "rvv_add_vf_fp32_m2"
register_rvv_intrin(RVV_ADD_VF_FP32_M2_INTRIN, get_rvv_add_vf_intrin_impl("float32", 2))


# vfmul_vf
def get_rvv_fmul_vf_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmul_vf_f{tvm_dtype.bits}m{lmul}"


def get_rvv_mul_vf_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_mul_vf_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_mul_vf_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = A[vi] * B[0]

    @T.prim_func
    def rvv_mul_vf_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    C.access_ptr("w"),
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *cc, #arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _sum = #vfmul_vf#(_in0, bb[0], vl);
            #vse#(cc, _sum, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmul_vf#", get_rvv_fmul_vf_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_mul_vf_desc, rvv_mul_vf_impl, micro_kernel


RVV_MUL_VF_FP32_M2_INTRIN = "rvv_mul_vf_fp32_m2"
register_rvv_intrin(RVV_MUL_VF_FP32_M2_INTRIN, get_rvv_mul_vf_intrin_impl("float32", 2))


# vfsub_vf
def get_rvv_fsub_vf_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfsub_vf_f{tvm_dtype.bits}m{lmul}"


def get_rvv_sub_vf_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_sub_vf_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_sub_vf_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = A[vi] - B[0]

    @T.prim_func
    def rvv_sub_vf_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    C.access_ptr("w"),
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *cc, #arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _sum = #vfsub_vf#(_in0, bb[0], vl);
            #vse#(cc, _sum, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfsub_vf#", get_rvv_fsub_vf_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_sub_vf_desc, rvv_sub_vf_impl, micro_kernel


RVV_SUB_VF_FP32_M2_INTRIN = "rvv_sub_vf_fp32_m2"
register_rvv_intrin(RVV_SUB_VF_FP32_M2_INTRIN, get_rvv_sub_vf_intrin_impl("float32", 2))


# vfdiv_vf
def get_rvv_fdiv_vf_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfdiv_vf_f{tvm_dtype.bits}m{lmul}"


def get_rvv_div_vf_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_div_vf_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_div_vf_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = A[vi] / B[0]

    @T.prim_func
    def rvv_div_vf_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    C.access_ptr("w"),
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *cc, #arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _sum = #vfdiv_vf#(_in0, bb[0], vl);
            #vse#(cc, _sum, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfdiv_vf#", get_rvv_fdiv_vf_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_div_vf_desc, rvv_div_vf_impl, micro_kernel


RVV_DIV_VF_FP32_M2_INTRIN = "rvv_div_vf_fp32_m2"
register_rvv_intrin(RVV_DIV_VF_FP32_M2_INTRIN, get_rvv_div_vf_intrin_impl("float32", 2))


def get_rvv_max_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmax_vf_f{tvm_dtype.bits}m{lmul}"


# relu
def get_rvv_relu_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_relu_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_relu_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile])
            T.writes(B[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    B[vi] = T.max(A[vi], 0)

    @T.prim_func
    def rvv_relu_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile])
            T.writes(B[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("w"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb) {
            #arg_dtype# cc = 0;
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _out = #vfmax_vf#(_in0, cc, vl);
            #vse#(bb, _out, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmax_vf#", get_rvv_max_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_relu_desc, rvv_relu_impl, micro_kernel


RVV_RELU_FP32_M2_INTRIN = "rvv_relu_fp32_m2"
register_rvv_intrin(RVV_RELU_FP32_M2_INTRIN, get_rvv_relu_intrin_impl("float32", 2))


# maxpool
def get_rvv_mv_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmv_v_f_f{tvm_dtype.bits}m{lmul}"


def get_rvv_fill_min_fp32_intrin_impl(lmul):
    dtype = "float32"
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits
    tile = VECTOR_LEN // bit * lmul

    @T.prim_func
    def rvv_fill_min_desc(
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    B[vi] = T.float32(-3.4028234663852886e38)

    @T.prim_func
    def rvv_fill_min_impl(
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile])

            pass

    return rvv_fill_min_desc, rvv_fill_min_impl


RVV_FILL_MIN_FP32_M2_INTRIN = "rvv_fill_min_fp32_m2"
TensorIntrin.register(RVV_FILL_MIN_FP32_M2_INTRIN, *get_rvv_fill_min_fp32_intrin_impl(2))


def get_rvv_vvmax_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmax_vv_f{tvm_dtype.bits}m{lmul}"


def get_rvv_maxpool_3x3_intrin_impl(dtype, lmul, in_dim_width, in_dim_channel):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_maxpool_3x3_{dtype}_m{lmul}_w{in_dim_width}_c{in_dim_channel}"

    @T.prim_func
    def rvv_maxpool_3x3_desc(
        A: T.Buffer((3, 3, tile), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(B[0:tile], A[0:3, 0:3, 0:tile])
            T.writes(B[0:tile])

            for ci, rv0, rv1 in T.grid(tile, 3, 3):
                with T.block(""):
                    v0, v1, v2 = T.axis.remap("SRR", [ci, rv0, rv1])
                    B[v0] = T.max(B[v0], A[v1, v2, v0])

    @T.prim_func
    def rvv_maxpool_3x3_impl(
        A: T.Buffer((3, 3, tile), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(B[0:tile], A[0:3, 0:3, 0:tile])
            T.writes(B[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("w"),
                    T.int32(in_dim_width),
                    T.int32(in_dim_channel),
                    dtype=dtype,
                )
            )

    def micro_kernel():
        cc_code = """
        #include <riscv_vector.h>
        #include <stdio.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb, int in_width_dim, int in_channel_dim) {
            int vl = #vsetvl#;
            #v_dtype# _max = #vfmv#(-3.40282347e+38F, vl);
            for(int h = 0; h < 3; h++) {
                for(int w = 0; w < 3; w++) {
                    const #arg_dtype# *inptr = aa + (h * in_width_dim + w) * in_channel_dim;
                    _max = #vvmax#(_max, #vle#(inptr, vl), vl);
                }
            }
            #vse#(bb, _max, vl);
            return 0;
        }    
        """

        cc_code = cc_code.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{tile}")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vvmax#", get_rvv_vvmax_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmv#", get_rvv_mv_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_maxpool_3x3_desc, rvv_maxpool_3x3_impl, micro_kernel


# reduction max
def get_rvv_redmax_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_redmax_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_redmax_desc(
        A: T.Buffer((1,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.writes(A[0])
            T.reads(B[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("R", [i])
                    A[0] = T.max(A[0], B[vi])

    @T.prim_func
    def rvv_redmax_impl(
        A: T.Buffer((1,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.writes(A[0])
            T.reads(B[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    B.access_ptr("r"),
                    A.access_ptr("w"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            vfloat32m1_t  _min = vfmv_v_f_f32m1(-3.4028234663852886e+38,4);
            #v_dtype# _in0 = #vle#(aa, vl);
            vfloat32m1_t _out = #vfredmax#(_out, _in0,_min, vl);
            #arg_dtype# max = vfmv_f_s_f32m1_f32(_out);
            bb[0] = max;
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfredmax#", get_rvv_redmax_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_redmax_desc, rvv_redmax_impl, micro_kernel


RVV_REDMAX_FP32_M2_INTRIN = "rvv_redmax_fp32_m2"
register_rvv_intrin(RVV_REDMAX_FP32_M2_INTRIN, get_rvv_redmax_intrin_impl("float32", 2))


def get_rvv_sum_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfredusum_vs_f{tvm_dtype.bits}m{lmul}_f32m1"


# sum
def get_rvv_sum_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_sum_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_sum_desc(
        A: T.Buffer((1,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.writes(A[0])
            T.reads(B[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("R", [i])
                    A[0] = A[0] + B[vi]

    @T.prim_func
    def rvv_sum_impl(
        A: T.Buffer((1,), dtype, offset_factor=1),
        B: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.writes(A[0])
            T.reads(B[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    B.access_ptr("r"),
                    A.access_ptr("w"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb) {
            int vl = #vsetvl#;
            vfloat32m1_t  _zero = vfmv_v_f_f32m1(0,4);
            #v_dtype# _in0 = #vle#(aa, vl);
            vfloat32m1_t _out = #vfsum#(_out, _in0,_zero, vl);
            #arg_dtype# sum = vfmv_f_s_f32m1_f32(_out);
            bb[0] = sum;
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfsum#", get_rvv_sum_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_sum_desc, rvv_sum_impl, micro_kernel


RVV_SUM_FP32_M2_INTRIN = "rvv_sum_fp32_m2"
register_rvv_intrin(RVV_SUM_FP32_M2_INTRIN, get_rvv_sum_intrin_impl("float32", 2))


# transpose
def get_rvv_vsse_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vsse{tvm_dtype.bits}_v_{DTYPE_SHORT_MAP[tvm_dtype.type_code]}{tvm_dtype.bits}m{lmul}"


def get_rvv_vsse_intrin_impl(dtype, lmul, last_axis_index, len_axis, stride):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits
    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_vsse_{dtype}_m{lmul}_index{last_axis_index}_stride{stride}"
    negative_index = last_axis_index - len_axis

    if negative_index == -2:

        @T.prim_func
        def rvv_vsse_desc(
            A: T.Buffer((tile,), dtype, offset_factor=1),
            B: T.Buffer((tile, 1), dtype, offset_factor=1),
        ) -> None:
            with T.block("root"):
                T.reads(A[0:tile])
                T.writes(B[0:tile, 1])
                for i in T.serial(0, tile):
                    with T.block("C"):
                        vi = T.axis.remap("S", [i])
                        B[vi, 0] = A[vi]

        @T.prim_func
        def rvv_vsse_impl(
            A: T.Buffer((tile,), dtype, offset_factor=1),
            B: T.Buffer((tile, 1), dtype, offset_factor=1),
        ):
            with T.block("root"):
                T.reads(A[0:tile])
                T.writes(B[0:tile, 1])
                T.evaluate(
                    T.call_extern(
                        micro_kernel_name,
                        A.access_ptr("r"),
                        B.access_ptr("w"),
                        stride,
                        dtype=dtype,
                    )
                )

    elif negative_index == -3:

        @T.prim_func
        def rvv_vsse_desc(
            A: T.Buffer((tile,), dtype, offset_factor=1),
            B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
        ) -> None:
            with T.block("root"):
                T.reads(A[0:tile])
                T.writes(B[0:tile, 1, 1])
                for i in T.serial(0, tile):
                    with T.block("C"):
                        vi = T.axis.remap("S", [i])
                        B[vi, 0, 0] = A[vi]

        @T.prim_func
        def rvv_vsse_impl(
            A: T.Buffer((tile,), dtype, offset_factor=1),
            B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
        ):
            with T.block("root"):
                T.reads(A[0:tile])
                T.writes(B[0:tile, 1, 1])
                T.evaluate(
                    T.call_extern(
                        micro_kernel_name,
                        A.access_ptr("r"),
                        B.access_ptr("w"),
                        stride,
                        dtype=dtype,
                    )
                )

    else:
        raise ValueError(f"only index -2, -3 are supported now.")

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb, int stride) {
            int vl = #vsetvl#;
            #v_dtype# _in = #vle#(aa, vl);
            #vsse#(bb, sizeof(#arg_dtype#) * stride, _in, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{tile}")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vsse#", get_rvv_vsse_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_vsse_desc, rvv_vsse_impl, micro_kernel


# avgpool
def get_rvv_fill_zero_fp32_intrin_impl(channel_num):
    dtype = "float32"
    tile = channel_num

    @T.prim_func
    def rvv_fill_zero_fp32_desc(
        B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile, 0, 0])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    B[vi, 0, 0] = T.float32(0)

    @T.prim_func
    def rvv_fill_zero_fp32_impl(
        B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile, 0, 0])
            pass

    return rvv_fill_zero_fp32_desc, rvv_fill_zero_fp32_impl


def get_rvv_avgpool_update_intrin_impl(kernel_h, kernel_w):
    dtype = "float32"
    lmul_border = [12, 8, 4]

    if kernel_w > lmul_border[0]:
        lmul = 4
    elif kernel_w > lmul_border[1]:
        lmul = 3
    elif kernel_w > lmul_border[2]:
        lmul = 2
    else:
        lmul = 1

    micro_kernel_name = f"rvv_avgpool_update_h{kernel_h}_w{kernel_w}"

    @T.prim_func
    def rvv_avgpool_desc(
        A: T.Buffer((kernel_h, kernel_w), dtype, offset_factor=1),
        B: T.Buffer((1, 1), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(B[0, 0], A[0:kernel_h, 0:kernel_w])
            T.writes(B[0, 0])
            for i, j in T.grid(kernel_h, kernel_w):
                with T.block(""):
                    vi, vj = T.axis.remap("RR", [i, j])
                    B[0, 0] = B[0, 0] + A[vi, vj]

    @T.prim_func
    def rvv_avgpool_impl(
        A: T.Buffer((kernel_h, kernel_w), dtype, offset_factor=1),
        B: T.Buffer((1, 1), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(B[0, 0], A[0:kernel_h, 0:kernel_w])
            T.writes(B[0, 0])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("w"),
                    int(kernel_h),
                    int(kernel_w),
                    dtype=dtype,
                )
            )

    def micro_kernel():
        cc_code = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb, int kernel_h, int kernel_w) {
            int vl = kernel_w;
            #v_dtype# _sum = #vfmv#(0.0f, vl);
            for(int h = 0; h < kernel_h; h++) {
                #v_dtype# _input = #vle#(aa, vl);
                _sum = #vfadd_vv#(_sum, _input, vl);
                aa += vl;
            }
            vfloat32m1_t _zero = vfmv_v_f_f32m1(0, 4);
            vfloat32m1_t _out = #vfsum#(vundefined_f32m1(), _sum, _zero, vl);
            #arg_dtype# res = vfmv_f_s_f32m1_f32(_out);
            // res = res / kernel_h /  kernel_w;
            *bb = res;
            return 0;
        }
        """

        cc_code = cc_code.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmv#", get_rvv_mv_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfsum#", get_rvv_sum_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfadd_vv#", get_rvv_fadd_vv_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_avgpool_desc, rvv_avgpool_impl, micro_kernel


def get_rvv_avg_intrin_impl(lmul, avg_factor):
    dtype = "float32"
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_avg_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_avg_desc(
        A: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
        B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile, 0, 0])
            T.writes(B[0:tile, 0, 0])
            for i in T.serial(0, tile):
                with T.block(""):
                    vi = T.axis.remap("S", [i])
                    B[vi, 0, 0] = A[vi, 0, 0] * T.float32(avg_factor)

    @T.prim_func
    def rvv_avg_impl(
        A: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
        B: T.Buffer((tile, 1, 1), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile, 0, 0])
            T.writes(B[0:tile, 0, 0])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("w"),
                    float(avg_factor),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb, #arg_dtype# avg_factor) {
            int vl = #vsetvl#;
            #v_dtype# in = #vle#(aa, vl);
            #v_dtype# res = #vfmul_vf#(in, avg_factor, vl);
            #vse#(bb, res, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmul_vf#", get_rvv_fmul_vf_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_avg_desc, rvv_avg_impl, micro_kernel


def get_rvv_vfmacc_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmacc_vf_f{tvm_dtype.bits}m{lmul}"


# vfmacc
def get_rvv_vfmacc_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits

    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_vfmacc_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_vfmacc_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = C[vi] + A[vi] * B[0]

    @T.prim_func
    def rvv_vfmacc_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(A[0:tile], B[0])
            T.writes(C[0:tile])

            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    C.access_ptr("rw"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb,#arg_dtype# *cc) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _acc = #vle#(cc, vl);
            _acc = #vfmacc_vf#(_acc, bb[0], _in0, vl);
            #vse#(cc, _acc, vl);
            return 0;
        }
        """

        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmacc_vf#", get_rvv_vfmacc_intrin(dtype, lmul))

        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_vfmacc_desc, rvv_vfmacc_impl, micro_kernel


RVV_VFMACC_FP32_M1_INTRIN = "rvv_vfmacc_fp32_m1"
register_rvv_intrin(RVV_VFMACC_FP32_M1_INTRIN, get_rvv_vfmacc_intrin_impl("float32", 1))


# vfmacc
def get_rvv_vfmacc_boai_intrin_impl(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits
    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_vfmacc_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_vfmacc_desc(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads(C[0:tile], B[0], A[0:tile])
            T.writes(C[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    C[vi] = C[vi] + B[0] * A[vi]

    @T.prim_func
    def rvv_vfmacc_impl(
        A: T.Buffer((tile,), dtype, offset_factor=1),
        B: T.Buffer((1,), dtype, offset_factor=1),
        C: T.Buffer((tile,), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads(C[0:tile], A[0:tile], B[0])
            T.writes(C[0:tile])
            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    A.access_ptr("r"),
                    B.access_ptr("r"),
                    C.access_ptr("rw"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *aa, #arg_dtype# *bb,#arg_dtype# *cc) {
            int vl = #vsetvl#;
            #v_dtype# _in0 = #vle#(aa, vl);
            #v_dtype# _acc = #vle#(cc, vl);
            _acc = #vfmacc_vf#(_acc, bb[0], _in0, vl);
            #vse#(cc, _acc, vl);
            return 0;
        }
        """
        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vle#", get_rvv_vle_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmacc_vf#", get_rvv_vfmacc_intrin(dtype, lmul))
        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_vfmacc_desc, rvv_vfmacc_impl, micro_kernel


RVV_VFMACC_B0AI_FP32_M1_INTRIN = "rvv_vfmacc_b0ai_fp32_m1"
register_rvv_intrin(RVV_VFMACC_B0AI_FP32_M1_INTRIN, get_rvv_vfmacc_boai_intrin_impl("float32", 1))


def get_rvv_vfmv_intrin(dtype, lmul):
    tvm_dtype = tvm.DataType(dtype)
    return f"vfmv_v_f_f{tvm_dtype.bits}m{lmul}"


def get_rvv_fill_zero_1_fp32_intrin_impl(lmul):
    dtype = "float32"
    tvm_dtype = tvm.DataType(dtype)
    bit = tvm_dtype.bits
    tile = VECTOR_LEN // bit * lmul
    micro_kernel_name = f"rvv_fill_zero_{dtype}_m{lmul}"

    @T.prim_func
    def rvv_fill_zero_fp32_desc(
        B: T.Buffer((tile), dtype, offset_factor=1),
    ) -> None:
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile])
            for i in T.serial(0, tile):
                with T.block("C"):
                    vi = T.axis.remap("S", [i])
                    B[vi] = T.float32(0)

    @T.prim_func
    def rvv_fill_zero_fp32_impl(
        B: T.Buffer((tile), dtype, offset_factor=1),
    ):
        with T.block("root"):
            T.reads()
            T.writes(B[0:tile])
            T.evaluate(
                T.call_extern(
                    micro_kernel_name,
                    B.access_ptr("w"),
                    dtype="float32",
                )
            )

    def micro_kernel():
        kernel_template = """
        #include <riscv_vector.h>
        extern "C" int #kernel_name#(#arg_dtype# *bb) {
            int vl = #vsetvl#;
            #v_dtype# _out = #vfmv_vf#(0.0, vl);
            #vse#(bb, _out, vl);
            return 0;
        }
        """
        cc_code = kernel_template.replace("#kernel_name#", micro_kernel_name)
        cc_code = cc_code.replace("#arg_dtype#", f"{dtype}_t")
        cc_code = cc_code.replace("#vsetvl#", f"{get_rvv_vsetvl_intrin(dtype, lmul)}({tile})")
        cc_code = cc_code.replace("#v_dtype#", get_rvv_dtype(dtype, lmul))
        cc_code = cc_code.replace("#vse#", get_rvv_vse_intrin(dtype, lmul))
        cc_code = cc_code.replace("#vfmv_vf#", get_rvv_vfmv_intrin(dtype, lmul))
        from tvm.contrib import clang, utils

        temp = utils.tempdir()
        ll_path = temp.relpath("temp.ll")
        # Create LLVM ir from c source code
        ll_code = clang.create_llvm(
            cc_code, output=ll_path, options=["-mcpu=c920", "-mrvv-v0p10-compatible"]
        )
        return ll_code

    return rvv_fill_zero_fp32_desc, rvv_fill_zero_fp32_impl, micro_kernel


RVV_FILL_ZERO_FP32_1_M1_INTRIN = "rvv_fill_zero_1_fp32"
register_rvv_intrin(RVV_FILL_ZERO_FP32_1_M1_INTRIN, get_rvv_fill_zero_1_fp32_intrin_impl(1))
