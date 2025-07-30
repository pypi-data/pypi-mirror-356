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
"""
RISCV-generic schedule rules.
"""
from .arithmetic import Arithmetic
from .memcpy_ops import Memcpy_Ops
from .sqrt import Sqrt
from .relu import Relu
from .maxpool import MaxPool
from .softmax import Softmax
from .conv2d import Conv2d
from .transpose import Transpose
from .avgpool import AvgPool
from .conv2d import Conv2d
from .gemm import Gemm
from .global_avgpool import Global_AvgPool
from .global_maxpool import Global_MaxPool
from .matmul_matrix import MatmulMatrix
from .conv2d_matrix import Conv2dMatrix
from .erf import Erf
from .mean import Mean
from .concat import Concat
from .cast import Cast
from .leaky_relu import Leaky_Relu
from .layer_norm import LayerNorm
from .sigmoid import Sigmoid
