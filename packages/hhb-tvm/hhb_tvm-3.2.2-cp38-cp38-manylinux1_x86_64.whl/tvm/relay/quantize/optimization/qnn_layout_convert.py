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
# pylint: disable=invalid-name, unused-argument, not-callable
"""Convert csinn model layout."""
import logging
import numpy as np

from tvm import relay, IRModule
from tvm.ir import transform
from tvm.relay import function as _function
from tvm.relay.expr import Constant, Tuple
from tvm.relay.transform import function_pass
from tvm.relay.dataflow_pattern import wildcard, is_op, DFPatternCallback, rewrite
from tvm.relay.frontend.common import infer_shape

from ..ir.base import _qnn_attrs, _get_csi_op


logger = logging.getLogger("HHB")

NCHW2NHWC_FUNCS = {}


def nchw2nhwc_attrs_changer(attrs):
    """Change layout attributes"""

    attrs = _qnn_attrs(attrs)
    if "data_layout" in attrs:
        attrs["data_layout"] = "NHWC"
    if "out_layout" in attrs:
        attrs["out_layout"] = "NHWC"
    if "kernel_layout" in attrs:
        attrs["kernel_layout"] = "OHWI"
    if "layout" in attrs:
        attrs["layout"] = "NHWC"
    return attrs


def insert_transpose_call(in_call, axes, q_params, layer_name):
    """Generate transpose op"""
    return relay.qnn.op.csi_transpose(
        in_call, axes=axes, out_dtype="float32", q_params=q_params, layer_name=layer_name
    )


def nchw2nhwc_func_register(func_name):
    """Register func in NCHW2NHWC_FUNCS"""

    def decorator(func):
        NCHW2NHWC_FUNCS[func_name] = func.__name__

        def wrapper(self, call, op_args):
            attrs = nchw2nhwc_attrs_changer(call.attrs)

            # only for 4-dim shape in ops, and dim[0] == 1
            out_shape = infer_shape(call)
            if isinstance(op_args[0], relay.expr.Tuple):
                in_shape = infer_shape(op_args[0]).fields[0].concrete_shape
            else:
                in_shape = infer_shape(op_args[0])
            if len(out_shape) != 4 or len(in_shape) != 4 or out_shape[0] != 1 or in_shape[0] != 1:
                ori_func = _get_csi_op(call.op.name)
                return ori_func(*op_args, **_qnn_attrs(call.attrs))

            new_args = []
            # NCHW to NHWC
            arg_idx = 0
            for arg in op_args:
                if isinstance(arg, (relay.expr.Call, relay.expr.TupleGetItem)):
                    trans_call = insert_transpose_call(
                        arg,
                        axes=(0, 2, 3, 1),
                        q_params=[attrs["q_params"][arg_idx], attrs["q_params"][arg_idx]],
                        layer_name=f"transpose_{arg_idx}_before_{attrs['layer_name']}",
                    )
                    new_args.append(trans_call)
                    arg_idx += 1
                elif isinstance(arg, relay.expr.Tuple):
                    new_tuple = []
                    for a in arg:
                        if isinstance(a, (relay.expr.Call, relay.expr.TupleGetItem)):
                            trans_call = insert_transpose_call(
                                a,
                                axes=(0, 2, 3, 1),
                                q_params=[attrs["q_params"][arg_idx], attrs["q_params"][arg_idx]],
                                layer_name=f"transpose_{arg_idx}_before_{attrs['layer_name']}",
                            )
                            new_tuple.append(trans_call)
                        else:
                            new_tuple.append(a)
                        arg_idx += 1
                    new_args.append(relay.expr.Tuple(new_tuple))
                else:
                    new_args.append(arg)
                    arg_idx += 1

            # NHWC
            new_call = func(self, new_args, attrs)

            # NHWC to NCHW
            trans_call = insert_transpose_call(
                new_call,
                axes=(0, 3, 1, 2),
                q_params=[attrs["q_params"][-1], attrs["q_params"][-1]],
                layer_name=f"transpose_after_{attrs['layer_name']}",
            )

            return trans_call

        return wrapper

    return decorator


def get_var_q_params(mod):
    """Get var node quantization params."""

    class InterHelper(relay.ExprVisitor):
        """Internal helper class"""

        def __init__(self):
            super(InterHelper, self).__init__()
            self.memo_map = {}
            self.var_quant = {}

        def visit_call(self, call):
            _ = [self.visit(arg) for arg in call.args]
            attrs = _qnn_attrs(call.attrs)
            arg_idx = 0
            for arg in call.args:
                if isinstance(arg, relay.expr.Var):
                    self.var_quant[arg] = attrs["q_params"][arg_idx]
                    arg_idx += 1
                elif isinstance(arg, relay.expr.Tuple):
                    for a in arg:
                        if isinstance(a, relay.expr.Var):
                            self.var_quant[a] = attrs["q_params"][arg_idx]
                        arg_idx += 1
                else:
                    arg_idx += 1

    ih = InterHelper()
    ih.visit(mod["main"])
    return ih.var_quant


@function_pass(opt_level=1)
class NCHW2NHWC:
    """Convert layout from NCHW to NHWC"""

    def list_convert(self, src_list):
        if len(src_list) == 4:
            return [src_list[i] for i in [0, 2, 3, 1]]
        return src_list

    def axis_convert(self, axis):
        convert_axis = [0, 3, 1, 2]
        return convert_axis[axis]

    def constant_convert(self, src_constat, is_depthwise=False):
        """Convert constant value layout"""
        if isinstance(src_constat, Constant):
            np_value = src_constat.data.asnumpy()
            value_rank = len(np_value.shape)
            if value_rank == 4:
                if is_depthwise:
                    np_value = np_value.transpose([1, 2, 3, 0])
                else:
                    np_value = np_value.transpose([0, 2, 3, 1])

            return relay.const(np_value, str(np_value.dtype))
        return src_constat

    def diso_convert(self, op_args, attrs, op_name):
        op_args[1] = self.constant_convert(op_args[1])
        func = _get_csi_op("qnn.csi." + op_name)
        return func(*op_args, **attrs)

    def siso_convert(self, op_args, attrs, op_name):
        func = _get_csi_op(op_name)
        return func(*op_args, **attrs)

    @nchw2nhwc_func_register("qnn.csi.conv2d")
    def conv2d(self, op_args, attrs):
        """convert conv2d layout"""
        dshape = infer_shape(op_args[0])
        wshape = infer_shape(op_args[1])
        is_depthwise = False
        if attrs["groups"] != 1 and attrs["groups"] == dshape[3] == wshape[0]:
            is_depthwise = True
        op_args[1] = self.constant_convert(op_args[1], is_depthwise)
        return relay.qnn.op.csi_conv2d(*op_args, **attrs)

    @nchw2nhwc_func_register("qnn.csi.conv2d_relu")
    def conv2d_relu(self, op_args, attrs):
        """convert conv2d_relu layout"""
        dshape = infer_shape(op_args[0])
        wshape = infer_shape(op_args[1])
        is_depthwise = False
        if attrs["groups"] != 1 and attrs["groups"] == dshape[3] == wshape[0]:
            is_depthwise = True
        op_args[1] = self.constant_convert(op_args[1], is_depthwise)
        return relay.qnn.op.csi_conv2d_relu(*op_args, **attrs)

    @nchw2nhwc_func_register("qnn.csi.conv2d_relu6")
    def conv2d_relu6(self, op_args, attrs):
        """convert conv2d_relu layout"""
        dshape = infer_shape(op_args[0])
        wshape = infer_shape(op_args[1])
        is_depthwise = False
        if attrs["groups"] != 1 and attrs["groups"] == dshape[3] == wshape[0]:
            is_depthwise = True
        op_args[1] = self.constant_convert(op_args[1], is_depthwise)
        return relay.qnn.op.csi_conv2d_relu6(*op_args, **attrs)

    # @nchw2nhwc_func_register("qnn.csi.reshape")
    # def reshape(self, op_args, attrs):
    #     """convert reshape layout"""
    #     in_shape_rank = len(infer_shape(op_args[0]))
    #     newshape_rank = len(attrs["newshape"])
    #     if in_shape_rank == 4 and newshape_rank != 4:
    #         axes = [0, 3, 1, 2]
    #         out_dtype = attrs["out_dtype"]
    #         q_params = attrs["q_params"]
    #         layer_name = attrs["layer_name"]
    #         op_args[0] = relay.qnn.op.csi_transpose(
    #             op_args[0], axes, out_dtype, q_params, layer_name
    #         )
    #     attrs["newshape"] = self.list_convert(attrs["newshape"])
    #     return relay.qnn.op.csi_reshape(*op_args, **attrs)

    # @nchw2nhwc_func_register("qnn.csi.depth_to_space")
    # def depth_to_space(self, op_args, attrs):
    #     """convert depth_to_space layout"""
    #     attrs["layout"] = "NHWC"
    #     return relay.qnn.op.csi_depth_to_space(*op_args, **attrs)

    @nchw2nhwc_func_register("qnn.csi.softmax")
    def softmax(self, op_args, attrs):
        """convert softmax layout"""
        in_expr = op_args[0]
        in_shape_rank = len(infer_shape(in_expr))
        if in_shape_rank == 4:
            attrs["axis"] = self.axis_convert(attrs["axis"])
        return relay.qnn.op.csi_softmax(*op_args, **attrs)

    # @nchw2nhwc_func_register("qnn.csi.squeeze")
    # def squeeze(self, op_args, attrs):
    #     """convert squeeze layout"""
    #     in_expr = op_args[0]
    #     in_shape_rank = len(infer_shape(in_expr))
    #     if in_shape_rank == 4:
    #         new_axis = []
    #         for i in attrs["axis"]:
    #             new_axis.append(self.axis_convert(int(i)))
    #         attrs["axis"] = new_axis
    #     return relay.qnn.op.csi_squeeze(*op_args, **attrs)

    # DISO
    @nchw2nhwc_func_register("qnn.csi.subtract")
    def subtract(self, op_args, attrs):
        """convert subtract layout"""
        return self.diso_convert(op_args, attrs, "subtract")

    @nchw2nhwc_func_register("qnn.csi.mul")
    def mul(self, op_args, attrs):
        """convert mul layout"""
        return self.diso_convert(op_args, attrs, "mul")

    @nchw2nhwc_func_register("qnn.csi.add")
    def add(self, op_args, attrs):
        """convert add layout"""
        return self.diso_convert(op_args, attrs, "add")

    @nchw2nhwc_func_register("qnn.csi.div")
    def div(self, op_args, attrs):
        """convert div layout"""
        return self.diso_convert(op_args, attrs, "div")

    @nchw2nhwc_func_register("qnn.csi.sigmoid")
    def sigmoid(self, op_args, attrs):
        """convert sigmoid layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.sigmoid")

    @nchw2nhwc_func_register("qnn.csi.erf")
    def erf(self, op_args, attrs):
        """convert erf layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.erf")

    @nchw2nhwc_func_register("qnn.csi.relu")
    def relu(self, op_args, attrs):
        """convert relu layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.relu")

    @nchw2nhwc_func_register("qnn.csi.relu6")
    def relu6(self, op_args, attrs):
        """convert relu6 layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.relu6")

    @nchw2nhwc_func_register("qnn.csi.leaky_relu")
    def leaky_relu(self, op_args, attrs):
        """convert leaky_relu layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.leaky_relu")

    @nchw2nhwc_func_register("qnn.csi.avgpool2d")
    def avgpool2d(self, op_args, attrs):
        """convert avgpool2d layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.avgpool2d")

    @nchw2nhwc_func_register("qnn.csi.maxpool2d")
    def maxpool2d(self, op_args, attrs):
        """convert maxpool2d layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.maxpool2d")

    @nchw2nhwc_func_register("qnn.csi.global_avgpool2d")
    def global_avgpool2d(self, op_args, attrs):
        """convert global_avgpool2d layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.global_avgpool2d")

    @nchw2nhwc_func_register("qnn.csi.global_maxpool2d")
    def global_maxpool2d(self, op_args, attrs):
        """convert global_maxpool2d layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.global_maxpool2d")

    @nchw2nhwc_func_register("qnn.csi.lrn")
    def lrn(self, op_args, attrs):
        """convert lrn layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.lrn")

    @nchw2nhwc_func_register("qnn.csi.upsampling")
    def upsampling(self, op_args, attrs):
        """convert upsampling layout"""
        return self.siso_convert(op_args, attrs, "qnn.csi.upsampling")

    # @nchw2nhwc_func_register("qnn.csi.minimum")
    # def minimum(self, op_args, attrs):
    #     """convert minimum layout"""
    #     return self.diso_convert(op_args, attrs, "minimum")

    # @nchw2nhwc_func_register("qnn.csi.split")
    # def split(self, op_args, attrs):
    #     """convert split layout"""
    #     in_rank = len(infer_shape(op_args[0]))
    #     if in_rank == 4:
    #         attrs["axis"] = self.axis_convert(attrs["axis"])
    #     return relay.qnn.op.csi_split(op_args[0], **attrs)

    @nchw2nhwc_func_register("qnn.csi.concatenate")
    def concatenate(self, op_args, attrs):
        """convert concatenate layout"""

        in_rank = len(infer_shape(op_args[0].fields[0]))
        new_args = []
        for arg in op_args[0]:
            new_args.append(self.constant_convert(arg))
        if in_rank == 4:
            attrs["axis"] = self.axis_convert(attrs["axis"])
        return relay.qnn.op.csi_concatenate(Tuple(new_args), **attrs)

    # @nchw2nhwc_func_register("qnn.csi.mean")
    # def mean(self, op_args, attrs):
    #     """convert mean layout"""
    #     in_rank = len(infer_shape(op_args[0]))
    #     old_axis = attrs["axis"]
    #     map(lambda x: x + in_rank if x < 0 else x, old_axis)
    #     if in_rank == 4:
    #         new_axis = []
    #         for a in old_axis:
    #             new_axis.append(self.axis_convert(a))
    #         attrs["axis"] = new_axis
    #     return relay.qnn.op.csi_mean(op_args[0], **attrs)

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)
        nchw_nhwc = self

        class NCHW2NHWCMutator(relay.ExprMutator):
            """convert layout from nchw to nhwc"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]
                if call.op.name in NCHW2NHWC_FUNCS:
                    func = getattr(nchw_nhwc, NCHW2NHWC_FUNCS[call.op.name])
                    new_call = func(call=call, op_args=op_args)
                else:
                    # attrs = nchw2nhwc_attrs_changer(call.attrs)
                    func = _get_csi_op(call.op.name)
                    new_call = func(*op_args, **_qnn_attrs(call.attrs))
                return new_call

            def visit_var(self, var):
                shape = list(var.checked_type.concrete_shape)
                new_shape = nchw_nhwc.list_convert(shape)
                dtype = var.checked_type.dtype
                name = var.name_hint
                # NHWC
                new_var = relay.var(name, shape=new_shape, dtype=dtype)
                return new_var

            # def visit_function(self, fn):
            #     new_params = [self.visit(x) for x in fn.params]
            #     new_body = self.visit(fn.body)
            #     return _function.Function(list(new_params), new_body)

        return NCHW2NHWCMutator().visit(func)


ALIGN_FUNCS = {}


def align_func_register(func_name):
    """Register func in ALIGN_FUNCS"""

    def decorator(func):
        ALIGN_FUNCS[func_name] = func.__name__

        def wrapper(self, call, op_args, old_shape):
            attrs = _qnn_attrs(call.attrs)
            return func(self, op_args, attrs, old_shape)

        return wrapper

    return decorator


@function_pass(opt_level=1)
class ShapeAlign:
    """weight shape alignment"""

    def __init__(self, align):
        self.align = align

    def fill_tensor(self, src_data, shape, axis):
        fill_data = np.zeros(shape).astype(np.float32)
        return np.concatenate([src_data, fill_data], axis=axis)

    def revert_shape(self, data, length, q_param, l_name, dtype, axis=1):
        """revert shape to origin"""
        index_expr = relay.const(list(range(length)))
        index_params = [q_param] * 3
        layer_name = l_name + "_take"
        ret = relay.qnn.op.csi_take(
            data,
            index_expr,
            axis=axis,
            out_dtype=dtype,
            q_params=index_params,
            mode="clip",
            layer_name=layer_name,
        )
        return ret

    def constant_convert(self, weight, bias, is_depthwise=False, need_fill=True):
        """Convert constant value layout"""
        np_weight = weight.data.asnumpy()
        np_bias = bias.data.asnumpy()
        fill_bias = np.prod(np_bias.shape) > 1
        k_o, k_i, k_h, k_w = np_weight.shape

        if is_depthwise:
            if need_fill:
                np_weight = self.fill_tensor(np_weight, [need_fill, k_i, k_h, k_w], 0)
                if fill_bias:
                    np_bias = self.fill_tensor(np_bias, [need_fill], 0)
        else:
            o_fill = self.align - k_o % self.align if k_o % self.align != 0 else 0

            if o_fill:
                np_weight = self.fill_tensor(np_weight, [o_fill, k_i, k_h, k_w], 0)
                if fill_bias:
                    np_bias = self.fill_tensor(np_bias, [o_fill], 0)

            if need_fill:
                shape = list(np_weight.shape)
                shape[1] = need_fill
                np_weight = self.fill_tensor(np_weight, shape, 1)
                if fill_bias:
                    np_bias = self.fill_tensor(np_bias, [need_fill], 0)

        new_weight = relay.const(np_weight, str(np_weight.dtype))
        new_bias = relay.const(np_bias, str(np_bias.dtype))
        return new_weight, new_bias

    @align_func_register("qnn.csi.conv2d")
    def conv2d(self, op_args, attrs, old_shape):
        """convert conv2d weight layout"""
        dshape = infer_shape(op_args[0])
        wshape = infer_shape(op_args[1])
        is_depthwise = False
        if attrs["groups"] != 1 and attrs["groups"] == old_shape[1] == wshape[0]:
            is_depthwise = True

        need_fill = dshape[1] - old_shape[1]

        if attrs["groups"] > 1 and not is_depthwise:
            if need_fill:
                op_args[0] = self.revert_shape(
                    op_args[0],
                    old_shape[1],
                    attrs["q_params"][0],
                    attrs["layer_name"],
                    attrs["out_dtype"],
                )
            logger.debug(
                "aligned %s shape: in_shape %s, w_shape: %s",
                attrs["layer_name"],
                dshape,
                wshape,
            )

            new_call = relay.qnn.op.csi_conv2d(*op_args, **attrs)
            return new_call

        op_args[1:] = self.constant_convert(op_args[1], op_args[2], is_depthwise, need_fill)
        attrs["channels"] = infer_shape(op_args[1])[0]
        if is_depthwise:
            attrs["groups"] = attrs["channels"]
        new_call = relay.qnn.op.csi_conv2d(*op_args, **attrs)
        logger.debug(
            "aligned %s shape: in_shape %s, w_shape: %s",
            attrs["layer_name"],
            dshape,
            op_args[1].data.asnumpy().shape,
        )

        return new_call

    @align_func_register("qnn.csi.softmax")
    def softmax(self, op_args, attrs, old_shape):
        """convert softmax layout"""
        dshape = infer_shape(op_args[0])
        if dshape != old_shape:
            op_args[0] = self.revert_shape(
                op_args[0],
                old_shape[1],
                attrs["q_params"][0],
                attrs["layer_name"],
                attrs["out_dtype"],
            )

        return relay.qnn.op.csi_softmax(*op_args, **attrs)

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)
        shape_align = self

        class ShapeAlignMutator(relay.ExprMutator):
            """weight shape alignment"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]
                if call.op.name in ALIGN_FUNCS:
                    func = getattr(shape_align, ALIGN_FUNCS[call.op.name])
                    old_shape = infer_shape(call.args[0])

                    new_call = func(call=call, op_args=op_args, old_shape=old_shape)
                else:
                    attrs = _qnn_attrs(call.attrs)
                    func = _get_csi_op(call.op.name)
                    new_call = func(*op_args, **attrs)

                return new_call

            def visit_function(self, fn):
                new_params = [self.visit(x) for x in fn.params]
                new_body = self.visit(fn.body)
                return _function.Function(list(new_params), new_body)

        return ShapeAlignMutator().visit(func)


@function_pass(opt_level=1)
class FuseTRDense:
    r"""
      Input
        |              Input
    Transpose            |
        |       -->   Reshape
     Reshape             |
        |              Dense
      Dense

    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            """patten and convert op"""

            def __init__(self):
                super(MyCallback, self).__init__()
                self.input = wildcard()
                # transpose
                self.t = is_op("qnn.csi.transpose")(self.input)
                # reshape
                self.r = is_op("qnn.csi.reshape")(self.t)
                # dense
                self.weight = wildcard()
                self.b = wildcard()
                self.dense = is_op("qnn.csi.dense")(self.r, self.weight, self.b)
                self.pattern = self.dense

            def callback(self, pre, post, node_map):
                """taget op"""

                in_node = node_map[self.input][0]
                weight = node_map[self.weight][0].data.numpy()
                bias = node_map[self.b][0]

                in_shape = infer_shape(node_map[self.t][0])
                reshape_attr = _qnn_attrs(node_map[self.r][0].attrs)
                dense_attr = _qnn_attrs(node_map[self.dense][0].attrs)

                # check
                transpose_attr = _qnn_attrs(node_map[self.t][0].attrs)
                trans_axes = transpose_attr["axes"]
                if trans_axes != [0, 3, 1, 2]:
                    raise Exception("dense fuse error!")

                w_shape = weight.shape
                new_weight = weight.reshape([-1, *in_shape])
                # to nhwc
                new_weight = new_weight.transpose([0, 1, 3, 4, 2])
                # to dense
                new_weight = new_weight.reshape(w_shape)

                new_reshape = relay.qnn.op.csi_reshape(in_node, **reshape_attr)
                new_node = relay.qnn.op.csi_dense(
                    new_reshape, relay.const(new_weight), bias, **dense_attr
                )

                return new_node

        out = rewrite(MyCallback(), mod["main"].body)
        res = IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class RemoveTranspose:
    """Remove useless transpose.

    For example,
    input -> transpoe(0, 3, 1, 2) -> transpose(0, 2, 3, 1) -> output

    convert to:
    input -> output

    """

    def detect_transpose_struct(self, call):
        """Detect whether transpose(0, 3, 1, 2) -> transpose(0, 2, 3, 1)"""
        is_struct = False
        if call.op.name == "qnn.csi.transpose":
            trans1_attrs = _qnn_attrs(call.attrs)
            if tuple(trans1_attrs["axes"]) == (0, 2, 3, 1):
                arg = call.args[0]
                if isinstance(arg, relay.expr.Call) and arg.op.name == "qnn.csi.transpose":
                    trans2_attrs = _qnn_attrs(arg.attrs)
                    if tuple(trans2_attrs["axes"]) == (0, 3, 1, 2):
                        is_struct = True

        return is_struct

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)
        outer = self

        class InterMutator(relay.ExprMutator):
            """helper mutator"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]

                new_args = []
                for arg in op_args:
                    if isinstance(arg, relay.expr.Call):
                        if outer.detect_transpose_struct(arg):
                            # the input of first transpose
                            new_args.append(arg.args[0].args[0])
                        else:
                            new_args.append(arg)
                    elif isinstance(arg, relay.expr.Tuple):
                        new_tuple = []
                        for a in arg:
                            if isinstance(a, relay.expr.Call):
                                if outer.detect_transpose_struct(a):
                                    new_tuple.append(a.args[0].args[0])
                                else:
                                    new_tuple.append(a)
                            else:
                                new_tuple.append(a)
                        new_args.append(relay.expr.Tuple(new_tuple))
                    else:
                        new_args.append(arg)

                func = _get_csi_op(call.op.name)
                new_call = func(*new_args, **_qnn_attrs(call.attrs))
                return new_call

        return InterMutator().visit(func)


@function_pass(opt_level=1)
class Output2NHWC:
    """Try to modify output layout"""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)

        class InterMutator(relay.ExprMutator):
            """helper mutator"""

            def visit_call(self, call):
                op_name = call.op.name
                attrs = _qnn_attrs(call.attrs)
                if op_name == "qnn.csi.transpose" and tuple(attrs["axes"]) == (0, 3, 1, 2):
                    if call.args[0].op.name in NCHW2NHWC_FUNCS:
                        return call.args[0]
                else:
                    outs = infer_shape(call)
                    if outs and isinstance(outs, (tuple, list)) and isinstance(outs[0], int):
                        if len(outs) == 4 and outs[0] == 1:
                            trans_call = insert_transpose_call(
                                call,
                                axes=(0, 2, 3, 1),
                                q_params=[attrs["q_params"][-1], attrs["q_params"][-1]],
                                layer_name=f"transpose_after_{attrs['layer_name']}",
                            )
                            return trans_call
                return call

        return InterMutator().visit(func)


def csi_layout_convert(mod, src_layout="NCHW", dest_layout="NHWC", align=1, out_layout="NHWC"):
    """layout convert"""
    if align > 1:
        mod = transform.Sequential([ShapeAlign(align)])(mod)

    if src_layout == "NCHW" and dest_layout == "NHWC":
        opt_seq = [NCHW2NHWC(), RemoveTranspose(), FuseTRDense()]
        if out_layout == "NHWC":
            opt_seq.append(Output2NHWC())
        mod = transform.Sequential(opt_seq)(mod)

    return mod
