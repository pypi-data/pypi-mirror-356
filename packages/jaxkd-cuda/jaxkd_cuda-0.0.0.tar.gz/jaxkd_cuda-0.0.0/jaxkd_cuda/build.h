// build.h
#pragma once

#include <cmath>
#include <cuda_runtime.h>
#include "common.h"
#include <cub/cub.cuh>

// tree math

__forceinline__ __host__ __device__ size_t tree_size(size_t n_levels) {
    return (size_t(1) << n_levels) - 1;
}

__forceinline__ __device__ size_t segment_offset(size_t i, size_t level, size_t n_levels, size_t n_points) {
    size_t height = n_levels - level - 1;
    size_t max_leaf = n_points - tree_size(n_levels - 1);
    size_t n_leaf = min(i * (1 << height), max_leaf);
    return i * tree_size(height) + n_leaf + tree_size(level);
}

__forceinline__ __device__ size_t inv_segment_offset(size_t offset, size_t level, size_t n_levels, size_t n_points) {
    size_t height = n_levels - level - 1;
    size_t max_leaf = n_points - tree_size(n_levels - 1);
    size_t sub1 = tree_size(level) + max_leaf;
    size_t sub2 = tree_size(level);
    size_t i1 = offset >= sub1 ? (offset - sub1) / tree_size(height) : 0;
    size_t i2 = offset >= sub2 ? (offset - sub2) / (tree_size(height) + (1 << height)) : 0;
    return max(i1, i2);
}

__forceinline__ __device__ size_t median_index(size_t i, size_t level, size_t n_levels, size_t n_points) {
    size_t height = n_levels - level - 1;
    size_t max_leaf = n_points - tree_size(n_levels - 1);
    size_t n_leaf = min(i * (1 << height) + (1 << (height - 1)), max_leaf);
    return i * tree_size(height) + tree_size(height - 1) + n_leaf + tree_size(level);
}

__forceinline__ __device__ size_t inv_median_index(size_t idx, size_t level, size_t n_levels, size_t n_points) {
    size_t height = n_levels - level - 1;
    size_t max_leaf = n_points - tree_size(n_levels - 1);
    size_t sub1 = tree_size(level) + tree_size(height - 1) + max_leaf;
    size_t sub2 = tree_size(level) + tree_size(height - 1) + (1 << (height - 1));
    size_t i1 = idx >= sub1 ? 1 + (idx - sub1) / tree_size(height) : 0;
    size_t i2 = idx >= sub2 ? 1 + (idx - sub2) / (tree_size(height) + (1 << height)) : 0;
    return max(i1, i2);
}

__forceinline__ __device__ size_t destination_index(size_t idx, size_t level, size_t n_levels, size_t n_points) {
    if (idx < tree_size(level)) return idx;
    size_t inv = inv_median_index(idx, level, n_levels, n_points);
    size_t prev_inv = idx > 0 ? inv_median_index(idx - 1, level, n_levels, n_points) : inv;
    if (inv != prev_inv) return inv + tree_size(level) - 1;
    else return idx - inv + (1 << level);
}

// kernels

__global__ void reorder_indices_kernel(
    const uint32_t* indices,
    uint32_t* new_indices,
    size_t level,
    size_t n_levels,
    size_t n_points
) {
    size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx >= n_points) return;
    size_t dest = destination_index(idx, level, n_levels, n_points);
    new_indices[dest] = indices[idx];
}

__global__ void compute_offsets_kernel(
    uint32_t* offsets,
    size_t level,
    size_t n_levels,
    size_t n_points
) {
    size_t i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i >= (1 << level) + 1) return;
    size_t offset = segment_offset(i, level, n_levels, n_points);
    offsets[i] = offset;
}

template <int N_DIM>
__global__ void copy_dim_kernel(
    const float* points,
    const uint32_t* indices,
    int8_t dim,
    float* values_along_dim,
    size_t n_points
) {
    size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx >= n_points) return;
    values_along_dim[idx] = points[indices[idx] * N_DIM + dim];
}

template <int N_DIM>
__global__ void copy_split_dim_kernel(
    const float* points,
    const uint32_t* indices,
    const int8_t* split_dims,
    float* values_along_dim,
    size_t level,
    size_t n_levels,
    size_t n_points
) {
    size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx >= n_points) return;
    int8_t split_dim;
    if (idx < tree_size(level)) {
        split_dim = split_dims[idx];
    } else {
        size_t node = inv_segment_offset(idx, level, n_levels, n_points) + tree_size(level);
        split_dim = split_dims[node];
    }
    values_along_dim[idx] = points[indices[idx] * N_DIM + split_dim];
}

template <int N_DIM>
__global__ void update_split_dims(
    const float* new_segment_min,
    const float* new_segment_max,
    float* segment_range,
    int8_t* split_dims,
    int8_t new_split_dim,
    size_t level,
    size_t n_segments
) {
    size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx >= n_segments) return;
    float new_segment_range = new_segment_max[idx] - new_segment_min[idx];
    if (new_segment_range > segment_range[idx]) {
        size_t node = tree_size(level) + idx;
        split_dims[node] = new_split_dim;
        segment_range[idx] = new_segment_range;
    }
}

template <int N_DIM>
__host__ void build_tree(
    cudaStream_t stream,
    const float* points,
    uint32_t* indices,
    int8_t* split_dims,
    size_t n_points
) {
    size_t n_levels = floored_log2(n_points) + 1;
    size_t max_segments = 1 << (n_levels - 2);
    size_t n_threads;
    size_t threads_per_block = 256;
    size_t n_blocks;

    // allocate temporary memory for double buffers
    uint32_t *indices_alt;
    float *values_along_dim, *values_along_dim_alt;
    cudaMalloc(&indices_alt, n_points * sizeof(uint32_t));
    cudaMalloc(&values_along_dim, n_points * sizeof(float));
    cudaMalloc(&values_along_dim_alt, n_points * sizeof(float));
    cub::DoubleBuffer<uint32_t> indices_buffer(indices, indices_alt);
    cub::DoubleBuffer<float> values_buffer(values_along_dim, values_along_dim_alt);

    // allocate temporary memory for segment ops
    uint32_t *offsets;
    float *segment_min, *segment_max, *segment_range;
    cudaMalloc(&offsets, (max_segments + 1) * sizeof(uint32_t));
    cudaMalloc(&segment_min, max_segments * sizeof(float));
    cudaMalloc(&segment_max, max_segments * sizeof(float));
    cudaMalloc(&segment_range, max_segments * sizeof(float));

    // allocate temporary memory for CUB ops
    // a bit risky, not 100% sure this is always enough since docs are unclear, but it works
    void *temp_storage;
    size_t temp_storage_bytes = n_points * sizeof(uint32_t);
    cudaMalloc(&temp_storage, temp_storage_bytes);

    // fill indices and split_dims
    n_threads = n_points;
    n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
    arange_kernel<uint32_t><<<n_blocks, threads_per_block, 0, stream>>>(indices_buffer.Current(), n_points);
    fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims, 0, n_points);

    // loop, MUST ALWAYS HAVE level < n_levels - 1
    for (size_t level = 0; level < n_levels - 1; ++level) {

        // compute offsets
        size_t n_segments = (1 << level);
        n_threads = n_segments + 1;
        n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
        compute_offsets_kernel<<<n_blocks, threads_per_block, 0, stream>>>(offsets, level, n_levels, n_points);

        // compute split dims for this level
        n_threads = n_segments;
        n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
        fill_kernel<float><<<n_blocks, threads_per_block, 0, stream>>>(segment_range, -1.0f, n_segments);
        for (int8_t i = 0; i < N_DIM; ++i) {
            n_threads = n_points;
            n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
            copy_dim_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(points, indices_buffer.Current(), i, values_along_dim, n_points);
            cub::DeviceSegmentedReduce::Min(nullptr, temp_storage_bytes, values_along_dim, segment_min, n_segments, offsets, offsets + 1, stream);
            cub::DeviceSegmentedReduce::Min(temp_storage, temp_storage_bytes, values_along_dim, segment_min, n_segments, offsets, offsets + 1, stream);
            cub::DeviceSegmentedReduce::Max(nullptr, temp_storage_bytes, values_along_dim, segment_max, n_segments, offsets, offsets + 1, stream);
            cub::DeviceSegmentedReduce::Max(temp_storage, temp_storage_bytes, values_along_dim, segment_max, n_segments, offsets, offsets + 1, stream);

            n_threads = n_segments;
            n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
            update_split_dims<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(segment_min, segment_max, segment_range, split_dims, i, level, n_segments);
        }

        // compute un-optimized split dims for this level, just cycle through dimensions (don't actually need split_dims array then)
        // n_threads = n_segments;
        // n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
        // fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims + tree_size(level), level % N_DIM, n_segments);

        // copy values along split dimension
        n_threads = n_points;
        n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
        copy_split_dim_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(points, indices_buffer.Current(), split_dims, values_along_dim, level, n_levels, n_points);

        // segment sort indices based on values
        cub::DeviceSegmentedSort::SortPairs(nullptr, temp_storage_bytes, values_buffer, indices_buffer, n_points, n_segments, offsets, offsets + 1, stream);
        cub::DeviceSegmentedSort::SortPairs(temp_storage, temp_storage_bytes, values_buffer, indices_buffer, n_points, n_segments, offsets, offsets + 1, stream);

        // select the median in each segment and put in tree order
        n_threads = n_points;
        n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
        reorder_indices_kernel<<<n_blocks, threads_per_block, 0, stream>>>(indices_buffer.Current(), indices_buffer.Alternate(), level, n_levels, n_points);
        indices_buffer.selector ^= 1; // swap buffers
    }

    // copy current indices to output
    if (indices_buffer.Current() != indices) {
        cudaMemcpyAsync(indices, indices_buffer.Current(), n_points * sizeof(uint32_t), cudaMemcpyDeviceToDevice, stream);
    }

    // fill leaf split_dims with -1
    n_threads = n_points - n_points/2;
    n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
    fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims + n_points/2, int8_t(-1), n_threads);

    // free temporary memory
    cudaStreamSynchronize(stream);
    cudaFree(indices_alt);
    cudaFree(values_along_dim);
    cudaFree(values_along_dim_alt);
    cudaFree(offsets);
    cudaFree(segment_min);
    cudaFree(segment_max);
    cudaFree(segment_range);
    cudaFree(temp_storage);
}


// VERSION WITH COPIED POINTS SORTED "IN-PLACE", NOT FASTER

// // tree math

// __forceinline__ __host__ __device__ size_t tree_size(size_t n_levels) {
//     return (size_t(1) << n_levels) - 1;
// }

// __forceinline__ __device__ size_t segment_offset(size_t i, size_t level, size_t n_levels, size_t n_points) {
//     size_t height = n_levels - level - 1;
//     size_t max_leaf = n_points - tree_size(n_levels - 1);
//     size_t n_leaf = min(i * (1 << height), max_leaf);
//     return i * tree_size(height) + n_leaf + tree_size(level);
// }

// __forceinline__ __device__ size_t inv_segment_offset(size_t offset, size_t level, size_t n_levels, size_t n_points) {
//     size_t height = n_levels - level - 1;
//     size_t max_leaf = n_points - tree_size(n_levels - 1);
//     size_t sub1 = tree_size(level) + max_leaf;
//     size_t sub2 = tree_size(level);
//     size_t i1 = offset >= sub1 ? (offset - sub1) / tree_size(height) : 0;
//     size_t i2 = offset >= sub2 ? (offset - sub2) / (tree_size(height) + (1 << height)) : 0;
//     return max(i1, i2);
// }

// __forceinline__ __device__ size_t median_index(size_t i, size_t level, size_t n_levels, size_t n_points) {
//     size_t height = n_levels - level - 1;
//     size_t max_leaf = n_points - tree_size(n_levels - 1);
//     size_t n_leaf = min(i * (1 << height) + (1 << (height - 1)), max_leaf);
//     return i * tree_size(height) + tree_size(height - 1) + n_leaf + tree_size(level);
// }

// __forceinline__ __device__ size_t inv_median_index(size_t idx, size_t level, size_t n_levels, size_t n_points) {
//     size_t height = n_levels - level - 1;
//     size_t max_leaf = n_points - tree_size(n_levels - 1);
//     size_t sub1 = tree_size(level) + tree_size(height - 1) + max_leaf;
//     size_t sub2 = tree_size(level) + tree_size(height - 1) + (1 << (height - 1));
//     size_t i1 = idx >= sub1 ? 1 + (idx - sub1) / tree_size(height) : 0;
//     size_t i2 = idx >= sub2 ? 1 + (idx - sub2) / (tree_size(height) + (1 << height)) : 0;
//     return max(i1, i2);
// }

// __forceinline__ __device__ size_t destination_index(size_t idx, size_t level, size_t n_levels, size_t n_points) {
//     if (idx < tree_size(level)) return idx;
//     size_t inv = inv_median_index(idx, level, n_levels, n_points);
//     size_t prev_inv = idx > 0 ? inv_median_index(idx - 1, level, n_levels, n_points) : inv;
//     if (inv != prev_inv) return inv + tree_size(level) - 1;
//     else return idx - inv + (1 << level);
// }

// // kernels

// __global__ void reorder_indices_kernel(
//     const uint32_t* indices,
//     uint32_t* new_indices,
//     size_t level,
//     size_t n_levels,
//     size_t n_points
// ) {
//     size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
//     if (idx >= n_points) return;
//     size_t dest = destination_index(idx, level, n_levels, n_points);
//     new_indices[dest] = indices[idx];
// }

// __global__ void compute_offsets_kernel(
//     uint32_t* offsets,
//     size_t level,
//     size_t n_levels,
//     size_t n_points
// ) {
//     size_t i = threadIdx.x + blockIdx.x * blockDim.x;
//     if (i >= (1 << level) + 1) return;
//     size_t offset = segment_offset(i, level, n_levels, n_points);
//     offsets[i] = offset;
// }

// template <int N_DIM>
// __global__ void copy_dim_kernel(
//     const float* points_sorted,
//     int8_t dim,
//     float* values_along_dim,
//     size_t n_points
// ) {
//     size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
//     if (idx >= n_points) return;
//     values_along_dim[idx] = points_sorted[idx * N_DIM + dim];
// }

// template <int N_DIM>
// __global__ void copy_split_dim_kernel(
//     const float* points_sorted,
//     const int8_t* split_dims,
//     float* values_along_dim,
//     size_t level,
//     size_t n_levels,
//     size_t n_points
// ) {
//     size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
//     if (idx >= n_points) return;
//     int8_t split_dim;
//     if (idx < tree_size(level)) {
//         split_dim = split_dims[idx];
//     } else {
//         size_t node = inv_segment_offset(idx, level, n_levels, n_points) + tree_size(level);
//         split_dim = split_dims[node];
//     }
//     values_along_dim[idx] = points_sorted[idx * N_DIM + split_dim];
// }


// // template <int N_DIM>
// // __global__ void copy_split_dim_kernel(
// //     const float* points,
// //     const uint32_t* indices,
// //     const int8_t* split_dims,
// //     float* values_along_dim,
// //     size_t level,
// //     size_t n_levels,
// //     size_t n_points
// // ) {
// //     size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
// //     if (idx >= n_points) return;
// //     int8_t split_dim;
// //     if (idx < tree_size(level)) {
// //         split_dim = split_dims[idx];
// //     } else {
// //         size_t node = inv_segment_offset(idx, level, n_levels, n_points) + tree_size(level);
// //         split_dim = split_dims[node];
// //     }
// //     values_along_dim[idx] = points[indices[idx] * N_DIM + split_dim];
// // }


// template <int N_DIM>
// __global__ void update_split_dims(
//     const float* new_segment_min,
//     const float* new_segment_max,
//     float* segment_range,
//     int8_t* split_dims,
//     int8_t new_split_dim,
//     size_t level,
//     size_t n_segments
// ) {
//     size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
//     if (idx >= n_segments) return;
//     float new_segment_range = new_segment_max[idx] - new_segment_min[idx];
//     if (new_segment_range > segment_range[idx]) {
//         size_t node = tree_size(level) + idx;
//         split_dims[node] = new_split_dim;
//         segment_range[idx] = new_segment_range;
//     }
// }

// template <int N_DIM>
// __host__ void build_tree(
//     cudaStream_t stream,
//     const float* points,
//     uint32_t* indices,
//     int8_t* split_dims,
//     size_t n_points
// ) {
//     size_t n_levels = floored_log2(n_points) + 1;
//     size_t max_segments = 1 << (n_levels - 2);
//     size_t n_threads;
//     size_t threads_per_block = 256;
//     size_t n_blocks;

//     // allocate temporary buffers to reorder points_sorted and indices
//     float *points_sorted, *points_sorted_alt;
//     uint32_t* indices_alt;
//     cudaMalloc(&points_sorted, n_points * N_DIM * sizeof(float));
//     cudaMalloc(&points_sorted_alt, n_points * N_DIM * sizeof(float));
//     cudaMalloc(&indices_alt, n_points * sizeof(uint32_t));
//     cub::DoubleBuffer<float> points_sorted_buffer(points_sorted, points_sorted_alt);
//     cub::DoubleBuffer<uint32_t> indices_buffer(indices, indices_alt);

//     // fill points_sorted, indices, and split_dims
//     cudaMemcpyAsync(points_sorted_buffer.Current(), points, n_points * N_DIM * sizeof(float), cudaMemcpyDeviceToDevice, stream);
//     n_threads = n_points;
//     n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//     arange_kernel<uint32_t><<<n_blocks, threads_per_block, 0, stream>>>(indices_buffer.Current(), n_points);
//     fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims, 0, n_points);

//     // allocate temporary memory for CUB operations
//     // not 100% sure this is always enough, CUB documentation is unclear, and maybe less memory is sufficient
//     size_t temp_storage_bytes = n_points * sizeof(uint32_t);
//     void *temp_storage;
//     cudaMalloc(&temp_storage, temp_storage_bytes);

//     // allocate temporary memory for segment min/max/range
//     // should be roughly equivalent to a single full n_points array
//     uint32_t *offsets;
//     float *segment_min, *segment_max, *segment_range;
//     cudaMalloc(&offsets, (max_segments + 1) * sizeof(uint32_t));
//     cudaMalloc(&segment_min, max_segments * sizeof(float));
//     cudaMalloc(&segment_max, max_segments * sizeof(float));
//     cudaMalloc(&segment_range, max_segments * sizeof(float));

//     // allocate extra memory for sorting, create double buffers
//     uint32_t *reorder, *reorder_alt;
//     float *values_along_dim, *values_along_dim_alt;
//     cudaMalloc(&reorder, n_points * sizeof(uint32_t));
//     cudaMalloc(&reorder_alt, n_points * sizeof(uint32_t));
//     cudaMalloc(&values_along_dim, n_points * sizeof(float));
//     cudaMalloc(&values_along_dim_alt, n_points * sizeof(float));
//     cub::DoubleBuffer<uint32_t> reorder_buffer(reorder, reorder_alt);
//     cub::DoubleBuffer<float> values_buffer(values_along_dim, values_along_dim_alt);

//     // loop, must always have level < n_levels - 1 or else indexing disasters will occur
//     for (size_t level = 0; level < n_levels - 1; ++level) {

//         // compute offsets
//         size_t n_segments = (1 << level);
//         n_threads = n_segments + 1;
//         n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         compute_offsets_kernel<<<n_blocks, threads_per_block, 0, stream>>>(offsets, level, n_levels, n_points);

//         // compute split dims for this level
//         // n_threads = n_segments;
//         // n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         // fill_kernel<float><<<n_blocks, threads_per_block, 0, stream>>>(segment_range, -1.0f, n_segments);
//         // for (int8_t i = 0; i < N_DIM; ++i) {
//         //     n_threads = n_points;
//         //     n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         //     copy_dim_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(points, indices_buffer.Current(), i, values_along_dim, n_points);
//         //     cub::DeviceSegmentedReduce::Min(nullptr, temp_storage_bytes, values_along_dim, segment_min, n_segments, offsets, offsets + 1, stream);
//         //     cub::DeviceSegmentedReduce::Min(temp_storage, temp_storage_bytes, values_along_dim, segment_min, n_segments, offsets, offsets + 1, stream);
//         //     cub::DeviceSegmentedReduce::Max(nullptr, temp_storage_bytes, values_along_dim, segment_max, n_segments, offsets, offsets + 1, stream);
//         //     cub::DeviceSegmentedReduce::Max(temp_storage, temp_storage_bytes, values_along_dim, segment_max, n_segments, offsets, offsets + 1, stream);

//         //     n_threads = n_segments;
//         //     n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         //     update_split_dims<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(segment_min, segment_max, segment_range, split_dims, i, level, n_segments);
//         // }

//         // compute un-optimized split dim for this level, just cycle through dimensions (don't really need split_dims then)
//         n_threads = n_segments;
//         n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims + tree_size(level), level % N_DIM, n_segments);

//         // copy values along split dimension and reset reorder buffer
//         n_threads = n_points;
//         n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         copy_split_dim_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(points_sorted_buffer.Current(), split_dims, values_buffer.Current(), level, n_levels, n_points);
//         arange_kernel<uint32_t><<<n_blocks, threads_per_block, 0, stream>>>(reorder_buffer.Current(), n_points);

//         // segment sort based on values along split dimension
//         cub::DeviceSegmentedSort::SortPairs(nullptr, temp_storage_bytes, values_buffer, reorder_buffer, n_points, n_segments, offsets, offsets + 1, stream);
//         cub::DeviceSegmentedSort::SortPairs(temp_storage, temp_storage_bytes, values_buffer, reorder_buffer, n_points, n_segments, offsets, offsets + 1, stream);

//         // select the median in each segment and put in tree order
//         n_threads = n_points;
//         n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         reorder_indices_kernel<<<n_blocks, threads_per_block, 0, stream>>>(reorder_buffer.Current(), reorder_buffer.Alternate(), level, n_levels, n_points);

//         // reorder points_sorted and indices
//         n_threads = n_points;
//         n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//         reorder_kernel<uint32_t, 1><<<n_blocks, threads_per_block, 0, stream>>>(indices_buffer.Current(), reorder_buffer.Alternate(), indices_buffer.Alternate(), n_points);
//         reorder_kernel<float, N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(points_sorted_buffer.Current(), reorder_buffer.Alternate(), points_sorted_buffer.Alternate(), n_points);
//         indices_buffer.selector ^= 1;
//         points_sorted_buffer.selector ^= 1;

//         cudaStreamSynchronize(stream);
//     }

//     // copy current indices to output
//     if (indices_buffer.Current() != indices) {
//         cudaMemcpyAsync(indices, indices_buffer.Current(), n_points * sizeof(uint32_t), cudaMemcpyDeviceToDevice, stream);
//     }

//     // fill leaf split_dims with -1
//     n_threads = n_points - n_points/2;
//     n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
//     fill_kernel<int8_t><<<n_blocks, threads_per_block, 0, stream>>>(split_dims + n_points/2, int8_t(-1), n_threads);

//     // free temporary memory
//     cudaStreamSynchronize(stream);
//     cudaFree(points_sorted);
//     cudaFree(points_sorted_alt);
//     cudaFree(indices_alt);
//     cudaFree(temp_storage);
//     cudaFree(offsets);
//     cudaFree(segment_min);
//     cudaFree(segment_max);
//     cudaFree(segment_range);
//     cudaFree(reorder);
//     cudaFree(reorder_alt);
//     cudaFree(values_along_dim);
//     cudaFree(values_along_dim_alt);
// }