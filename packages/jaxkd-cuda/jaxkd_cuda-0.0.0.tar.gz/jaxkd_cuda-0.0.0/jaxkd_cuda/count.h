// count.h
#pragma once

#include <cmath>
#include <cuda_runtime.h>
#include "common.h"

// TODO: implement a unified traverse_tree and have query_neighbors and count_neighbors call it like in jax version

template <int N_DIM>
__forceinline__ __device__ void count_neighbors_impl(
    const float* points, // (N, d)
    const uint32_t* indices, // (N,)
    const int8_t* split_dims, // (N,)
    const float* query, // (d,)
    const float* distances, // (R,) distances to search
    uint32_t* counts, // (R,) output buffer
    size_t n_points, // points in tree, can be less if only querying upper levels
    size_t n_distances
) {

    // calculate maximum distance
    float max_distance = distances[0];
    for (int i = 1; i < n_distances; ++i) {
        if (distances[i] > max_distance) {
            max_distance = distances[i];
        }
    }
    // square for distance comparison
    max_distance = max_distance * max_distance;

    // set up traversal variables
    uint32_t current = 0;
    uint32_t root_parent = (current - uint32_t(1)) / 2;
    uint32_t previous = root_parent;
    uint32_t next = 0;
    float current_point[N_DIM];

    // traverse until we return to root
    while (current != root_parent) {
        uint32_t parent = (current - uint32_t(1)) / 2;
        uint32_t current_index = indices[current];
        int8_t split_dim = split_dims[current];
        #pragma unroll
        for (int i = 0; i < N_DIM; ++i) {
            current_point[i] = points[current_index * N_DIM + i];
        }

        // update neighbor array if necessary
        if (previous == parent) {
            float current_distance = compute_square_distance<N_DIM>(current_point, query);
            for (int i = 0; i < n_distances; ++i) {
                if (current_distance < distances[i] * distances[i]) {
                    counts[i]++;
                }
            }
        }

        // locate children and determine if far child in range
        float split_distance = query[split_dim] - current_point[split_dim];
        uint32_t near_side = (split_distance >= 0.0f);
        uint32_t near_child = (2 * current + 1) + near_side;
        uint32_t far_child = (2 * current + 2) - near_side;
        uint32_t far_in_range = (far_child < n_points) && (split_distance * split_distance <= max_distance);

        // determine next node to traverse
        if (previous == parent) {
            if (near_child < n_points) next = near_child;
            else if (far_in_range) next = far_child;
            else next = parent;
        } else if (previous == near_child) {
            if (far_in_range) next = far_child;
            else next = parent;
        } else {
            next = parent;
        }
        previous = current;
        current = next;
    }
}

// NOTE: could process different radii in parallel as well,
// could also have non-broadcasted distances (R,) for memory
// think about these later
template <int N_DIM>
__global__ void count_neighbors_kernel(
    const float* points, // (N, d)
    const uint32_t* indices, // (N,)
    const int8_t* split_dims, // (N,)
    const float* queries, // (Q, d)
    const float* distances, // (Q, R)
    uint32_t* counts, // output buffer (Q, R)
    size_t n_points,
    size_t n_queries,
    size_t n_distances
) {
    size_t tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= n_queries) return;
    count_neighbors_impl<N_DIM>(
        points,
        indices,
        split_dims,
        queries + tid * N_DIM,
        distances + tid * n_distances,
        counts + tid * n_distances,
        n_points,
        n_distances
    );
}

template <int N_DIM>
__host__ void count_neighbors(
    cudaStream_t stream,
    const float* points,
    const uint32_t* indices,
    const int8_t* split_dims,
    const float* queries,
    float* distances,
    uint32_t* counts,
    size_t n_points,
    size_t n_queries,
    size_t n_distances
) {
    size_t n_threads = n_queries * n_distances;
    size_t threads_per_block = 256;
    size_t n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
    fill_kernel<uint32_t><<<n_blocks, threads_per_block, 0, stream>>>(counts, 0, n_queries * n_distances);

    n_threads = n_queries;
    n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
    count_neighbors_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(
        points,
        indices,
        split_dims,
        queries,
        distances,
        counts,
        n_points,
        n_queries,
        n_distances
    );
}