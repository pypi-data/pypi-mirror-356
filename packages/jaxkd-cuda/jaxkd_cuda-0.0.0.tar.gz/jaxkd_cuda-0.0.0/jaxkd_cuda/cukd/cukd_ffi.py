import ctypes
from pathlib import Path
import numpy as np
import jax
import jax.numpy as jnp

def register_cukd():
    so_path = next(Path("jaxkd_cuda/cukd/build").glob("libjaxcukd*.so"), None)
    libjaxcukd = ctypes.cdll.LoadLibrary(str(so_path))
    jax.ffi.register_ffi_target(
        "build_and_query", jax.ffi.pycapsule(libjaxcukd.build_and_query), platform="gpu"
    )

def cukd_query_neighbors(points, queries, k: int):
    call = jax.ffi.ffi_call(
        "build_and_query",
        jax.ShapeDtypeStruct((len(queries), k), jnp.int32),
        vmap_method="sequential",
    )
    neighbors = call(points, queries, k=np.int32(k))
    distances = jnp.linalg.norm(points[neighbors] - queries[:, jnp.newaxis], axis=-1)
    return neighbors, distances