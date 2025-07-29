import ctypes, os
from ctypes import Structure, c_float, c_double, c_int, c_int8, c_int16, c_int32, c_int64, c_uint8, c_uint16, c_uint32, c_uint64, c_size_t, c_void_p, c_char_p, POINTER
from typing import *

lib_path = os.path.join(os.path.dirname(__file__), 'lib/libarray.so')
lib = ctypes.CDLL(lib_path)

# dtype enumeration
class DType:
  FLOAT32 = 0
  FLOAT64 = 1
  INT8 = 2
  INT16 = 3
  INT32 = 4
  INT64 = 5
  UINT8 = 6
  UINT16 = 7
  UINT32 = 8
  UINT64 = 9
  BOOL = 10

# dtype union
class DTypeValue(ctypes.Union):
  _fields_ = [
    ("f32", c_float),
    ("f64", c_double),
    ("i8", c_int8),
    ("i16", c_int16),
    ("i32", c_int32),
    ("i64", c_int64),
    ("u8", c_uint8),
    ("u16", c_uint16),
    ("u32", c_uint32),
    ("u64", c_uint64),
    ("boolean", c_uint8),
  ]

class CArray(Structure):
  pass

CArray._fields_ = [
  ("data", c_void_p),
  ("strides", POINTER(c_int)),
  ("backstrides", POINTER(c_int)),
  ("shape", POINTER(c_int)),
  ("size", c_size_t),
  ("ndim", c_size_t),
  ("dtype", c_int),
  ("is_view", c_int),
]

# core array functions
lib.create_array.argtypes = [POINTER(c_float), c_size_t, POINTER(c_int), c_size_t, c_int]
lib.create_array.restype = POINTER(CArray)
lib.delete_array.argtypes = [POINTER(CArray)]
lib.delete_array.restype = None
lib.delete_data.argtypes = [POINTER(CArray)]
lib.delete_data.restype = None
lib.delete_shape.argtypes = [POINTER(CArray)]
lib.delete_shape.restype = None
lib.delete_strides.argtypes = [POINTER(CArray)]
lib.delete_strides.restype = None
lib.print_array.argtypes = [POINTER(CArray)]
lib.print_array.restype = None
lib.out_data.argtypes = [POINTER(CArray)]
lib.out_data.restype = POINTER(c_float)
lib.out_shape.argtypes = [POINTER(CArray)]
lib.out_shape.restype = POINTER(c_int)
lib.out_strides.argtypes = [POINTER(CArray)]
lib.out_strides.restype = POINTER(c_int)
lib.out_size.argtypes = [POINTER(CArray)]
lib.out_size.restype = c_int

# contiguous ops
lib.contiguous_array.argtypes = [POINTER(CArray)]
lib.contiguous_array.restype = POINTER(CArray)
lib.is_contiguous_array.argtypes = [POINTER(CArray)]
lib.is_contiguous_array.restype = POINTER(CArray)
lib.make_contiguous_inplace_array.argtypes = [POINTER(CArray)]
lib.make_contiguous_inplace_array.restype = POINTER(CArray)
lib.view_array.argtypes = [POINTER(CArray)]
lib.view_array.restype = POINTER(CArray)
lib.is_view_array.argtypes = [POINTER(CArray)]
lib.is_view_array.restype = POINTER(CArray)

# dtype casting functions
lib.cast_array.argtypes = [POINTER(CArray), c_int]
lib.cast_array.restype = POINTER(CArray)
lib.cast_array_simple.argtypes = [POINTER(CArray), c_int]
lib.cast_array_simple.restype = POINTER(CArray)

# dtype utility functions
lib.get_dtype_size.argtypes = [c_int]
lib.get_dtype_size.restype = c_size_t
lib.get_dtype_name.argtypes = [c_int]
lib.get_dtype_name.restype = c_char_p
lib.dtype_to_float32.argtypes = [c_void_p, c_int, c_size_t]
lib.dtype_to_float32.restype = c_float
lib.float32_to_dtype.argtypes = [c_float, c_void_p, c_int, c_size_t]
lib.float32_to_dtype.restype = None
lib.convert_to_float32.argtypes = [c_void_p, c_int, c_size_t]
lib.convert_to_float32.restype = POINTER(c_float)
lib.convert_from_float32.argtypes = [POINTER(c_float), c_void_p, c_int, c_size_t]
lib.convert_from_float32.restype = None
lib.allocate_dtype_array.argtypes = [c_int, c_size_t]
lib.allocate_dtype_array.restype = c_void_p
lib.copy_with_dtype_conversion.argtypes = [c_void_p, c_int, c_void_p, c_int, c_size_t]
lib.copy_with_dtype_conversion.restype = None
lib.cast_array_dtype.argtypes = [c_void_p, c_int, c_int, c_size_t]
lib.cast_array_dtype.restype = c_void_p

# dtype helper functions
lib.is_integer_dtype.argtypes = [c_int]
lib.is_integer_dtype.restype = c_int
lib.is_float_dtype.argtypes = [c_int]
lib.is_float_dtype.restype = c_int
lib.is_unsigned_dtype.argtypes = [c_int]
lib.is_unsigned_dtype.restype = c_int
lib.is_signed_dtype.argtypes = [c_int]
lib.is_signed_dtype.restype = c_int
lib.clamp_to_int_range.argtypes = [c_double, c_int]
lib.clamp_to_int_range.restype = c_int64
lib.clamp_to_uint_range.argtypes = [c_double, c_int]
lib.clamp_to_uint_range.restype = c_uint64
lib.get_dtype_priority.argtypes = [c_int]
lib.get_dtype_priority.restype = c_int
lib.promote_dtypes.argtypes = [c_int, c_int]
lib.promote_dtypes.restype = c_int

# maths ops ----
lib.add_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.add_array.restype = POINTER(CArray)
lib.add_scalar_array.argtypes = [POINTER(CArray), c_float]
lib.add_scalar_array.restype = POINTER(CArray)
lib.add_broadcasted_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.add_broadcasted_array.restype = POINTER(CArray)
lib.sub_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.sub_array.restype = POINTER(CArray)
lib.sub_scalar_array.argtypes = [POINTER(CArray), c_float]
lib.sub_scalar_array.restype = POINTER(CArray)
lib.sub_broadcasted_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.sub_broadcasted_array.restype = POINTER(CArray)
lib.mul_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.mul_array.restype = POINTER(CArray)
lib.mul_scalar_array.argtypes = [POINTER(CArray), c_float]
lib.mul_scalar_array.restype = POINTER(CArray)
lib.mul_broadcasted_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.mul_broadcasted_array.restype = POINTER(CArray)
lib.div_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.div_array.restype = POINTER(CArray)
lib.div_scalar_array.argtypes = [POINTER(CArray), c_float]
lib.div_scalar_array.restype = POINTER(CArray)
lib.div_broadcasted_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.div_broadcasted_array.restype = POINTER(CArray)
lib.pow_array.argtypes = [POINTER(CArray), c_float]
lib.pow_array.restype = POINTER(CArray)
lib.pow_scalar.argtypes = [c_float, POINTER(CArray)]
lib.pow_scalar.restype = POINTER(CArray)
lib.log_array.argtypes = [POINTER(CArray)]
lib.log_array.restype = POINTER(CArray)
lib.exp_array.argtypes = [POINTER(CArray)]
lib.exp_array.restype = POINTER(CArray)
lib.abs_array.argtypes = [POINTER(CArray)]
lib.abs_array.restype = POINTER(CArray)
lib.matmul_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.matmul_array.restype = POINTER(CArray)
lib.batch_matmul_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.batch_matmul_array.restype = POINTER(CArray)
lib.broadcasted_matmul_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.broadcasted_matmul_array.restype = POINTER(CArray)

lib.sin_array.argtypes = [POINTER(CArray)]
lib.sin_array.restype = POINTER(CArray)
lib.sinh_array.argtypes = [POINTER(CArray)]
lib.sinh_array.restype = POINTER(CArray)
lib.cos_array.argtypes = [POINTER(CArray)]
lib.cos_array.restype = POINTER(CArray)
lib.cosh_array.argtypes = [POINTER(CArray)]
lib.cosh_array.restype = POINTER(CArray)
lib.tan_array.argtypes = [POINTER(CArray)]
lib.tan_array.restype = POINTER(CArray)
lib.tanh_array.argtypes = [POINTER(CArray)]
lib.tanh_array.restype = POINTER(CArray)

lib.transpose_array.argtypes = [POINTER(CArray)]
lib.transpose_array.restype = POINTER(CArray)
lib.equal_array.argtypes = [POINTER(CArray), POINTER(CArray)]
lib.equal_array.restype = POINTER(CArray)
lib.reshape_array.argtypes = [POINTER(CArray), POINTER(c_int), c_int]
lib.reshape_array.restype = POINTER(CArray)
lib.squeeze_array.argtypes = [POINTER(CArray), c_int]
lib.squeeze_array.restype = POINTER(CArray)
lib.expand_dims_array.argtypes = [POINTER(CArray), c_int]
lib.expand_dims_array.restype = POINTER(CArray)
lib.flatten_array.argtypes = [POINTER(CArray)]
lib.flatten_array.restype = POINTER(CArray)

lib.sum_array.argtypes = [POINTER(CArray), c_int, ctypes.c_bool]
lib.sum_array.restype = POINTER(CArray)
lib.min_array.argtypes = [POINTER(CArray), c_int, ctypes.c_bool]
lib.min_array.restype = POINTER(CArray)
lib.max_array.argtypes = [POINTER(CArray), c_int, ctypes.c_bool]
lib.max_array.restype = POINTER(CArray)
lib.mean_array.argtypes = [POINTER(CArray), c_int, ctypes.c_bool]
lib.mean_array.restype = POINTER(CArray)
lib.var_array.argtypes = [POINTER(CArray), c_int, c_int]
lib.var_array.restype = POINTER(CArray)
lib.std_array.argtypes = [POINTER(CArray), c_int, c_int]
lib.std_array.restype = POINTER(CArray)

# utils functions ---
lib.zeros_like_array.argtypes = [POINTER(CArray)]
lib.zeros_like_array.restype = POINTER(CArray)
lib.ones_like_array.argtypes = [POINTER(CArray)]
lib.ones_like_array.restype = POINTER(CArray)
lib.zeros_array.argtypes = [POINTER(c_int), c_size_t, c_size_t, c_int]
lib.zeros_array.restype = POINTER(CArray)
lib.ones_array.argtypes = [POINTER(c_int), c_size_t, c_size_t, c_int]
lib.ones_array.restype = POINTER(CArray)
lib.randn_array.argtypes = [POINTER(c_int), c_size_t, c_size_t, c_int]
lib.randn_array.restype = POINTER(CArray)
lib.randint_array.argtypes = [c_int, c_int, POINTER(c_int), c_size_t, c_size_t, c_int]
lib.randint_array.restype = POINTER(CArray)
lib.uniform_array.argtypes = [c_int, c_int, POINTER(c_int), c_size_t, c_size_t, c_int]
lib.uniform_array.restype = POINTER(CArray)
lib.fill_array.argtypes = [c_float, POINTER(c_int), c_size_t, c_size_t, c_int]
lib.fill_array.restype = POINTER(CArray)
lib.linspace_array.argtypes = [c_float, c_float, c_float, POINTER(c_int), c_size_t, c_size_t, c_int]
lib.linspace_array.restype = POINTER(CArray)