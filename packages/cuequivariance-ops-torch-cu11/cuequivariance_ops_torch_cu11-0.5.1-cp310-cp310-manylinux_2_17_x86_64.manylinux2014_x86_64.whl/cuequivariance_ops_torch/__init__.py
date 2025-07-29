# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import torch

from cuequivariance_ops_torch._version import __git_commit__, __version__

import cuequivariance_ops

from cuequivariance_ops_torch.segmented_transpose import (
    segmented_transpose,
)


from cuequivariance_ops_torch.fused_tensor_product import (
    fused_tensor_product,
    FusedTensorProductOp3,
    FusedTensorProductOp4,
    tensor_product_info_as_ctype,
    int_mappings_to_mode,
)

from cuequivariance_ops_torch.symmetric_tensor_contraction import (
    SymmetricTensorContraction,
)

from cuequivariance_ops_torch.tensor_product_uniform_1d import (
    TensorProductUniform4x1d,
    TensorProductUniform1d,
)

from cuequivariance_ops_torch.tensor_product_uniform_1d_indexed import (
    TensorProductUniform4x1dIndexed,
    TensorProductUniform3x1dIndexed,
)

from cuequivariance_ops_torch.triangle_attention import triangle_attention

__all__ = [
    "segmented_transpose",
    "fused_tensor_product",
    "FusedTensorProductOp3",
    "FusedTensorProductOp4",
    "tensor_product_info_as_ctype",
    "int_mappings_to_mode",
    "SymmetricTensorContraction",
    "TensorProductUniform4x1dIndexed",
    "TensorProductUniform3x1dIndexed",
    "TensorProductUniform4x1d",
    "TensorProductUniform1d",
    "triangle_attention"
]

try:
    from cuequivariance_ops_torch.triangle_multiplicative_update import triangle_multiplicative_update
    from cuequivariance_ops_torch.triangle_multiplicative_update import Precision as TriMulPrecision
except Exception as e:
    IMPORT_EXCEPTION = e
    def triangle_multiplicative_update(*args, **kwargs):
        global IMPORT_EXCEPTION
        raise Exception(f"Failed to import Triton-based component: triangle_multiplicative_update:\n{IMPORT_EXCEPTION}\n"
                        "Please make sure to install triton==3.3.0. Other versions may not work!")

__all__ += [
    "triangle_multiplicative_update",
    "TriMulPrecision"
]
