// common.h
#pragma once

#include <cuda_runtime.h>

// __forceinline__ __device__ void traverse_next(uint32_t* current_ptr, uint32_t* previous_ptr, uint32_t parent, uint32_t near_child, uint32_t far_child, bool far_in_range, size_t n_points) {
//     uint32_t current = *current_ptr;
//     uint32_t previous = *previous_ptr;
//     uint32_t next;

//     if (previous == parent) {
//         if (near_child < n_points) {
//             next = near_child;
//         } else if (far_in_range) {
//             next = far_child;
//         } else {
//             next = parent;
//         }
//     } else if (previous == near_child) {
//         if (far_in_range) {
//             next = far_child;
//         } else {
//             next = parent;
//         }
//     } else {
//         next = parent;
//     }
//     *previous_ptr = current;
//     *current_ptr = next;
// }

template <typename T, int N_DIM>
__global__ void reorder_kernel(const T* a, const uint32_t* indices, T* out, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    #pragma unroll
    for (int j = 0; j < N_DIM; ++j) {
        out[i * N_DIM + j] = a[indices[i] * N_DIM + j];
    }
}

template <typename T, int N_DIM>
__global__ void transpose_kernel(T* a, T* out, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    size_t row = i / N_DIM;
    size_t col = i % N_DIM;
    size_t new_index = col * (n / N_DIM) + row;
    out[new_index] = a[i];
}

template <typename T>
__global__ void fill_kernel(T* a, T value, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    a[i] = value;
}

template <typename T>
__global__ void arange_kernel(T* a, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) a[i] = (T)i;
}

template <int N_DIM>
__forceinline__ __device__ float compute_square_distance(
    const float* point_a, // (d,)
    const float* point_b // (d,)
) {
    float dist = 0.0f;
    #pragma unroll
    for (int i = 0; i < N_DIM; ++i) {
        float diff = point_a[i] - point_b[i];
        dist += diff * diff;
    }
    return dist;
}

__host__ __device__ uint32_t floored_log2(uint32_t x) {
    return (x > 0) ? 31 - __builtin_clz(x) : 0;  // returns 0 for x = 0
}

__host__ __device__ uint64_t floored_log2(uint64_t x) {
    return (x > 0) ? 63 - __builtin_clzll(x) : 0;  // returns 0 for x = 0
}