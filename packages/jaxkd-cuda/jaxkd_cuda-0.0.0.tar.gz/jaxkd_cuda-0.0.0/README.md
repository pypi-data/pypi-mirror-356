# jaxkd-cuda

This package contains CUDA extensions for [JAX *k*-D](https://github.com/dodgebc/jaxkd). It requires JAX, CMake, and a CUDA compiler (nvcc) to build. It is intended to be installed as an optional dependency to JAX *k*-D and used as an add-on like so:

`python -m pip install jaxkd[cuda]`

Note that the [cudaKDTree](https://github.com/ingowald/cudaKDTree) library is more powerful and flexible, and can be bound to JAX using the foreign function interface. See the sample bindings in `jaxkd_cuda/cukd` for a rough example of how to do this. [JaxKDTree](https://github.com/EiffL/JaxKDTree) also has an example, though it is no longer working with the current JAX API.

This extension uses a slightly different tree-building method to exactly match the behavior of the pure-JAX version. It only permutes an index array and chooses the dimension with the widest spread of points (not largest bounding box) to split. Currently the performance bottleneck is actually the reduce operations needed to compute this. There is also a substantial memory overhead (a few times the number of points), which can probably be reduced in the future. The neighbor query algorithm follows [[2](https://arxiv.org/abs/2210.12859)] and the neighbor counting is a trivial modification.