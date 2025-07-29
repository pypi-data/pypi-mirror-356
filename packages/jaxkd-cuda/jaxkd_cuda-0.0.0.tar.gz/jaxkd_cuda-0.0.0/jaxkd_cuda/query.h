// query.h
#pragma once

#include <cmath>
#include <cuda_runtime.h>
#include "common.h"

__forceinline__ __device__ void insert_neighbor(
    uint32_t* neighbors,
    float* distances,
    uint32_t current_index,
    float current_distance,
    int k
) {
    int i = k - 1;
    while ((i > 0) && (current_distance < distances[i-1])) {
        neighbors[i] = neighbors[i-1];
        distances[i] = distances[i-1];
        --i;
    }
    neighbors[i] = current_index;
    distances[i] = current_distance;

}

template <int N_DIM>
__forceinline__ __device__ void query_neighbors_impl(
    const float* points, // (N, d)
    const uint32_t* indices, // (N,)
    const int8_t* split_dims, // (N,)
    const float* query, // (d,)
    uint32_t* neighbors, // (k,) output buffer
    float* distances, // (k,) output buffer
    int k, // number of neighbors to find
    size_t n_points // points in tree, can be less if only querying upper levels
) {

    // initialize distances to infinity (NOTE: could have local arrays in registers explicitly, not a huge difference but could explore)
    float max_distance = INFINITY;
    #pragma unroll
    for (int i = 0; i < k; ++i) {
        distances[i] = INFINITY;
        neighbors[i] = 0;
    }

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
            float current_distance = compute_square_distance<N_DIM>(points + current_index * N_DIM, query);
            if (current_distance < max_distance) {
                insert_neighbor(neighbors, distances, current_index, current_distance, k);
                max_distance = distances[k - 1];
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

    // take square root to get actual distances
    #pragma unroll
    for (int i = 0; i < k; ++i) {
        distances[i] = sqrtf(distances[i]);
    }
}

template <int N_DIM>
__global__ void query_neighbors_kernel(
    const float* points,
    const uint32_t* indices,
    const int8_t* split_dims,
    const float* queries,
    uint32_t* neighbors,
    float* distances,
    int k,
    size_t n_points,
    size_t n_queries
) {
    size_t tid = threadIdx.x + blockIdx.x * blockDim.x;
    if (tid >= n_queries) return;
    query_neighbors_impl<N_DIM>(
        points,
        indices,
        split_dims,
        queries + tid * N_DIM,
        neighbors + tid * k,
        distances + tid * k,
        k,
        n_points
    );
}

template <int N_DIM>
__host__ void query_neighbors(
    cudaStream_t stream,
    const float* points,
    const uint32_t* indices,
    const int8_t* split_dims,
    const float* queries,
    uint32_t* neighbors,
    float* distances,
    int k,
    size_t n_points,
    size_t n_queries
) {
    size_t n_threads = n_queries;
    size_t threads_per_block = 256;
    size_t n_blocks = (n_threads + threads_per_block - 1) / threads_per_block;
    query_neighbors_kernel<N_DIM><<<n_blocks, threads_per_block, 0, stream>>>(
        points,
        indices,
        split_dims,
        queries,
        neighbors,
        distances,
        k,
        n_points,
        n_queries
    );
}