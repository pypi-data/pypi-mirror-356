/*
 * Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once
namespace kernelcatcher::utils {

enum class Datatype : int {
  kFloat32  = 0,
  kFloat64  = 1,
  kFloat16  = 2,
  kBFloat16 = 3,
  kInt32    = 4,
  kInt64    = 5
};

}  // namespace kernelcatcher::utils
