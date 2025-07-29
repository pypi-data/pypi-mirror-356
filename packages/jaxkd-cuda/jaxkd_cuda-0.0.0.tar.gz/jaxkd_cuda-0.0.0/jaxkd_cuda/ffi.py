import ctypes
from pathlib import Path
import jax
import jax.numpy as jnp
import numpy as np

def _register():    
    so_path = next(Path(__file__).parent.glob("libjaxkd_cuda*"))
    jaxkd_cuda_lib = ctypes.cdll.LoadLibrary(str(so_path))
    jax.ffi.register_ffi_target("jaxkd_cuda_build_tree", jax.ffi.pycapsule(jaxkd_cuda_lib.build_tree_xla), platform="CUDA")
    jax.ffi.register_ffi_target("jaxkd_cuda_query_neighbors", jax.ffi.pycapsule(jaxkd_cuda_lib.query_neighbors_xla), platform="CUDA")
    jax.ffi.register_ffi_target("jaxkd_cuda_count_neighbors", jax.ffi.pycapsule(jaxkd_cuda_lib.count_neighbors_xla), platform="CUDA")
    
def build_tree(points):
    if points.dtype != jnp.float32:
        raise TypeError("CUDA build only supports 32-bit for now.")
    call = jax.ffi.ffi_call(
        "jaxkd_cuda_build_tree",
        (
            jax.ShapeDtypeStruct((len(points),), jnp.uint32),
            jax.ShapeDtypeStruct((len(points),), jnp.int8),
        ),
        vmap_method="sequential",
    )
    indices, split_dims = call(points)
    return points, indices, split_dims

def query_neighbors(tree, queries, k, unsigned=False):
    points, indices, split_dims = tree
    if queries.dtype != jnp.float32 or points.dtype != jnp.float32:
        raise TypeError("CUDA query only supports 32-bit for now.")
    if split_dims is None:
        raise ValueError("CUDA query only supports optimized trees for now.")
    call = jax.ffi.ffi_call(
        "jaxkd_cuda_query_neighbors",
        (
            jax.ShapeDtypeStruct((len(queries), k), jnp.uint32),
            jax.ShapeDtypeStruct((len(queries), k), jnp.float32),
        ),
        vmap_method="sequential",
    )
    neighbors, distances = call(points, jnp.asarray(indices, dtype=jnp.uint32), split_dims, queries, k=np.int32(k))
    distances = jnp.linalg.norm(points[neighbors] - queries[:, jnp.newaxis], axis=-1) # recompute to enable differentiation
    if unsigned:
        return neighbors, distances
    return jnp.asarray(neighbors, dtype=int), distances

def count_neighbors(tree, queries, distances, unsigned=False):
    points, indices, split_dims = tree
    if queries.dtype != jnp.float32 or points.dtype != jnp.float32 or distances.dtype != jnp.float32:
        raise TypeError("CUDA query only supports 32-bit for now.")
    if split_dims is None:
        raise ValueError("CUDA query only supports optimized trees for now.")
    call = jax.ffi.ffi_call(
        "jaxkd_cuda_count_neighbors",
        jax.ShapeDtypeStruct(distances.shape, jnp.uint32),
        vmap_method="sequential",
    )
    counts = call(points, jnp.asarray(indices, dtype=jnp.uint32), split_dims, queries, distances)
    if unsigned:
        return counts
    return jnp.asarray(counts, dtype=int)
