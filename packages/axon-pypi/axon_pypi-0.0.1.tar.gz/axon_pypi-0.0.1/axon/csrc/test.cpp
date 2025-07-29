// compile with:
// *- g++ -o run test.cpp array.cpp core/core.cpp core/dtype.cpp cpu/maths_ops.cpp cpu/utils.cpp cpu/helpers.cpp cpu/red_ops.cpp

#include <stdio.h>
#include <stdlib.h>
#include "array.h"

int main() {
  int* shape = (int*)malloc(2 * sizeof(int));
  shape[0] = 2;
  shape[1] = 3;
  size_t size = 6;
  size_t ndim = 2;

  // Create two arrays with values
  float* data1 = (float*)malloc(size * sizeof(float));
  float* data2 = (float*)malloc(size * sizeof(float));
  for (int i = 0; i < size; i++) {
    data1[i] = i + 1;
    data2[i] = (i + 1) * 2;
  }

  Array* a = create_array(data1, ndim, shape, size, DTYPE_INT8);
  Array* b = create_array(data2, ndim, shape, size, DTYPE_INT8);

  // Print original arrays
  printf("Original Arrays:\n");
  print_array(a);
  print_array(b);

  // Perform elementwise addition
  Array* c = add_array(a, b);
  printf("\nAddition:\n");
  print_array(c);

  // Multiply result with scalar
  Array* d = mul_scalar_array(c, 0.5f);
  printf("\nScalar Multiplication (0.5):\n");
  print_array(d);

  // Reshape the array
  int* new_shape = (int*)malloc(2 * sizeof(int));
  new_shape[0] = 3;
  new_shape[1] = 2;
  Array* reshaped = reshape_array(d, new_shape, 2);
  printf("\nReshaped (3, 2):\n");
  print_array(reshaped);

  // Apply a trig operation
  Array* s = sin_array(d);
  printf("\nSin of elements:\n");
  print_array(s);

  // Create random arrays
  Array* r1 = randn_array(shape, size, ndim, DTYPE_FLOAT64);
  Array* r2 = randint_array(-5, 5, shape, size, ndim, DTYPE_INT16);
  printf("\nRandom Normal:\n");
  print_array(r1);
  printf("\nRandom Integers (-5 to 5):\n");
  print_array(r2);

  // Flatten and then squeeze
  Array* flat = flatten_array(d);
  printf("\nFlattened:\n");
  print_array(flat);

  // Clean up
  delete_array(a);
  delete_array(b);
  delete_array(c);
  delete_array(d);
  delete_array(reshaped);
  delete_array(s);
  delete_array(r1);
  delete_array(r2);
  delete_array(flat);
  free(shape);
  free(new_shape);
  free(data1);
  free(data2);

  return 0;
}