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
# pylint: disable=invalid-name,too-many-locals,unused-variable
# pylint: disable=no-value-for-parameter
"""riscv dense operators"""
from __future__ import absolute_import as _abs
import tvm
from tvm import te
from tvm import autotvm
from tvm import auto_scheduler
from tvm.autotvm.task.space import SplitEntity
from tvm.contrib import cblas
from tvm.contrib import mkl
from tvm.contrib import dnnl

from .utils import (
    get_simd_32bit_lanes,
    intrin_add_vv,
    intrin_macc_vf,
    intrin_load,
    intrin_act,
    get_simd_16bit_lanes,
)
from .utils import get_act_mod
from .. import generic, tag, add
from ..utils import traverse_inline, get_const_tuple
from .tensor_intrin import dot_16x1x16_uint8_int8_int32_cascadelake


def _schedule_dense_pack_template(cfg, s, C, O):
    A, packedB = s[C].op.input_tensors

    CC = s.cache_write(C, "global")
    y, x = s[C].op.axis
    (k,) = s[CC].op.reduce_axis

    yt, yo, yi = cfg["tile_y"].apply(s, C, y)
    xt, xo, xi = cfg["tile_x"].apply(s, C, x)
    factor = cfg["tile_x"].size[-1]
    s[C].reorder(xt, yt, yo, xo, yi, xi)
    xyt = s[C].fuse(xt, yt)
    if C == O:
        s[C].parallel(xyt)
    xyo = s[C].fuse(yo, xo)
    s[C].unroll(yi)
    dtype = O.dtype
    if C == O:
        load = intrin_load(factor, dtype)
        s[C].tensorize(xi, load)

    s[CC].compute_at(s[C], xyo)
    y, x = s[CC].op.axis
    ko, ki = cfg["tile_k"].apply(s, CC, k)
    s[CC].reorder(ko, ki, y, x)
    # s[CC].vectorize(x)

    macc = intrin_macc_vf(factor, dtype)
    s[CC].tensorize(x, macc)

    tile_inner = cfg["tile_inner"].size[-1]
    if tile_inner > 1:
        yo, yi = s[CC].split(y, tile_inner)
        s[CC].reorder(ko, yo, ki, yi, x)
        s[CC].unroll(yo)
        s[CC].unroll(ki)
        s[CC].unroll(yi)
    else:
        s[CC].unroll(ki)
        s[CC].unroll(y)

    if C != O:
        y, x = s[O].op.axis
        yt, yo, yi = cfg["tile_y"].apply(s, O, y)
        xt, xo, xi = cfg["tile_x"].apply(s, O, x)
        s[O].reorder(xt, yt, yo, xo, yi, xi)
        xyt = s[O].fuse(xt, yt)
        xyo = s[O].fuse(yo, xo)
        s[C].compute_at(s[O], xyo)
        # s[O].vectorize(xi)
        # s[O].parallel(xyt)
        act_mod = None
        if "elemwise" in s[O].op.tag:
            act_mod = get_act_mod(s[O].op)
        if "add" in str(s[O].op.body[0]) or "add" in str(s[O].op.name):
            my_add = intrin_add_vv(factor, dtype, load_a=False, act_mod=act_mod)
            s[O].tensorize(xi, my_add)
        else:
            my_act = intrin_act(factor, act_mod, dtype)
            s[O].tensorize(xi, my_act)

        s[O].unroll(yi)
    return s


def _schedule_dense_nopack_template(cfg, s, C):
    y, x = s[C].op.axis
    (kk,) = s[C].op.reduce_axis
    yo, yi = cfg["tile_y"].apply(s, C, y)
    xo, xi = cfg["tile_x"].apply(s, C, x)
    s[C].reorder(yo, xo, yi, xi)
    xyo = s[C].fuse(yo, xo)
    s[C].parallel(xyo)
    s[C].unroll(kk)

    (CC,) = s[C].op.input_tensors
    s[CC].compute_at(s[C], xyo)
    z, y, x = s[CC].op.axis
    (k,) = s[CC].op.reduce_axis
    yz = s[CC].fuse(z, y)
    s[CC].reorder(k, yz, x)
    s[CC].unroll(yz)
    s[CC].vectorize(x)
    return s


def _default_dense_pack_config(cfg, M, N, K, dtype):
    # Generate default schedule for dynamic shape.
    if isinstance(M, (tvm.tir.Var, tvm.tir.Any)):
        M = 16
    if isinstance(N, (tvm.tir.Var, tvm.tir.Any)):
        N = 16
    if isinstance(K, (tvm.tir.Var, tvm.tir.Any)):
        K = 16

    if dtype == "float32":
        vec_width = get_simd_32bit_lanes()
    else:
        vec_width = get_simd_16bit_lanes()
    tilex_ii = 1
    for bn in range(vec_width, 0, -1):
        if N % bn == 0:
            tilex_ii = bn
            break
    NN = N // tilex_ii
    tilex_oi = 1
    while NN // tilex_oi > 4:
        if (NN // tilex_oi) % 2 == 1:
            break
        tilex_oi *= 2

    tiley_ii = 8
    while M % tiley_ii != 0:
        tiley_ii //= 2
    MM = M // tiley_ii
    tiley_oi = 1
    while MM // tiley_oi > 4:
        if (MM // tiley_oi) % 2 == 1:
            break
        tiley_oi *= 2

    cfg["tile_y"] = SplitEntity([MM // tiley_oi, tiley_oi, tiley_ii])
    cfg["tile_x"] = SplitEntity([NN // tilex_oi, tilex_oi, tilex_ii])
    cfg["tile_k"] = SplitEntity([K, 1])
    cfg["tile_inner"] = SplitEntity([M // tiley_ii, tiley_ii])


def _default_dense_nopack_config(cfg, M, N, K, dtype):
    # Generate default schedule for dynamic shape.
    if isinstance(M, (tvm.tir.Var, tvm.tir.Any)):
        M = 16
    if isinstance(N, (tvm.tir.Var, tvm.tir.Any)):
        N = 16
    if isinstance(K, (tvm.tir.Var, tvm.tir.Any)):
        K = 16

    if dtype == "float32":
        vec_width = get_simd_32bit_lanes()
    else:
        vec_width = get_simd_16bit_lanes()
    tilek_bn = 1
    for bn in range(vec_width * 2, 0, -1):
        if K % bn == 0:
            tilek_bn = bn
            break
    cfg["tile_k"] = SplitEntity([K // tilek_bn, tilek_bn])
    cfg["tile_x"] = SplitEntity([N, 1])
    cfg["tile_y"] = SplitEntity([1, M])


@autotvm.register_topi_compute("dense_nopack.riscv")
def dense_nopack(cfg, data, weight, bias=None, out_dtype=None):
    """Compute dense without packing"""
    if out_dtype is None:
        out_dtype = data.dtype
    M, K = get_const_tuple(data.shape)
    N, _ = get_const_tuple(weight.shape)
    # create tuning space
    cfg.define_split(
        "tile_y", 32 if isinstance(M, (tvm.tir.Var, tvm.tir.Any)) else M, num_outputs=2
    )
    cfg.define_split(
        "tile_x", 32 if isinstance(N, (tvm.tir.Var, tvm.tir.Any)) else N, num_outputs=2
    )
    cfg.define_split(
        "tile_k", 32 if isinstance(K, (tvm.tir.Var, tvm.tir.Any)) else K, num_outputs=2
    )
    if cfg.is_fallback:
        _default_dense_nopack_config(cfg, M, N, K, out_dtype)

    vec = cfg["tile_k"].size[-1]
    k = te.reduce_axis((0, K // vec), "k")
    CC = te.compute(
        (M, N, vec),
        lambda z, y, x: te.sum(
            data[z, k * vec + x].astype(out_dtype) * weight[y, k * vec + x].astype(out_dtype),
            axis=k,
        ),
    )

    kk = te.reduce_axis((0, vec), "kk")
    C = te.compute((M, N), lambda y, x: te.sum(CC[y, x, kk], axis=kk), tag="dense_nopack")
    if bias is not None:
        C = te.compute((M, N), lambda i, j: C[i, j] + bias[j].astype(out_dtype), tag=tag.BROADCAST)
    return C


@autotvm.register_topi_schedule("dense_nopack.riscv")
def schedule_dense_nopack(cfg, outs):
    """Create the schedule for dense_nopack"""
    s = te.create_schedule([x.op for x in outs])

    def _callback(op):
        if "dense_nopack" in op.tag:
            _schedule_dense_nopack_template(cfg, s, op.output(0))

    traverse_inline(s, outs[0].op, _callback)
    return s


@autotvm.register_topi_compute("dense_pack.riscv")
def dense_pack(cfg, data, weight, bias=None, out_dtype=None):
    """Compute dense with transformed weight."""
    if out_dtype is None:
        out_dtype = data.dtype
    M, K = get_const_tuple(data.shape)  # batch, in_dim
    if len(weight.shape) == 3:
        N, _, packw_bn = get_const_tuple(weight.shape)  # out_dim
        N = N * packw_bn
    else:
        N, _ = get_const_tuple(weight.shape)  # out_dim
    # create tuning space
    cfg.define_split(
        "tile_y", 32 if isinstance(M, (tvm.tir.Var, tvm.tir.Any)) else M, num_outputs=3
    )
    cfg.define_split(
        "tile_x", 32 if isinstance(N, (tvm.tir.Var, tvm.tir.Any)) else N, num_outputs=3
    )
    cfg.define_split(
        "tile_k", 32 if isinstance(K, (tvm.tir.Var, tvm.tir.Any)) else K, num_outputs=2
    )
    cfg.define_split(
        "tile_inner",
        32 if isinstance(M, (tvm.tir.Var, tvm.tir.Any)) else M,
        num_outputs=2,
        filter=lambda y: y.size[-1] <= 16,
    )
    if cfg.is_fallback:
        _default_dense_pack_config(cfg, M, N, K, out_dtype)

    if len(weight.shape) == 2:
        packw_bn = cfg["tile_x"].size[-1]
        packw_shape = (N // packw_bn, K, packw_bn)
        if autotvm.GLOBAL_SCOPE.in_tuning:
            # Directly use modified data layout placeholder.
            packw = tvm.te.placeholder(packw_shape, weight.dtype, name="packed_weight")
        else:
            packw = te.compute(
                packw_shape, lambda z, y, x: weight[z * packw_bn + x, y], name="packed_weight"
            )
    else:
        packw = weight

    idxdiv = tvm.tir.indexdiv
    idxmod = tvm.tir.indexmod
    k = te.reduce_axis((0, K), name="k")
    C = te.compute(
        (M, N),
        lambda y, x: te.sum(
            data[y, k].astype(out_dtype)
            * packw[idxdiv(x, packw_bn), k, idxmod(x, packw_bn)].astype(out_dtype),
            axis=k,
        ),
        tag="dense_pack",
    )
    if bias is not None:
        C = te.compute((M, N), lambda i, j: C[i, j] + bias[j].astype(out_dtype), tag=tag.BROADCAST)
    return C


@autotvm.register_topi_schedule("dense_pack.riscv")
def schedule_dense_pack(cfg, outs):
    """Create the schedule for dense_pack"""
    s = te.create_schedule([x.op for x in outs])

    def _callback(op):
        if "dense_pack" in op.tag:
            _schedule_dense_pack_template(cfg, s, op.output(0), outs[0])

    traverse_inline(s, outs[0].op, _callback)
    return s


def dense_vnni_compute(cfg, X, packed_w, bias=None):
    """Compute for uint8 x int8 -> int32 dense"""
    m, k = X.shape
    n_o, _, n_i, _ = packed_w.shape
    ak = te.reduce_axis((0, k), name="k")

    C = te.compute(
        (m, n_o * n_i),
        lambda i, j: te.sum(
            X[i, ak].astype("int32")
            * packed_w[tvm.tir.indexdiv(j, 16), tvm.tir.indexdiv(ak, 4), j % 16, ak % 4].astype(
                "int32"
            ),
            axis=ak,
        ),
        tag="dense_vnni",
        attrs={"schedule_rule": "meta_schedule.dense_vnni"},
    )

    if bias is not None:
        C = te.compute(C.shape, lambda i, j: C[i, j] + bias[j], tag=tag.BROADCAST)

    a_y, _ = C.op.axis
    cfg.define_split("tile_y", a_y, num_outputs=2)

    return C


def dense_vnni_schedule(cfg, s, C, O, do_parallel=True):
    """Schedule dense compute using VNNI vpdpbusd instruction"""

    # C: The output of GEMM
    # O: The output of the fused op
    def split_y(out):
        default_y_split_factor = 32
        a_y = out.op.axis[-2]

        if cfg.is_fallback:
            return s[out].split(a_y, factor=default_y_split_factor)

        return cfg["tile_y"].apply(s, out, a_y)

    (a_k,) = C.op.reduce_axis

    a_yo, a_yi = split_y(C)
    a_xo, a_xi = s[C].split(C.op.axis[-1], factor=16)
    a_ko, a_ki = s[C].split(a_k, factor=4)

    s[C].reorder(a_yo, a_xo, a_yi, a_ko, a_xi, a_ki)

    pc = dot_16x1x16_uint8_int8_int32_cascadelake()
    s[C].tensorize(a_xi, pc)

    if C == O:
        fused = s[O].fuse(a_yo, a_xo)
    else:
        a_yo, a_yi = split_y(O)
        a_xo, a_xi = s[O].split(O.op.axis[-1], factor=16)

        s[O].reorder(a_yo, a_xo, a_yi, a_xi)
        s[O].vectorize(a_xi)
        s[C].compute_at(s[O], a_yi)

        fused = s[O].fuse(a_yo, a_xo)

    if do_parallel:
        s[O].parallel(fused)

    return s, fused


@autotvm.register_topi_compute("dense_vnni.riscv")
def dense_vnni(cfg, data, weight, bias=None, out_dtype=None):
    """Compute for uint8 x int8 -> int32 dense"""
    if out_dtype is None:
        out_dtype = data.dtype
    assert len(weight.shape) == 4
    assert data.dtype == "uint8" and weight.dtype == "int8"
    _, _, n_inner, k_inner = get_const_tuple(weight.shape)  # out_dim
    assert n_inner == 16 and k_inner == 4
    return dense_vnni_compute(cfg, data, weight, bias)


@autotvm.register_topi_schedule("dense_vnni.riscv")
def schedule_dense_vnni(cfg, outs):
    """Create a schedule for dense_vnni"""
    s = te.create_schedule([x.op for x in outs])

    def _callback(op):
        if "dense_vnni" in op.tag:
            dense_vnni_schedule(cfg, s, op.output(0), outs[0])

    traverse_inline(s, outs[0].op, _callback)
    return s


def matmul_blas_common(cfg, tensor_a, tensor_b, bias, out_dtype, transpose_a, transpose_b, lib):
    """Compute matmul/dense using a BLAS library"""
    M, K = get_const_tuple(tensor_a.shape)
    N, _ = get_const_tuple(tensor_b.shape)
    if isinstance(M, int) and isinstance(K, int) and isinstance(N, int):
        cfg.add_flop(M * K * N * 2)
    if tensor_a.dtype == "uint8" and tensor_b.dtype == "int8" and out_dtype == "int32":
        if not hasattr(lib, "matmul_u8s8s32"):
            raise NotImplementedError(
                f"Matmul/Dense with {lib.__name__} for {tensor_a.dtype} is not supported "
                "(matmulu8s8s32 not imlemented)"
            )
        C = lib.matmul_u8s8s32(tensor_a, tensor_b, transpose_a, transpose_b, dtype=out_dtype)
    elif tensor_a.dtype == "float32" or tensor_a.dtype == "float64":
        C = lib.matmul(tensor_a, tensor_b, transpose_a, transpose_b)
    else:
        raise NotImplementedError(
            f"Matmul/Dense with {lib.__name__} for {tensor_a.dtype} is not supported"
        )

    if bias is not None:
        C = te.compute(C.shape, lambda i, j: C[i, j] + bias[j].astype(out_dtype), tag=tag.BROADCAST)
    return C


@autotvm.register_topi_compute("dense_cblas.riscv")
def dense_cblas(cfg, data, weight, bias=None, out_dtype=None):
    """Compute dense using cblas. This is an alias of matmul_nt operator."""
    return matmul_blas_common(cfg, data, weight, bias, out_dtype, False, True, cblas)


@autotvm.register_topi_schedule("dense_cblas.riscv")
def schedule_dense_cblas(_, outs):
    """Create schedule for dense_cblas. This is an alias of matmul_nt operator."""
    return generic.schedule_extern(outs)


@autotvm.register_topi_compute("dense_mkl.riscv")
def dense_mkl(cfg, data, weight, bias=None, out_dtype=None):
    """Compute dense using mkl. This is an alias of matmul_nt operator."""
    return matmul_blas_common(cfg, data, weight, bias, out_dtype, False, True, mkl)


@autotvm.register_topi_schedule("dense_mkl.riscv")
def schedule_dense_mkl(_, outs):
    """Create schedule for dense_mkl. This is an alias of matmul_nt operator."""
    return generic.schedule_extern(outs)


@autotvm.register_topi_compute("dense_dnnl.riscv")
def dense_dnnl(cfg, data, weight, bias=None, out_dtype=None):
    """Compute dense using dnnl. This is an alias of matmul_nt operator."""
    return matmul_blas_common(cfg, data, weight, bias, out_dtype, False, True, dnnl)


@autotvm.register_topi_schedule("dense_dnnl.riscv")
def schedule_dense_dnnl(_, outs):
    """Create schedule for dense_dnnl. This is an alias of matmul_nt operator."""
    return generic.schedule_extern(outs)


@autotvm.register_topi_compute("matmul_cblas.riscv")
def matmul_cblas(
    cfg, tensor_a, tensor_b, bias=None, out_dtype=None, transpose_a=False, transpose_b=False
):
    """Compute matmul using cblas."""
    return matmul_blas_common(
        cfg, tensor_a, tensor_b, bias, out_dtype, transpose_a, transpose_b, cblas
    )


@autotvm.register_topi_schedule("matmul_cblas.riscv")
def schedule_matmul_cblas(_, outs):
    """Create schedule for matmul_cblas."""
    return generic.schedule_extern(outs)


@autotvm.register_topi_compute("matmul_mkl.riscv")
def matmul_mkl(
    cfg, tensor_a, tensor_b, bias=None, out_dtype=None, transpose_a=False, transpose_b=False
):
    """Compute matmul using mkl."""
    return matmul_blas_common(
        cfg, tensor_a, tensor_b, bias, out_dtype, transpose_a, transpose_b, mkl
    )


@autotvm.register_topi_schedule("matmul_mkl.riscv")
def schedule_matmul_mkl(_, outs):
    """Create schedule for matmul_mkl."""
    return generic.schedule_extern(outs)


@autotvm.register_topi_compute("matmul_dnnl.riscv")
def matmul_dnnl(
    cfg, tensor_a, tensor_b, bias=None, out_dtype=None, transpose_a=False, transpose_b=False
):
    """Compute matmul using dnnl."""
    return matmul_blas_common(
        cfg, tensor_a, tensor_b, bias, out_dtype, transpose_a, transpose_b, dnnl
    )


@autotvm.register_topi_schedule("matmul_dnnl.riscv")
def schedule_matmul_dnnl(_, outs):
    """Create schedule for matmul_dnnl."""
    return generic.schedule_extern(outs)


def matmul(
    tensor_a,
    tensor_b,
    bias=None,
    out_dtype=None,
    transpose_a=False,
    transpose_b=False,
    auto_scheduler_rewritten_layout="",
    meta_schedule_original_shape=None,
):
    """The default implementation of matmul in topi.

    Parameters
    ----------
    tensor_a : tvm.te.Tensor
        2-D with shape [batch, in_dim]

    tensor_b : tvm.te.Tensor
        2-D with shape [out_dim, in_dim]

    bias : Optional[tvm.te.Tensor]
        1-D with shape [out_dim]

    out_dtype : Optional[str]
        The output type. This is used for mixed precision.

    transpose_a : Optional[bool] = False
        Whether the tensor_a is in transposed format.

    transpose_b : Optional[bool] = False
        Whether the tensor_b is in transposed format.

    auto_scheduler_rewritten_layout: Optional[str] = ""
        The layout after auto-scheduler's layout rewrite pass.

    meta_schedule_original_shape: Optional[List[PrimExpr]] = None
        The original shape of the input tensor.

    Returns
    -------
    output : tvm.te.Tensor
        2-D with shape [batch, out_dim]
    """
    # TODO(yixin): support cases for 1-dim input
    # TODO(yixin): adding support and further check for >2-dim input in autotvm template
    assert (
        len(tensor_a.shape) >= 2 and len(tensor_b.shape) >= 2
    ), "1-dim matmul is not supported yet."
    if bias is not None:
        assert len(bias.shape) == 1
    if out_dtype is None:
        out_dtype = tensor_a.dtype
    if transpose_a:
        reduce_dim_a, in_dim = tensor_a.shape[-2:]
    else:
        in_dim, reduce_dim_a = tensor_a.shape[-2:]
    batch_dims_a = tensor_a.shape[:-2]

    if auto_scheduler_rewritten_layout:
        # Infer shape for the rewritten layout
        assert len(tensor_b).shape == 2, "only support 2-dim matmul when using auto-scheduler"
        out_dim, reduce_dim_b = auto_scheduler.get_shape_from_rewritten_layout(
            auto_scheduler_rewritten_layout, ["j", "k"]
        )
        auto_scheduler.remove_index_check(tensor_b)
    elif meta_schedule_original_shape:
        auto_scheduler.rewrite_tensor_shape(tensor_b, meta_schedule_original_shape)
        if transpose_b:
            out_dim, reduce_dim_b = tensor_b.shape[-2:]
        else:
            reduce_dim_b, out_dim = tensor_b.shape[-2:]
    elif transpose_b:
        out_dim, reduce_dim_b = tensor_b.shape[-2:]
    else:
        reduce_dim_b, out_dim = tensor_b.shape[-2:]
    batch_dims_b = tensor_b.shape[:-2]

    if not isinstance(reduce_dim_a, tvm.tir.Var) and not isinstance(reduce_dim_b, tvm.tir.Var):
        assert int(reduce_dim_a) == int(
            reduce_dim_b
        ), f"Reduction dimensions of dense do not match. {reduce_dim_a} vs {reduce_dim_b}."

    result_ndim = max(len(batch_dims_a), len(batch_dims_b))
    batch_dims_a = [1] * (result_ndim - len(batch_dims_a)) + batch_dims_a
    batch_dims_b = [1] * (result_ndim - len(batch_dims_b)) + batch_dims_b

    for idx, (l, r) in enumerate(zip(batch_dims_a, batch_dims_b)):
        if (
            not isinstance(l, tvm.tir.Var)
            and not isinstance(r, tvm.tir.Var)
            and int(l) != 1
            and int(r) != 1
        ):
            assert int(l) == int(r), (
                "Batch dimensions of dense do not match: "
                f"{tensor_a.shape[:-2]} vs {tensor_b.shape[:-2]}."
            )
        if not isinstance(l, tvm.tir.Var) and int(l) == 1:
            batch_dims_a[idx] = batch_dims_b[idx]

    k = te.reduce_axis((0, reduce_dim_a), name="k")

    def compute(*indices):
        batch_indices_a = indices[-len(tensor_a.shape) : -2]
        batch_indices_a = [
            i if isinstance(dim, tvm.tir.Var) or int(dim) != 1 else 0
            for i, dim in zip(batch_indices_a, tensor_a.shape[:-2])
        ]
        batch_indices_b = indices[-len(tensor_b.shape) : -2]
        batch_indices_b = [
            i if isinstance(dim, tvm.tir.Var) or int(dim) != 1 else 0
            for i, dim in zip(batch_indices_b, tensor_b.shape[:-2])
        ]
        i, j = indices[-2:]
        a_indices = (*batch_indices_a, k, i) if transpose_a else (*batch_indices_a, i, k)
        b_indices = (*batch_indices_b, j, k) if transpose_b else (*batch_indices_b, k, j)
        return te.sum(
            tensor_a[a_indices].astype(out_dtype) * tensor_b[b_indices].astype(out_dtype), axis=k
        )

    # compute_name = {
    #     (True, True): "T_matmul_TT",
    #     (True, False): "T_matmul_TN",
    #     (False, True): "T_matmul_NT",
    #     (False, False): "T_matmul_NN",
    # }[(transpose_a, transpose_b)]

    compute_name = "matmul"

    # TODO(jcf94): Remove `dense` when `matmul` is finally ready
    compute_tag = "dense" if (transpose_a, transpose_b) == (False, True) else "matmul"

    mat = te.compute(
        (*batch_dims_a, in_dim, out_dim),
        compute,
        name=compute_name,
        tag=compute_tag,
        attrs={"layout_free_placeholders": [tensor_b]},
    )

    if bias is not None:
        mat = add(mat, bias.astype(out_dtype))

    if auto_scheduler_rewritten_layout:
        mat = auto_scheduler.rewrite_compute_body(mat, auto_scheduler_rewritten_layout)

    return mat
