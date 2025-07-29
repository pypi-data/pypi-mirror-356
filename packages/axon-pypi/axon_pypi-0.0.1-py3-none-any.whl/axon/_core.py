from ctypes import c_float, c_size_t, c_int
from typing import *

from ._cbase import CArray, lib, DType
from .helpers.shape import get_shape, flatten, get_strides, transposed_shape, reshape_list

int8, int16, int32, int64, long = "int8", "int16", "int32", "int64", "long"
float32, float64, double = "float32", "float64", "double"
uint8, uint16, uint32, uint64 = "uint8", "uint16", "uint32", "uint64"
boolean = "bool"

class array:
  int8, int16, int32, int64, long, float32, float64, double, uint8, uint16, uint32, uint64, boolean = int8, int16, int32, int64, long, float32, float64, double, uint8, uint16, uint32, uint64, boolean
  def __init__(self, data: Union[List[Any], int, float], dtype: str = "float32") -> None:
    """
    Initialize a new array instance with the given data and dtype.

    Parameters:
    -----------
    data : list, int, float
        Input data for the array. Can be a nested list or scalar.
    dtype : str, optional
        The data type of the array (default is 'float32').

    Returns:
    --------
    None
    """
    self.dtype = self._parse_dtype(dtype)
    
    if isinstance(data, (CArray, array)):
      self.data, self.shape = data, []
      self.size, self.ndim, self._raw_value, self.strides = 0, 0, None, 0      
    else:
      flat, shape = flatten(data), get_shape(data)
      size, ndim = len(flat), len(shape)

      self._float_arr = (c_float * size)(*flat)
      self._shape_arr = (c_int * ndim)(*shape)

      self.data = lib.create_array(self._float_arr, c_size_t(ndim), self._shape_arr, c_size_t(size), c_int(self.dtype))
      self.shape, self.size, self.ndim, self._raw_value, self.strides = tuple(shape), size, ndim, data, get_strides(shape)

  def _parse_dtype(self, dtype: str) -> int:
    """
    Parse a string-based dtype into the internal integer enum representation.

    Parameters:
    -----------
    dtype : str
        Data type string (e.g., 'float32', 'int64').

    Returns:
    --------
    int : internal enum ID for the dtype
    """
    dtype_map = {
      "float32": DType.FLOAT32,
      "float64": DType.FLOAT64,
      "int8": DType.INT8,
      "int16": DType.INT16,
      "int32": DType.INT32,
      "int64": DType.INT64,
      "uint8": DType.UINT8,
      "uint16": DType.UINT16,
      "uint32": DType.UINT32,
      "uint64": DType.UINT64,
      "bool": DType.BOOL,
    }
    if dtype not in dtype_map:
      raise ValueError(f"Unsupported dtype: {dtype}. Supported dtypes: {list(dtype_map.keys())}")
    return dtype_map[dtype]

  def _get_dtype_name(self) -> str:
    """
    Get the string name of the current internal dtype.

    Returns:
    --------
    str : name of the dtype (e.g., 'float32')
    """
    dtype_names = {
      DType.FLOAT32: "float32",
      DType.FLOAT64: "float64",
      DType.INT8: "int8",
      DType.INT16: "int16",
      DType.INT32: "int32",
      DType.INT64: "int64",
      DType.UINT8: "uint8",
      DType.UINT16: "uint16",
      DType.UINT32: "uint32",
      DType.UINT64: "uint64",
      DType.BOOL: "bool",
    }
    return dtype_names.get(self.dtype, "unknown")

  def __repr__(self) -> str:
    """
    Official string representation of the array object.

    Returns:
    --------
    str : repr-style output displaying original data and dtype.
    """
    return f"array({self._raw_value}, dtype={self._get_dtype_name()})"

  def __str__(self) -> str:
    """
    User-friendly string version showing formatted array contents.

    Returns:
    --------
    str : An empty string (actual printing is done through C backend).
    """
    lib.print_array(self.data)
    return ""

  def astype(self, dtype: str) -> "array":
    """
    Convert array to a new dtype.

    Parameters:
    -----------
    dtype : str
        Target data type string (e.g., 'int32').

    Returns:
    --------
    array : A new array object casted to the specified dtype.
    """
    new_dtype = self._parse_dtype(dtype)
    result_ptr = lib.cast_array(self.data, c_int(new_dtype)).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = new_dtype
    return out

  def is_contiguous(self) -> bool:
    """
    Check if the array is contiguous in memory.

    Returns:
    --------
    bool : True if array is contiguous, False otherwise.
    """
    return bool(lib.is_contiguous_array(self.data))

  def contiguous(self) -> "array":
    """
    Return a contiguous copy of the array.

    Returns:
    --------
    array : A new contiguous array with the same data.
    """
    result_ptr = lib.contiguous_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def make_contiguous(self) -> None:
    """
    Make the array contiguous in-place (modifies the current array).

    Returns:
    --------
    None
    """
    lib.make_contiguous_inplace_array(self.data)
    # updating strides since they may have changed
    self.strides = get_strides(self.shape)

  def view(self) -> "array":
    """
    Create a view of the array.

    Returns:
    --------
    array : A view of the current array.
    """
    result_ptr = lib.view_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def is_view(self) -> bool:
    """
    Check if the array is a view of another array.

    Returns:
    --------
    bool : True if array is a view, False otherwise.
    """
    return bool(lib.is_view_array(self.data))

  def __add__(self, other) -> "array":
    """
    Elementwise addition of self and another array or scalar.

    Parameters:
    -----------
    other : array, int, or float
        Right-hand operand for the addition.

    Returns:
    --------
    array : Result of elementwise addition.
    """
    if isinstance(other, (int, float)):
      result_ptr = lib.add_scalar_array(self.data, c_float(other)).contents
    else:
      other = other if isinstance(other, (CArray, array)) else array(other)
      result_ptr = lib.add_array(self.data, other.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def __radd__(self, other) -> "array":
    """
    Right-hand addition to support scalar + array.

    Parameters:
    -----------
    other : int or float

    Returns:
    --------
    array : Result of elementwise addition.
    """
    return self + other

  def __sub__(self, other) -> "array":
    """
    Elementwise subtraction of another array or scalar from self.

    Parameters:
    -----------
    other : array, int, or float
        Right-hand operand for subtraction.

    Returns:
    --------
    array : Result of elementwise subtraction.
    """
    if isinstance(other, (int, float)):
      result_ptr = lib.sub_scalar_array(self.data, c_float(other)).contents
    else:
      other = other if isinstance(other, (CArray, array)) else array(other)
      result_ptr = lib.sub_array(self.data, other.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def __rsub__(self, other) -> "array":
    """
    Right-hand subtraction to support scalar - array.

    Parameters:
    -----------
    other : int or float

    Returns:
    --------
    array : Result of reversed subtraction.
    """
    return other - self

  def __mul__(self, other) -> "array":
    """
    Elementwise multiplication of self with another array or scalar.

    Parameters:
    -----------
    other : array, int, or float
        Right-hand operand for multiplication.

    Returns:
    --------
    array : Result of elementwise multiplication.
    """
    if isinstance(other, (int, float)):
      result_ptr = lib.mul_scalar_array(self.data, c_float(other)).contents
    else:
      other = other if isinstance(other, (CArray, array)) else array(other)
      result_ptr = lib.mul_array(self.data, other.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def __rmul__(self, other) -> "array":
    """
    Right-hand multiplication to support scalar * array.

    Parameters:
    -----------
    other : int or float

    Returns:
    --------
    array : Result of elementwise multiplication.
    """
    return self * other

  def __truediv__(self, other) -> "array":
    """
    Elementwise division of self by another array or scalar.

    Parameters:
    -----------
    other : array, int, or float
        Right-hand operand for division.

    Returns:
    --------
    array : Result of elementwise division.
    """
    if isinstance(other, (int, float)):
      result_ptr = lib.div_scalar_array(self.data, c_float(other)).contents
    else:
      other = other if isinstance(other, (CArray, array)) else array(other)
      result_ptr = lib.div_array(self.data, other.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def __rtruediv__(self, other) -> "array":
    """
    Right-hand division to support scalar / array.

    Parameters:
    -----------
    other : int or float
        Left-hand operand for division.

    Returns:
    --------
    array : Result of reversed elementwise division.
    """
    return (self / other) ** -1

  def __pow__(self, exp) -> "array":
    """
    Elementwise power of self to another array or scalar.

    Parameters:
    -----------
    other : array, int, or float
        Exponent to raise each element.

    Returns:
    --------
    array : Result of exponentiation.
    """
    if isinstance(exp, (int, float)):
      result_ptr = lib.pow_array(self.data, c_float(exp)).contents
    else:
      pass
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def __rpow__(self, base) -> "array":
    """
    Right-hand power to support scalar ** array.

    Parameters:
    -----------
    base : int or float
        Base value for exponentiation.

    Returns:
    --------
    array : Result of reversed exponentiation.
    """
    if isinstance(base, (int, float)):
      result_ptr = lib.pow_scalar(c_float(base), self.data).contents
      out = array(result_ptr)
      out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
      out.dtype = self.dtype
      return out
    else:
      raise NotImplementedError("__rpow__ with array base not implemented yet")

  def __eq__(self, other) -> "array":
    """Element-wise equality comparison"""
    if isinstance(other, (int, float)):
      # For scalar comparison, create a scalar array first
      other = array([other], dtype=self._get_dtype_name())
    else:
      other = other if isinstance(other, (CArray, array)) else array(other)
    
    result_ptr = lib.equal_array(self.data, other.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = DType.BOOL
    return out

  def log(self) -> "array":
    """
    Compute the natural logarithm of the array.

    Returns:
    --------
    array : Array with natural logarithm of each element.
    """
    result_ptr = lib.log_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def exp(self) -> "array":
    """
    Compute the exponential of the array.

    Returns:
    --------
    array : Array with exponential of each element.
    """
    result_ptr = lib.exp_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def abs(self) -> "array":
    """
    Compute the absolute value of the array.

    Returns:
    --------
    array : Array with absolute value of each element.
    """
    result_ptr = lib.abs_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def _matmul(self, other) -> "array":
    """
    Matrix multiplication with optimized shape handling.
    Parameters:
    -----------
    other : array
        Right-hand operand for matrix multiplication.
    
    Returns:
    --------
    array : Result of matrix multiplication.
    """
    other = other if isinstance(other, (CArray, array)) else array(other)

    # using the appropriate C function based on dimensions
    if self.ndim <= 2 and other.ndim <= 2:
      result_ptr = lib.matmul_array(self.data, other.data).contents
    elif self.ndim == 3 and other.ndim == 3 and self.shape[0] == other.shape[0]:
      result_ptr = lib.batch_matmul_array(self.data, other.data).contents
    else:
      result_ptr = lib.broadcasted_matmul_array(self.data, other.data).contents

    # creating output array and let C backend handle shape calculation
    out = array(result_ptr)
    # getting actual shape from C backend instead of calculating in Python
    shape_ptr = lib.out_shape(out.data)
    size = lib.out_size(out.data)
    ndim = out.data.ndim

    out.shape = tuple(shape_ptr[i] for i in range(ndim))
    out.size, out.ndim, out.dtype = size, ndim, self.dtype
    out.strides = get_strides(out.shape)
    return out

  def __matmul__(self, other) -> "array":
    """Matrix multiplication operator (@)."""
    return self._matmul(other)

  def to_list(self) -> List[Any]:
    """
    Convert array to Python list.

    Returns:
    --------
    list : Python list representation of the array.
    """
    data_ptr = lib.out_data(self.data)
    data_array = [data_ptr[i] for i in range(self.size)]

    if self.ndim == 0:
      return data_array[0]
    elif self.ndim == 1:
      return data_array
    else:
      return reshape_list(data_array, self.shape)

  def sin(self) -> "array":
    """
    Compute the elementwise sine of the array.

    Returns:
    --------
    array : Array with sine of each element.
    """
    result_ptr = lib.sin_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def cos(self) -> "array":
    """
    Compute the elementwise cosine of the array.

    Returns:
    --------
    array : Array with cosine of each element.
    """
    result_ptr = lib.cos_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def tan(self) -> "array":
    """
    Compute the elementwise tangent of the array.

    Returns:
    --------
    array : Array with tangent of each element.
    """
    result_ptr = lib.tan_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def sinh(self) -> "array":
    """
    Compute the elementwise hyperbolic sine of the array.

    Returns:
    --------
    array : Array with hyperbolic sine of each element.
    """
    result_ptr = lib.sinh_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def cosh(self) -> "array":
    """
    Compute the elementwise hyperbolic cosine of the array.

    Returns:
    --------
    array : Array with hyperbolic cosine of each element.
    """
    result_ptr = lib.cosh_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def tanh(self) -> "array":
    """
    Compute the elementwise hyperbolic tangent of the array.

    Returns:
    --------
    array : Array with hyperbolic tangent of each element.
    """
    result_ptr = lib.tanh_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim, out.strides = self.shape, self.size, self.ndim, self.strides
    out.dtype = self.dtype
    return out

  def transpose(self) -> "array":
    assert self.ndim <= 3, ".transpose() only supported till 3-d arrays"
    result_ptr = lib.transpose_array(self.data).contents
    out = array(result_ptr)
    out.shape, out.size, out.ndim = transposed_shape(self.shape), self.size, self.ndim
    out.strides = get_strides(out.shape)
    out.dtype = self.dtype
    return out

  def reshape(self, new_shape: Union[List[int], Tuple[int]]) -> "array":
    if isinstance(new_shape, tuple):
      new_shape = list(new_shape)
    new_size = 1
    for dim in new_shape:
      new_size *= dim

    if new_size != self.size:
      raise ValueError(f"Cannot reshape array of size {self.size} into shape {new_shape}")

    ndim = len(new_shape)
    shape_arr = (c_int * ndim)(*new_shape)
    result_ptr = lib.reshape_array(self.data, shape_arr, c_int(ndim)).contents

    out = array(result_ptr)
    out.shape, out.size, out.ndim = tuple(new_shape), self.size, ndim
    out.strides = get_strides(new_shape)
    out.dtype = self.dtype
    return out

  def squeeze(self, axis: int = -1) -> "array":
    """Remove single-dimensional entries from the shape of an array"""
    result_ptr = lib.squeeze_array(self.data, c_int(axis)).contents
    out = array(result_ptr)
    
    if axis == -1:
      # Remove all dimensions of size 1
      new_shape = [dim for dim in self.shape if dim != 1]
    else:
      # Remove specific axis if it has size 1
      if self.shape[axis] != 1:
        raise ValueError(f"Cannot squeeze axis {axis} with size {self.shape[axis]}")
      new_shape = list(self.shape)
      new_shape.pop(axis)
    
    out.shape = tuple(new_shape) if new_shape else (1,)
    out.size = self.size
    out.ndim = len(out.shape)
    out.strides = get_strides(out.shape)
    out.dtype = self.dtype
    return out

  def expand_dims(self, axis: int) -> "array":
    """Expand the shape of an array by inserting a new axis"""
    result_ptr = lib.expand_dims_array(self.data, c_int(axis)).contents
    out = array(result_ptr)
    
    new_shape = list(self.shape)
    if axis < 0:
      axis = len(new_shape) + axis + 1
    new_shape.insert(axis, 1)
    
    out.shape = tuple(new_shape)
    out.size = self.size
    out.ndim = len(new_shape)
    out.strides = get_strides(new_shape)
    out.dtype = self.dtype
    return out

  def flatten(self) -> "array":
    """Return a copy of the array collapsed into one dimension"""
    result_ptr = lib.flatten_array(self.data).contents
    out = array(result_ptr)
    out.shape = (self.size,)
    out.size = self.size
    out.ndim = 1
    out.strides = get_strides(out.shape)
    out.dtype = self.dtype
    return out

  def sum(self, axis: int = -1, keepdims: bool = False) -> "array":
    """
    Sum of array elements over a given axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which a sum is performed. Default is -1 (all elements).
    keepdims : bool, optional
        If True, the axes which are reduced are left as dimensions with size one.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    import ctypes
    result_ptr = lib.sum_array(self.data, c_int(axis), ctypes.c_bool(keepdims)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Sum all elements
      out.shape, out.size, out.ndim = (1,) if keepdims else (), 1, 1 if keepdims else 0
    else:
      new_shape = list(self.shape)
      if keepdims:
        new_shape[axis] = 1
      else:
        new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out

  def mean(self, axis: int = -1, keepdims: bool = False) -> "array":
    """
    Compute the arithmetic mean along the specified axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which the mean is computed. Default is -1 (all elements).
    keepdims : bool, optional
        If True, the axes which are reduced are left as dimensions with size one.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    import ctypes
    result_ptr = lib.mean_array(self.data, c_int(axis), ctypes.c_bool(keepdims)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Mean of all elements
      out.shape, out.size, out.ndim = (1,) if keepdims else (), 1, 1 if keepdims else 0
    else:
      new_shape = list(self.shape)
      if keepdims:
        new_shape[axis] = 1
      else:
        new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out

  def max(self, axis: int = -1, keepdims: bool = False) -> "array":
    """
    Return the maximum of an array or maximum along an axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which to operate. Default is -1 (all elements).
    keepdims : bool, optional
        If True, the axes which are reduced are left as dimensions with size one.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    import ctypes
    result_ptr = lib.max_array(self.data, c_int(axis), ctypes.c_bool(keepdims)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Max of all elements
      out.shape, out.size, out.ndim = (1,) if keepdims else (), 1, 1 if keepdims else 0
    else:
      new_shape = list(self.shape)
      if keepdims:
        new_shape[axis] = 1
      else:
        new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out

  def min(self, axis: int = -1, keepdims: bool = False) -> "array":
    """
    Return the minimum of an array or minimum along an axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which to operate. Default is -1 (all elements).
    keepdims : bool, optional
        If True, the axes which are reduced are left as dimensions with size one.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    import ctypes
    result_ptr = lib.min_array(self.data, c_int(axis), ctypes.c_bool(keepdims)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Min of all elements
      out.shape, out.size, out.ndim = (1,) if keepdims else (), 1, 1 if keepdims else 0
    else:
      new_shape = list(self.shape)
      if keepdims:
        new_shape[axis] = 1
      else:
        new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out

  def var(self, axis: int = -1, ddof: int = 0) -> "array":
    """
    Compute the variance along the specified axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which the variance is computed. Default is -1 (all elements).
    ddof : int, optional
        Delta Degrees of Freedom: the divisor used in calculation is N - ddof.
        Default is 0.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    result_ptr = lib.var_array(self.data, c_int(axis), c_int(ddof)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Variance of all elements
      out.shape, out.size, out.ndim = (), 1, 0
    else:
      new_shape = list(self.shape)
      new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out

  def std(self, axis: int = -1, ddof: int = 0) -> "array":
    """
    Compute the standard deviation along the specified axis.
    
    Parameters:
    -----------
    axis : int, optional
        Axis along which the standard deviation is computed. Default is -1 (all elements).
    ddof : int, optional
        Delta Degrees of Freedom: the divisor used in calculation is N - ddof.
        Default is 0.
    
    Returns:
    --------
    array : Array with the same shape as self, with the specified axis removed.
    """
    result_ptr = lib.std_array(self.data, c_int(axis), c_int(ddof)).contents
    out = array(result_ptr)
    
    if axis == -1:  # Standard deviation of all elements
      out.shape, out.size, out.ndim = (), 1, 0
    else:
      new_shape = list(self.shape)
      new_shape.pop(axis)
      out.shape = tuple(new_shape)
      out.size = 1 if not new_shape else eval('*'.join(map(str, new_shape)))
      out.ndim = len(new_shape)
    
    out.strides = get_strides(out.shape) if out.shape else []
    out.dtype = self.dtype
    return out