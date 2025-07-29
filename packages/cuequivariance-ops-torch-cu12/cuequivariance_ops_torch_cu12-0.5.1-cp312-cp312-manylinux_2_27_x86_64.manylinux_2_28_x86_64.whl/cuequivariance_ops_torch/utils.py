# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from typing import Any, Dict, List, Optional, Tuple, Union

import torch


def get_operator_from_module(module, operator_base_str, dtypes):
    def _get_dtype(dtype):
        if dtype is torch.float64:
            return "fp64"
        if dtype is torch.float32:
            return "fp32"
        if dtype is torch.float16:
            return "fp16"
        if dtype is torch.bfloat16:
            return "bf16"
        if dtype is torch.float64:
            return "fp64"
        if dtype is torch.int16:
            return "int16"
        if dtype is torch.int8:
            return "int8"
        if dtype is torch.int32:
            return "int32"
        if dtype is torch.int64:
            return "int64"
        else:
            raise Exception("Unreconginzied torch data type.")

    dtypes = [_get_dtype(dt) for dt in dtypes]
    return getattr(module, operator_base_str + "_" + "_".join(dtypes))


def get_tensor_meta_data(tensor: Optional[torch.Tensor]) -> Dict[str, Any]:
    if tensor is None:
        return {"size": None, "dtype": None, "device": None}
    return {"size": tensor.size(), "dtype": tensor.dtype, "device": tensor.device}


def maybe_detach(tensor: torch.Tensor) -> Optional[torch.Tensor]:
    return None if tensor is None else tensor.detach().contiguous()


def maybe_size(tensor: torch.Tensor, dim: int = -1) -> int:
    return tensor.size(dim) if tensor is not None else 0


# The following functions are intended for usages where a gradient is only
# initialized if we have the corresponding ctx.needs_input_grads


def maybe_empty_like(
    input: torch.Tensor, create_tensor: bool = True, **kwargs
) -> Optional[torch.Tensor]:
    return torch.empty_like(input, **kwargs) if create_tensor else None


def maybe_empty(
    size: Union[List[int], Tuple[int], torch.Size],
    device: torch.device,
    dtype: torch.dtype,
    create_tensor: bool = True,
) -> Optional[torch.Tensor]:
    return torch.empty(size, device=device, dtype=dtype) if create_tensor else None


def maybe_zeros_like(
    input: torch.Tensor, create_tensor: bool = True
) -> Optional[torch.Tensor]:
    return torch.zeros_like(input) if create_tensor else None


def maybe_zeros(
    size: Union[List[int], Tuple[int], torch.Size],
    device: torch.device,
    dtype: torch.dtype,
    create_tensor: bool = True,
) -> Optional[torch.Tensor]:
    return torch.zeros(size, device=device, dtype=dtype) if create_tensor else None
