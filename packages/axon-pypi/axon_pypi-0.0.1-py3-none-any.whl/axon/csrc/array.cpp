#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "core/core.h"
#include "core/dtype.h"
#include "cpu/maths_ops.h"
#include "cpu/utils.h"
#include "array.h"
#include "cpu/red_ops.h"
#include "cpu/binary_ops.h"

Array* add_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != b->ndim) {
    fprintf(stderr, "arrays must have the same no of dims %d and %d for addition\n", a->ndim, b->ndim);
    exit(EXIT_FAILURE);
  }

  // checking if shapes match
  for (size_t i = 0; i < a->ndim; i++) {
    if (a->shape[i] != b->shape[i]) {
      fprintf(stderr, "arrays must have the same shape for addition\n");
      exit(EXIT_FAILURE);
    }
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  add_ops(a_float, b_float, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);

  return result;
}

Array* add_scalar_array(Array* a, float b) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(1);
  }
  add_scalar_ops(a_float, b, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = a->dtype;  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);

  return result;
}

Array* add_broadcasted_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int max_ndim = a->ndim > b->ndim ? a->ndim : b->ndim;
  int* broadcasted_shape = (int*)malloc(max_ndim * sizeof(int));
  if (broadcasted_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < max_ndim; i++) {
    int dim1 = i < a->ndim ? a->shape[a->ndim - 1 - i] : 1;
    int dim2 = i < b->ndim ? b->shape[b->ndim - 1 - i] : 1;
    if (dim1 != dim2 && dim1 != 1 && dim2 != 1) {
      fprintf(stderr, "shapes are not compatible for broadcasting\n");
      free(broadcasted_shape);
      exit(EXIT_FAILURE);
    }
    broadcasted_shape[max_ndim - 1 - i] = dim1 > dim2 ? dim1 : dim2;
  }

  // calculate broadcasted size
  size_t broadcasted_size = 1;
  for (int i = 0; i < max_ndim; i++) {
    broadcasted_size *= broadcasted_shape[i];
  }
  // convert both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(broadcasted_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  add_broadcasted_array_ops(a_float, b_float, out, broadcasted_shape, broadcasted_size, a->ndim, b->ndim, a->shape, b->shape);
  // determining result dtype using proper dtype promotion
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, max_ndim, broadcasted_shape, broadcasted_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(broadcasted_shape);  
  return result;
}

Array* sub_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != b->ndim) {
    fprintf(stderr, "arrays must have the same no of dims %d and %d for subtraction\n", a->ndim, b->ndim);
    exit(EXIT_FAILURE);
  }

  // checking if shapes match
  for (size_t i = 0; i < a->ndim; i++) {
    if (a->shape[i] != b->shape[i]) {
      fprintf(stderr, "arrays must have the same shape for subtraction\n");
      exit(EXIT_FAILURE);
    }
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  sub_ops(a_float, b_float, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);

  return result;
}

Array* sub_scalar_array(Array* a, float b) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(1);
  }
  sub_scalar_ops(a_float, b, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = a->dtype;  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);

  return result;
}

Array* sub_broadcasted_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int max_ndim = a->ndim > b->ndim ? a->ndim : b->ndim;
  int* broadcasted_shape = (int*)malloc(max_ndim * sizeof(int));
  if (broadcasted_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < max_ndim; i++) {
    int dim1 = i < a->ndim ? a->shape[a->ndim - 1 - i] : 1;
    int dim2 = i < b->ndim ? b->shape[b->ndim - 1 - i] : 1;
    if (dim1 != dim2 && dim1 != 1 && dim2 != 1) {
      fprintf(stderr, "shapes are not compatible for broadcasting\n");
      free(broadcasted_shape);
      exit(EXIT_FAILURE);
    }
    broadcasted_shape[max_ndim - 1 - i] = dim1 > dim2 ? dim1 : dim2;
  }

  // calculate broadcasted size
  size_t broadcasted_size = 1;
  for (int i = 0; i < max_ndim; i++) {
    broadcasted_size *= broadcasted_shape[i];
  }
  // convert both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(broadcasted_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  sub_broadcasted_array_ops(a_float, b_float, out, broadcasted_shape, broadcasted_size, a->ndim, b->ndim, a->shape, b->shape);
  // determining result dtype using proper dtype promotion
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, max_ndim, broadcasted_shape, broadcasted_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(broadcasted_shape);  
  return result;
}

Array* mul_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != b->ndim) {
    fprintf(stderr, "arrays must have the same no of dims %d and %d for multiplication\n", a->ndim, b->ndim);
    exit(EXIT_FAILURE);
  }

  // checking if shapes match
  for (size_t i = 0; i < a->ndim; i++) {
    if (a->shape[i] != b->shape[i]) {
      fprintf(stderr, "arrays must have the same shape for multiplication\n");
      exit(EXIT_FAILURE);
    }
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  mul_ops(a_float, b_float, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);

  return result;
}

Array* mul_scalar_array(Array* a, float b) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(1);
  }
  mul_scalar_ops(a_float, b, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = a->dtype;  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);

  return result;
}

Array* mul_broadcasted_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int max_ndim = a->ndim > b->ndim ? a->ndim : b->ndim;
  int* broadcasted_shape = (int*)malloc(max_ndim * sizeof(int));
  if (broadcasted_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < max_ndim; i++) {
    int dim1 = i < a->ndim ? a->shape[a->ndim - 1 - i] : 1;
    int dim2 = i < b->ndim ? b->shape[b->ndim - 1 - i] : 1;
    if (dim1 != dim2 && dim1 != 1 && dim2 != 1) {
      fprintf(stderr, "shapes are not compatible for broadcasting\n");
      free(broadcasted_shape);
      exit(EXIT_FAILURE);
    }
    broadcasted_shape[max_ndim - 1 - i] = dim1 > dim2 ? dim1 : dim2;
  }

  // calculate broadcasted size
  size_t broadcasted_size = 1;
  for (int i = 0; i < max_ndim; i++) {
    broadcasted_size *= broadcasted_shape[i];
  }
  // convert both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(broadcasted_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  mul_broadcasted_array_ops(a_float, b_float, out, broadcasted_shape, broadcasted_size, a->ndim, b->ndim, a->shape, b->shape);
  // determining result dtype using proper dtype promotion
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, max_ndim, broadcasted_shape, broadcasted_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(broadcasted_shape);  
  return result;
}

Array* div_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != b->ndim) {
    fprintf(stderr, "arrays must have the same no of dims %d and %d for division\n", a->ndim, b->ndim);
    exit(EXIT_FAILURE);
  }

  // checking if shapes match
  for (size_t i = 0; i < a->ndim; i++) {
    if (a->shape[i] != b->shape[i]) {
      fprintf(stderr, "arrays must have the same shape for division\n");
      exit(EXIT_FAILURE);
    }
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  div_ops(a_float, b_float, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);

  return result;
}

Array* div_scalar_array(Array* a, float b) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(1);
  }
  div_scalar_ops(a_float, b, out, a->size);  // Perform the addition operation
  dtype_t result_dtype = a->dtype;  // determining result dtype
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);

  return result;
}

Array* div_broadcasted_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int max_ndim = a->ndim > b->ndim ? a->ndim : b->ndim;
  int* broadcasted_shape = (int*)malloc(max_ndim * sizeof(int));
  if (broadcasted_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < max_ndim; i++) {
    int dim1 = i < a->ndim ? a->shape[a->ndim - 1 - i] : 1;
    int dim2 = i < b->ndim ? b->shape[b->ndim - 1 - i] : 1;
    if (dim1 != dim2 && dim1 != 1 && dim2 != 1) {
      fprintf(stderr, "shapes are not compatible for broadcasting\n");
      free(broadcasted_shape);
      exit(EXIT_FAILURE);
    }
    broadcasted_shape[max_ndim - 1 - i] = dim1 > dim2 ? dim1 : dim2;
  }

  // calculate broadcasted size
  size_t broadcasted_size = 1;
  for (int i = 0; i < max_ndim; i++) {
    broadcasted_size *= broadcasted_shape[i];
  }
  // convert both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(broadcasted_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(broadcasted_shape);
    exit(EXIT_FAILURE);
  }
  div_broadcasted_array_ops(a_float, b_float, out, broadcasted_shape, broadcasted_size, a->ndim, b->ndim, a->shape, b->shape);
  // determining result dtype using proper dtype promotion
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, max_ndim, broadcasted_shape, broadcasted_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(broadcasted_shape);  
  return result;
}

Array* matmul_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != 2 || b->ndim != 2) {
    fprintf(stderr, "Both arrays must be 2D for matrix multiplication\n");
    exit(EXIT_FAILURE);
  }
  if (a->shape[1] != b->shape[0]) {
    fprintf(stderr, "Inner dimensions must match for matrix multiplication: %d != %d\n", a->shape[1], b->shape[0]);
    exit(EXIT_FAILURE);
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  int* result_shape = (int*)malloc(2 * sizeof(int));    // result shape: [a->shape[0], b->shape[1]]
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  result_shape[0] = a->shape[0];
  result_shape[1] = b->shape[1];  // result is A rows × B rows (since we're doing A @ B^T)
  size_t result_size = result_shape[0] * result_shape[1];

  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  // performing optimized matrix multiplication (regular A @ B)
  matmul_array_ops(a_float, b_float, out, a->shape, b->shape);
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, 2, result_shape, result_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(result_shape);
  return result;
}

Array* batch_matmul_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != 3 || b->ndim != 3) {
    fprintf(stderr, "Both arrays must be 3D for batch matrix multiplication\n");
    exit(EXIT_FAILURE);
  }
  if (a->shape[0] != b->shape[0]) {
    fprintf(stderr, "Batch dimensions must match: %d != %d\n", a->shape[0], b->shape[0]);
    exit(EXIT_FAILURE);
  }
  if (a->shape[2] != b->shape[1]) {
    fprintf(stderr, "Inner dimensions must match for batch matrix multiplication: %d != %d\n", a->shape[2], b->shape[1]);
    exit(EXIT_FAILURE);
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  // result shape: [batch_size, a->shape[1], b->shape[2]]
  int* result_shape = (int*)malloc(3 * sizeof(int));
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  result_shape[0] = a->shape[0];
  result_shape[1] = a->shape[1];
  result_shape[2] = b->shape[2];
  size_t result_size = result_shape[0] * result_shape[1] * result_shape[2];

  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  // calculate strides for batch matmul
  int a_strides[3] = {a->shape[1] * a->shape[2], a->shape[2], 1};
  int b_strides[3] = {b->shape[1] * b->shape[2], b->shape[2], 1};

  batch_matmul_array_ops(a_float, b_float, out, a->shape, b->shape, a_strides, b_strides);
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, 3, result_shape, result_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(result_shape);
  return result;
}

Array* broadcasted_matmul_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != 2 || b->ndim != 3) {
    fprintf(stderr, "First array must be 2D and second array must be 3D for broadcasted matrix multiplication\n");
    exit(EXIT_FAILURE);
  }
  if (a->shape[1] != b->shape[1]) {
    fprintf(stderr, "Inner dimensions must match for broadcasted matrix multiplication: %d != %d\n", a->shape[1], b->shape[1]);
    exit(EXIT_FAILURE);
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  // result shape: [b->shape[0], a->shape[0], b->shape[2]]
  int* result_shape = (int*)malloc(3 * sizeof(int));
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  result_shape[0] = b->shape[0];
  result_shape[1] = a->shape[0];
  result_shape[2] = b->shape[2];
  size_t result_size = result_shape[0] * result_shape[1] * result_shape[2];

  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  // calculate strides
  int a_strides[2] = {a->shape[1], 1};
  int b_strides[3] = {b->shape[1] * b->shape[2], b->shape[2], 1};

  broadcasted_matmul_array_ops(a_float, b_float, out, a->shape, b->shape, a_strides, b_strides);
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, 3, result_shape, result_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(result_shape);
  return result;
}

Array* dot_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != 1 || b->ndim != 1) {
    fprintf(stderr, "Both arrays must be 1D for dot product\n");
    exit(EXIT_FAILURE);
  }
  if (a->size != b->size) {
    fprintf(stderr, "Arrays must have the same size for dot product: %zu != %zu\n", a->size, b->size);
    exit(EXIT_FAILURE);
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  // result is a scalar (0D array)
  int* result_shape = (int*)malloc(1 * sizeof(int));
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  result_shape[0] = 1;

  float* out = (float*)malloc(sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  dot_array_ops(a_float, b_float, out, a->size);
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, 0, NULL, 1, result_dtype);  // 0D array for scalar
  free(a_float);
  free(b_float);
  free(out);
  free(result_shape);
  return result;
}

Array* batch_dot_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != 2 || b->ndim != 2) {
    fprintf(stderr, "Both arrays must be 2D for batch dot product\n");
    exit(EXIT_FAILURE);
  }
  if (a->shape[0] != b->shape[0] || a->shape[1] != b->shape[1]) {
    fprintf(stderr, "Arrays must have the same shape for batch dot product\n");
    exit(EXIT_FAILURE);
  }

  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);

  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }

  // result shape: [batch_count]
  int* result_shape = (int*)malloc(1 * sizeof(int));
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  result_shape[0] = a->shape[0];
  size_t result_size = result_shape[0];

  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  batch_dot_array_ops(a_float, b_float, out, a->shape[0], a->shape[1]);
  dtype_t result_dtype = promote_dtypes(a->dtype, b->dtype);
  Array* result = create_array(out, 1, result_shape, result_size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  free(result_shape);
  return result;
}

Array* sin_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  sin_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* sinh_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  sinh_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* cos_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  cos_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* cosh_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  cosh_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* tan_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  tan_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* tanh_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  tanh_ops(a_float, out, a->size);
  // For trigonometric functions, always return float type
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* log_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  log_array_ops(a_float, out, a->size);
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* exp_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  exp_array_ops(a_float, out, a->size);
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* abs_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  abs_array_ops(a_float, out, a->size);
  // If input is integer, promote to float32; if already float, keep same precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keep float32 or float64
  }
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* pow_array(Array* a, float exp) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }

  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }  
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    exit(EXIT_FAILURE);
  }

  pow_array_ops(a_float, exp, out, a->size);
  // for power operations, promote integer types to float
  // keeping existing float precision
  dtype_t result_dtype;
  if (is_integer_dtype(a->dtype) || a->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = a->dtype; // keeping float32 or float64
  }
  
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(out);
  return result;
}

Array* pow_scalar(float a, Array* exp) {
  if (exp == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  float* exp_float = convert_to_float32(exp->data, exp->dtype, exp->size);
  if (exp_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }

  float* out = (float*)malloc(exp->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(exp_float);
    exit(EXIT_FAILURE);
  }
  pow_scalar_ops(a, exp_float, out, exp->size);
  // for power operations, promote integer types to float
  // keeping existing float precision
  dtype_t result_dtype;
  if (is_integer_dtype(exp->dtype) || exp->dtype == DTYPE_BOOL) {
    result_dtype = DTYPE_FLOAT32;
  } else {
    result_dtype = exp->dtype; // keeping float32 or float64
  }
  Array* result = create_array(out, exp->ndim, exp->shape, exp->size, result_dtype);
  free(exp_float);
  free(out);  
  return result;
}

Array* transpose_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }  
  
  int ndim = a->ndim;
  int* result_shape = (int*)malloc(ndim * sizeof(int));
  if (result_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // creating the result shape (reversed dimensions)
  for (int i = 0; i < ndim; i++) {
    result_shape[i] = a->shape[ndim - 1 - i];
  }
  
  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(result_shape);
    exit(EXIT_FAILURE);
  }  
  
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(result_shape);
    exit(EXIT_FAILURE);
  }

  // performing transpose based on dimensions
  // IMPORTANT: passing the ORIGINAL shape to transpose functions, not the result shape
  switch(ndim) {
    case 1:
      transpose_1d_array_ops(a_float, out, a->shape);  // using original shape
      break;
    case 2:
      transpose_2d_array_ops(a_float, out, a->shape);  // using original shape
      break;
    case 3:
      transpose_3d_array_ops(a_float, out, a->shape);  // using original shape
      break;
    default:
    if (ndim > 3) {
      transpose_ndim_array_ops(a_float, out, a->shape, a->ndim);
    } else {
      fprintf(stderr, "Transpose supported only for 1-3 dimensional arrays\n");
      free(a_float);
      free(out);
      free(result_shape);
      exit(EXIT_FAILURE);
    }
  }
  dtype_t result_dtype = a->dtype;
  Array* result = create_array(out, ndim, result_shape, a->size, result_dtype);
  free(a_float);
  free(out);
  free(result_shape);
  return result;
}

Array* reshape_array(Array* a, int* new_shape, int new_ndim) {
  if (a == NULL || new_shape == NULL) {
    fprintf(stderr, "Array or shape pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int* shape = (int*)malloc(new_ndim * sizeof(int));
  if (shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // copying new shape and calculate new size
  size_t new_size = 1;
  for (int i = 0; i < new_ndim; i++) {
    shape[i] = new_shape[i];
    new_size *= shape[i];
  }
  if (new_size != a->size) {
    fprintf(stderr, "Can't reshape the array. array's size doesn't match the target size: %zu != %zu\n", a->size, new_size);
    free(shape);
    exit(EXIT_FAILURE);
  }

  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(shape);
    exit(EXIT_FAILURE);
  }
  // performing reshape (basically just copy data)
  reassign_array_ops(a_float, out, a->size);
  dtype_t result_dtype = a->dtype;    // reshaping preserves the original dtype
  Array* result = create_array(out, new_ndim, shape, a->size, result_dtype);
  free(a_float);
  free(out);
  free(shape);
  return result;
}

Array* equal_array(Array* a, Array* b) {
  if (a == NULL || b == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  if (a->ndim != b->ndim) {
    fprintf(stderr, "arrays must have same dimensions %d and %d for equal\n", a->ndim, b->ndim);
    exit(EXIT_FAILURE);
  }

  // checking if shapes match
  for (size_t i = 0; i < a->ndim; i++) {
    if (a->shape[i] != b->shape[i]) {
      fprintf(stderr, "arrays must have the same shape for comparison\n");
      exit(EXIT_FAILURE);
    }
  }
  // converting both arrays to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  float* b_float = convert_to_float32(b->data, b->dtype, b->size);
  if (a_float == NULL || b_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    if (a_float) free(a_float);
    if (b_float) free(b_float);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(b_float);
    exit(EXIT_FAILURE);
  }
  // perform the equality comparison
  equal_array_ops(a_float, b_float, out, a->size);
  // comparison operations always return boolean type
  dtype_t result_dtype = DTYPE_BOOL;
  Array* result = create_array(out, a->ndim, a->shape, a->size, result_dtype);
  free(a_float);
  free(b_float);
  free(out);
  return result;
}

Array* squeeze_array(Array* a, int axis) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int new_ndim = 0;
  int* temp_shape = (int*)malloc(a->ndim * sizeof(int));
  if (temp_shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // if axis is -1, remove all dimensions of size 1
  if (axis == -1) {
    for (int i = 0; i < a->ndim; i++) {
      if (a->shape[i] != 1) {
        temp_shape[new_ndim] = a->shape[i];
        new_ndim++;
      }
    }
  } else {
    // validate axis
    if (axis < 0 || axis >= a->ndim) {
      fprintf(stderr, "axis %d is out of bounds for array of dimension %zu\n", axis, a->ndim);
      free(temp_shape);
      exit(EXIT_FAILURE);
    }
    if (a->shape[axis] != 1) {
      fprintf(stderr, "cannot select an axis to squeeze out which has size not equal to one\n");
      free(temp_shape);
      exit(EXIT_FAILURE);
    }
    // remove specific axis
    for (int i = 0; i < a->ndim; i++) {
      if (i != axis) {
        temp_shape[new_ndim] = a->shape[i];
        new_ndim++;
      }
    }
  }

  // handling edge case where all dimensions are squeezed out
  if (new_ndim == 0) {
    new_ndim = 1;
    temp_shape[0] = 1;
  }
  int* shape = (int*)malloc(new_ndim * sizeof(int));
  if (shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(temp_shape);
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < new_ndim; i++) {
    shape[i] = temp_shape[i];
  }
  free(temp_shape);
  
  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(shape);
    exit(EXIT_FAILURE);
  }
  reassign_array_ops(a_float, out, a->size);  // performing squeeze (basically just copy data)
  dtype_t result_dtype = a->dtype;  // squeeze preserves the original dtype
  Array* result = create_array(out, new_ndim, shape, a->size, result_dtype);
  free(a_float);
  free(out);
  free(shape);
  return result;
}

Array* expand_dims_array(Array* a, int axis) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  
  int new_ndim = a->ndim + 1;
  if (axis < 0) {
    axis = new_ndim + axis;   // normalizing negative axis
  }
  // validating axis
  if (axis < 0 || axis >= new_ndim) {
    fprintf(stderr, "axis %d is out of bounds for array of dimension %d\n", axis, new_ndim);
    exit(EXIT_FAILURE);
  }
  int* shape = (int*)malloc(new_ndim * sizeof(int));
  if (shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // create new shape with expanded dimension
  int old_idx = 0;
  for (int i = 0; i < new_ndim; i++) {
    if (i == axis) {
      shape[i] = 1;  // insert new dimension of size 1
    } else {
      shape[i] = a->shape[old_idx];
      old_idx++;
    }
  }
  
  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(shape);
    exit(EXIT_FAILURE);
  }
  reassign_array_ops(a_float, out, a->size);   // performing expand_dims (basically just copy data)
  dtype_t result_dtype = a->dtype;  // expand_dims preserves the original dtype
  Array* result = create_array(out, new_ndim, shape, a->size, result_dtype);
  free(a_float);
  free(out);
  free(shape);
  return result;
}

Array* flatten_array(Array* a) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }
  int new_ndim = 1;
  int* shape = (int*)malloc(new_ndim * sizeof(int));
  if (shape == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  shape[0] = a->size;   // flattened array has single dimension with size equal to total elements
  // converting array to float32 for computation
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* out = (float*)malloc(a->size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(a_float);
    free(shape);
    exit(EXIT_FAILURE);
  }

  reassign_array_ops(a_float, out, a->size);  // performing flatten (basically just copy data)
  dtype_t result_dtype = a->dtype;  // flatten preserves the original dtype
  Array* result = create_array(out, new_ndim, shape, a->size, result_dtype);
  free(a_float);
  free(out);
  free(shape);
  return result;
}

Array* sum_array(Array* a, int axis, bool keepdims) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }

  // validate axis
  if (axis != -1 && (axis < 0 || axis >= a->ndim)) {
    fprintf(stderr, "Error: axis %d out of range for array of dimension %zu\n", axis, a->ndim);
    exit(EXIT_FAILURE);
  }

  // calculate output shape and size
  int ndim;
  int* shape;
  size_t out_size;

  if (axis == -1) {
    // global sum - output is scalar (shape [1])
    ndim = 1;
    shape = (int*)malloc(1 * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      exit(EXIT_FAILURE);
    }
    shape[0] = 1;
    out_size = 1;
  } else {
    // axis-specific sum - remove the specified axis
    ndim = a->ndim - 1;
    if (ndim == 0) {
      // if result would be 0-dimensional, make it 1-dimensional with size 1
      ndim = 1;
      shape = (int*)malloc(1 * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      shape[0] = 1;
      out_size = 1;
    } else {
      shape = (int*)malloc(ndim * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      for (int i = 0, j = 0; i < a->ndim; i++) {
        if (i != axis) {
          shape[j++] = a->shape[i];
        }
      }
      out_size = 1;
      for (int i = 0; i < ndim; i++) {
        out_size *= shape[i];
      }
    }
  }
  float* out = (float*)malloc(out_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    free(out);
    exit(EXIT_FAILURE);
  }

  sum_array_ops(a_float, out, a->shape, a->strides, a->size, shape, axis, a->ndim);
  if (keepdims) {
    free(shape);  // free the current shape
    // creating new shape with same number of dimensions as input
    ndim = a->ndim;
    shape = (int*)malloc(ndim * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      free(a_float);
      free(out);
      exit(EXIT_FAILURE);
    }
    if (axis == -1) {
      // all dimensions become 1
      for (int i = 0; i < ndim; i++) {
        shape[i] = 1;
      }
    } else {
      // copying original shape but set axis dimension to 1
      for (int i = 0; i < ndim; i++) {
        if (i == axis) {
          shape[i] = 1;
        } else {
          shape[i] = a->shape[i];
        }
      }
    }
  }

  // create result array
  dtype_t result_dtype = a->dtype;  // preserve original dtype
  Array* result = create_array(out, ndim, shape, out_size, result_dtype);
  free(a_float);
  free(out);
  if (shape) free(shape);
  return result;
}

Array* mean_array(Array* a, int axis, bool keepdims) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }

  // validate axis
  if (axis != -1 && (axis < 0 || axis >= a->ndim)) {
    fprintf(stderr, "Error: axis %d out of range for array of dimension %zu\n", axis, a->ndim);
    exit(EXIT_FAILURE);
  }

  // calculate output shape and size
  int ndim;
  int* shape;
  size_t out_size;

  if (axis == -1) {
    // global sum - output is scalar (shape [1])
    ndim = 1;
    shape = (int*)malloc(1 * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      exit(EXIT_FAILURE);
    }
    shape[0] = 1;
    out_size = 1;
  } else {
    // axis-specific sum - remove the specified axis
    ndim = a->ndim - 1;
    if (ndim == 0) {
      // if result would be 0-dimensional, make it 1-dimensional with size 1
      ndim = 1;
      shape = (int*)malloc(1 * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      shape[0] = 1;
      out_size = 1;
    } else {
      shape = (int*)malloc(ndim * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      for (int i = 0, j = 0; i < a->ndim; i++) {
        if (i != axis) {
          shape[j++] = a->shape[i];
        }
      }
      out_size = 1;
      for (int i = 0; i < ndim; i++) {
        out_size *= shape[i];
      }
    }
  }
  float* out = (float*)malloc(out_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    free(out);
    exit(EXIT_FAILURE);
  }

  mean_array_ops(a_float, out, a->shape, a->strides, a->size, shape, axis, a->ndim);
  if (keepdims) {
    free(shape);  // free the current shape
    // creating new shape with same number of dimensions as input
    ndim = a->ndim;
    shape = (int*)malloc(ndim * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      free(a_float);
      free(out);
      exit(EXIT_FAILURE);
    }
    if (axis == -1) {
      // all dimensions become 1
      for (int i = 0; i < ndim; i++) {
        shape[i] = 1;
      }
    } else {
      // copying original shape but set axis dimension to 1
      for (int i = 0; i < ndim; i++) {
        if (i == axis) {
          shape[i] = 1;
        } else {
          shape[i] = a->shape[i];
        }
      }
    }
  }

  // create result array
  dtype_t result_dtype = a->dtype;  // preserve original dtype
  Array* result = create_array(out, ndim, shape, out_size, result_dtype);
  free(a_float);
  free(out);
  if (shape) free(shape);
  return result;
}

Array* max_array(Array* a, int axis, bool keepdims) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }

  // validate axis
  if (axis != -1 && (axis < 0 || axis >= a->ndim)) {
    fprintf(stderr, "Error: axis %d out of range for array of dimension %zu\n", axis, a->ndim);
    exit(EXIT_FAILURE);
  }

  // calculate output shape and size
  int ndim;
  int* shape;
  size_t out_size;

  if (axis == -1) {
    // global sum - output is scalar (shape [1])
    ndim = 1;
    shape = (int*)malloc(1 * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      exit(EXIT_FAILURE);
    }
    shape[0] = 1;
    out_size = 1;
  } else {
    // axis-specific sum - remove the specified axis
    ndim = a->ndim - 1;
    if (ndim == 0) {
      // if result would be 0-dimensional, make it 1-dimensional with size 1
      ndim = 1;
      shape = (int*)malloc(1 * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      shape[0] = 1;
      out_size = 1;
    } else {
      shape = (int*)malloc(ndim * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      for (int i = 0, j = 0; i < a->ndim; i++) {
        if (i != axis) {
          shape[j++] = a->shape[i];
        }
      }
      out_size = 1;
      for (int i = 0; i < ndim; i++) {
        out_size *= shape[i];
      }
    }
  }
  float* out = (float*)malloc(out_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    free(out);
    exit(EXIT_FAILURE);
  }

  max_array_ops(a_float, out, a->size, a->shape, a->strides, shape, axis, a->ndim);
  if (keepdims) {
    free(shape);  // free the current shape
    // creating new shape with same number of dimensions as input
    ndim = a->ndim;
    shape = (int*)malloc(ndim * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      free(a_float);
      free(out);
      exit(EXIT_FAILURE);
    }
    if (axis == -1) {
      // all dimensions become 1
      for (int i = 0; i < ndim; i++) {
        shape[i] = 1;
      }
    } else {
      // copying original shape but set axis dimension to 1
      for (int i = 0; i < ndim; i++) {
        if (i == axis) {
          shape[i] = 1;
        } else {
          shape[i] = a->shape[i];
        }
      }
    }
  }

  // create result array
  dtype_t result_dtype = a->dtype;  // preserve original dtype
  Array* result = create_array(out, ndim, shape, out_size, result_dtype);
  free(a_float);
  free(out);
  if (shape) free(shape);
  return result;
}

Array* min_array(Array* a, int axis, bool keepdims) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointers are null!\n");
    exit(EXIT_FAILURE);
  }

  // validate axis
  if (axis != -1 && (axis < 0 || axis >= a->ndim)) {
    fprintf(stderr, "Error: axis %d out of range for array of dimension %zu\n", axis, a->ndim);
    exit(EXIT_FAILURE);
  }

  // calculate output shape and size
  int ndim;
  int* shape;
  size_t out_size;

  if (axis == -1) {
    // global sum - output is scalar (shape [1])
    ndim = 1;
    shape = (int*)malloc(1 * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      exit(EXIT_FAILURE);
    }
    shape[0] = 1;
    out_size = 1;
  } else {
    // axis-specific sum - remove the specified axis
    ndim = a->ndim - 1;
    if (ndim == 0) {
      // if result would be 0-dimensional, make it 1-dimensional with size 1
      ndim = 1;
      shape = (int*)malloc(1 * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      shape[0] = 1;
      out_size = 1;
    } else {
      shape = (int*)malloc(ndim * sizeof(int));
      if (shape == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
      }
      for (int i = 0, j = 0; i < a->ndim; i++) {
        if (i != axis) {
          shape[j++] = a->shape[i];
        }
      }
      out_size = 1;
      for (int i = 0; i < ndim; i++) {
        out_size *= shape[i];
      }
    }
  }
  float* out = (float*)malloc(out_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    free(shape);
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    free(shape);
    free(out);
    exit(EXIT_FAILURE);
  }

  min_array_ops(a_float, out, a->size, a->shape, a->strides, shape, axis, a->ndim);
  if (keepdims) {
    free(shape);  // free the current shape
    // creating new shape with same number of dimensions as input
    ndim = a->ndim;
    shape = (int*)malloc(ndim * sizeof(int));
    if (shape == NULL) {
      fprintf(stderr, "Memory allocation failed\n");
      free(a_float);
      free(out);
      exit(EXIT_FAILURE);
    }
    if (axis == -1) {
      // all dimensions become 1
      for (int i = 0; i < ndim; i++) {
        shape[i] = 1;
      }
    } else {
      // copying original shape but set axis dimension to 1
      for (int i = 0; i < ndim; i++) {
        if (i == axis) {
          shape[i] = 1;
        } else {
          shape[i] = a->shape[i];
        }
      }
    }
  }

  // create result array
  dtype_t result_dtype = a->dtype;  // preserve original dtype
  Array* result = create_array(out, ndim, shape, out_size, result_dtype);
  free(a_float);
  free(out);
  free(out);
  if (shape) free(shape);
  return result;
}

Array* var_array(Array* a, int axis, int ddof) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointer is null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }

  // calculate result shape and size
  int* result_shape;
  size_t result_size;
  int result_ndim;
  if (axis == -1) {
    // global variance - scalar result
    result_ndim = 0;  // scalar
    result_shape = NULL;
    result_size = 1;
  } else {
    // axis-specific variance
    if (axis < 0 || axis >= a->ndim) {
      fprintf(stderr, "Invalid axis %d for array with %zu dimensions\n", axis, a->ndim);
      free(a_float);
      exit(EXIT_FAILURE);
    }
    result_ndim = a->ndim - 1;
    result_shape = (int*)malloc(result_ndim * sizeof(int));
    if (result_shape == NULL) {
      fprintf(stderr, "Memory allocation failed for result shape\n");
      free(a_float);
      exit(EXIT_FAILURE);
    }
    // copy shape excluding the axis dimension
    int j = 0;
    result_size = 1;
    for (int i = 0; i < a->ndim; i++) {
      if (i != axis) {
        result_shape[j] = a->shape[i];
        result_size *= a->shape[i];
        j++;
      }
    }
  }
  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed for output\n");
    free(a_float);
    if (result_shape) free(result_shape);
    exit(EXIT_FAILURE);
  }

  var_array_ops(a_float, out, a->size, a->shape, a->strides, result_shape, axis, a->ndim, ddof);
  Array* result;
  if (axis == -1) {
    // for scalar result, create a 1D array with size 1
    int scalar_shape[1] = {1};
    result = create_array(out, 1, scalar_shape, 1, DTYPE_FLOAT32);
  } else {
    result = create_array(out, result_ndim, result_shape, result_size, DTYPE_FLOAT32);
  }

  free(a_float);
  free(out);
  if (result_shape) free(result_shape);
  return result;
}

Array* std_array(Array* a, int axis, int ddof) {
  if (a == NULL) {
    fprintf(stderr, "Array value pointer is null!\n");
    exit(EXIT_FAILURE);
  }
  float* a_float = convert_to_float32(a->data, a->dtype, a->size);
  if (a_float == NULL) {
    fprintf(stderr, "Memory allocation failed during dtype conversion\n");
    exit(EXIT_FAILURE);
  }

  // calculate result shape and size
  int* result_shape;
  size_t result_size;
  int result_ndim;
  if (axis == -1) {
    // global standard deviation - scalar result
    result_ndim = 0;  // scalar
    result_shape = NULL;
    result_size = 1;
  } else {
    // axis-specific standard deviation
    if (axis < 0 || axis >= a->ndim) {
      fprintf(stderr, "Invalid axis %d for array with %zu dimensions\n", axis, a->ndim);
      free(a_float);
      exit(EXIT_FAILURE);
    }
    
    result_ndim = a->ndim - 1;
    result_shape = (int*)malloc(result_ndim * sizeof(int));
    if (result_shape == NULL) {
      fprintf(stderr, "Memory allocation failed for result shape\n");
      free(a_float);
      exit(EXIT_FAILURE);
    }
    int j = 0;
    result_size = 1;
    for (int i = 0; i < a->ndim; i++) {
      if (i != axis) {
        result_shape[j] = a->shape[i];
        result_size *= a->shape[i];
        j++;
      }
    }
  }
  float* out = (float*)malloc(result_size * sizeof(float));
  if (out == NULL) {
    fprintf(stderr, "Memory allocation failed for output\n");
    free(a_float);
    if (result_shape) free(result_shape);
    exit(EXIT_FAILURE);
  }

  std_array_ops(a_float, out, a->size, a->shape, a->strides, result_shape, axis, a->ndim, ddof);
  Array* result;
  if (axis == -1) {
    // for scalar result, create a 1D array with size 1
    int scalar_shape[1] = {1};
    result = create_array(out, 1, scalar_shape, 1, DTYPE_FLOAT32);
  } else {
    result = create_array(out, result_ndim, result_shape, result_size, DTYPE_FLOAT32);
  }

  free(a_float);
  free(out);
  if (result_shape) free(result_shape);
  return result;
}