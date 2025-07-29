cmake_minimum_required(VERSION 3.18...3.27)
project(jaxcukd LANGUAGES C CXX CUDA)

find_package(Python 3.10 COMPONENTS Interpreter Development.Module REQUIRED)

# Find FFI include directory
execute_process(
  COMMAND "${Python_EXECUTABLE}"
          "-c" "from jax import ffi; print(ffi.include_dir())"
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE XLA_DIR)
message(STATUS "XLA include directory: ${XLA_DIR}")

# Set CUDA architecture
set(CMAKE_CUDA_ARCHITECTURES native)

# Add bindings for cudaKDTree
add_library(jaxcukd SHARED cukd_bindings.cu)
target_include_directories(jaxcukd PRIVATE ${XLA_DIR} ../../../cudaKDTree)
set_target_properties(jaxcukd PROPERTIES POSITION_INDEPENDENT_CODE ON)
# target_link_libraries(jaxcukd PRIVATE cudaKDTree)