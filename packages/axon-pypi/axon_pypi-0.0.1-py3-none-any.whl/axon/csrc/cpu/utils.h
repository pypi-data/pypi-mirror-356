#ifndef __UTILS__H__
#define __UTILS__H__

#include <stdlib.h>

extern "C" {
  void reassign_array_ops(float* a, float* out, size_t size);
  void equal_array_ops(float* a, float* b, float* out, size_t size);
  void transpose_1d_array_ops(float* a, float* out, int* shape);
  void transpose_2d_array_ops(float* a, float* out, int* shape);
  void transpose_3d_array_ops(float* a, float* out, int* shape);
  void transpose_ndim_array_ops(float* a, float* out, int* shape, int ndim);
}

#endif