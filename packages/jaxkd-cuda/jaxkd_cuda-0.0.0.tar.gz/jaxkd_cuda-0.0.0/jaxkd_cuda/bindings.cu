// bindings.cu
#include "xla/ffi/api/c_api.h"
#include "xla/ffi/api/ffi.h"
#include "build.h"
#include "query.h"
#include "count.h"

namespace ffi = xla::ffi;

ffi::Error build_tree_bind(
    cudaStream_t stream,
    ffi::Buffer<ffi::F32> points, // (N, d)
    ffi::ResultBuffer<ffi::U32> indices, // (N,)
    ffi::ResultBuffer<ffi::S8> split_dims // (N,)
) {
    size_t n_points = points.dimensions()[0];
    int n_dim = points.dimensions()[1];

    if (n_dim > 6) {
        return ffi::Error::InvalidArgument("only compiled for n_dim <= 6");
    }
    if (n_points > UINT32_MAX) {
        return ffi::Error::InvalidArgument("number of points must be less than 2^32 to fit indices in uint32_t");
    }

    // Terrible, should make this more concise with some trick
    if (n_dim == 1) {
        build_tree<1>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    } else if (n_dim == 2) {
        build_tree<2>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    } else if (n_dim == 3) {
        build_tree<3>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    } else if (n_dim == 4) {
        build_tree<4>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    } else if (n_dim == 5) {
        build_tree<5>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    } else if (n_dim == 6) {
        build_tree<6>(stream, points.typed_data(), indices->typed_data(), split_dims->typed_data(), n_points);
    }

    return ffi::Error::Success();
}

XLA_FFI_DEFINE_HANDLER_SYMBOL(
    build_tree_xla, build_tree_bind,
    ffi::Ffi::Bind()
        .Ctx<ffi::PlatformStream<cudaStream_t>>()
        .Arg<ffi::Buffer<ffi::F32>>()  // points
        .Ret<ffi::Buffer<ffi::U32>>()  // indices
        .Ret<ffi::Buffer<ffi::S8>>()  // split_dims
);

ffi::Error query_neighbors_bind(
    cudaStream_t stream,
    ffi::Buffer<ffi::F32> points, // (N, d)
    ffi::Buffer<ffi::U32> indices, // (N,)
    ffi::Buffer<ffi::S8> split_dims, // (N,)
    ffi::Buffer<ffi::F32> queries, // (M, d)
    ffi::ResultBuffer<ffi::U32> neighbors, // (M, k)
    ffi::ResultBuffer<ffi::F32> distances, // (M, k)
    int k // number of neighbors to find
) {
    size_t n_points = points.dimensions()[0];
    size_t n_queries = queries.dimensions()[0];
    int n_dim = points.dimensions()[1];

    if (k <= 0) {
        return ffi::Error::InvalidArgument("k must be greater than 0");
    } else if (k > n_points) {
        return ffi::Error::InvalidArgument("k must be less than or equal to the number of points");
    }
    if (n_dim > 6) {
        return ffi::Error::InvalidArgument("only compiled for n_dim <= 6");
    }
    if (indices.dimensions()[0] != n_points) {
        return ffi::Error::InvalidArgument("indices must have the same number of elements as points");
    }
    if (split_dims.dimensions()[0] != n_points) {
        return ffi::Error::InvalidArgument("split_dims must have the same number of elements as points");
    }
    if (queries.dimensions()[1] != n_dim) {
        return ffi::Error::InvalidArgument("queries must have the same number of dimensions as points");
    }
    if (n_points > UINT32_MAX) {
        return ffi::Error::InvalidArgument("number of points must be less than 2^32 to fit indices in uint32_t");
    }

    // Terrible, should make this more concise with some trick
    if (n_dim == 1) {
        query_neighbors<1>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    } else if (n_dim == 2) {
        query_neighbors<2>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    } else if (n_dim == 3) {
        query_neighbors<3>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    } else if (n_dim == 4) {
        query_neighbors<4>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    } else if (n_dim == 5) {
        query_neighbors<5>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    } else if (n_dim == 6) {
        query_neighbors<6>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), neighbors->typed_data(), distances->typed_data(), k, n_points, n_queries);
    }

    return ffi::Error::Success();
}

XLA_FFI_DEFINE_HANDLER_SYMBOL(
    query_neighbors_xla, query_neighbors_bind,
    ffi::Ffi::Bind()
        .Ctx<ffi::PlatformStream<cudaStream_t>>()
        .Arg<ffi::Buffer<ffi::F32>>()  // points
        .Arg<ffi::Buffer<ffi::U32>>()  // indices
        .Arg<ffi::Buffer<ffi::S8>>()  // split_dims
        .Arg<ffi::Buffer<ffi::F32>>()  // queries
        .Ret<ffi::Buffer<ffi::U32>>()  // neighbors
        .Ret<ffi::Buffer<ffi::F32>>()  // distances
        .Attr<int>("k")
);

ffi::Error count_neighbors_bind(
    cudaStream_t stream,
    ffi::Buffer<ffi::F32> points, // (N, d)
    ffi::Buffer<ffi::U32> indices, // (N,)
    ffi::Buffer<ffi::S8> split_dims, // (N,)
    ffi::Buffer<ffi::F32> queries, // (Q, d)
    ffi::Buffer<ffi::F32> distances, // (Q, R)
    ffi::ResultBuffer<ffi::U32> counts // (Q, R)
) {
    size_t n_points = points.dimensions()[0];
    size_t n_queries = queries.dimensions()[0];
    size_t n_distances = distances.dimensions()[1];
    int n_dim = points.dimensions()[1];

    if (n_dim > 6) {
        return ffi::Error::InvalidArgument("only compiled for n_dim <= 6");
    }
    if (indices.dimensions()[0] != n_points) {
        return ffi::Error::InvalidArgument("indices must have the same number of elements as points");
    }
    if (split_dims.dimensions()[0] != n_points) {
        return ffi::Error::InvalidArgument("split_dims must have the same number of elements as points");
    }
    if (queries.dimensions()[1] != n_dim) {
        return ffi::Error::InvalidArgument("queries must have the same number of dimensions as points");
    }
    if (distances.dimensions()[0] != n_queries) {
        return ffi::Error::InvalidArgument("distances must have the same number of queries as queries");
    }
    if (n_points > UINT32_MAX) {
        return ffi::Error::InvalidArgument("number of points must be less than 2^32 to fit indices in uint32_t");
    }

    // Terrible, should make this more concise with some trick
    if (n_dim == 1) {
        count_neighbors<1>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    } else if (n_dim == 2) {
        count_neighbors<2>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    } else if (n_dim == 3) {
        count_neighbors<3>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    } else if (n_dim == 4) {
        count_neighbors<4>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    } else if (n_dim == 5) {
        count_neighbors<5>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    } else if (n_dim == 6) {
        count_neighbors<6>(stream, points.typed_data(), indices.typed_data(), split_dims.typed_data(), queries.typed_data(), distances.typed_data(), counts->typed_data(), n_points, n_queries, n_distances);
    }

    return ffi::Error::Success();
}

XLA_FFI_DEFINE_HANDLER_SYMBOL(
    count_neighbors_xla, count_neighbors_bind,
    ffi::Ffi::Bind()
        .Ctx<ffi::PlatformStream<cudaStream_t>>()
        .Arg<ffi::Buffer<ffi::F32>>()  // points
        .Arg<ffi::Buffer<ffi::U32>>()  // indices
        .Arg<ffi::Buffer<ffi::S8>>()  // split_dims
        .Arg<ffi::Buffer<ffi::F32>>()  // queries
        .Arg<ffi::Buffer<ffi::F32>>()  // distances
        .Ret<ffi::Buffer<ffi::U32>>()  // counts
);