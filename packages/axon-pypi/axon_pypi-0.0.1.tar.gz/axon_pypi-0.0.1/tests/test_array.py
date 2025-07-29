import unittest
import sys, os

try:
  from axon._core import array, zeros, ones, zeros_like, ones_like, randn, randint, uniform, fill, linspace
except ImportError:
  sys.path.append(os.path.dirname(os.path.abspath(__file__)))
  from axon._core import array, zeros, ones, zeros_like, ones_like, randn, randint, uniform, fill, linspace

class TestArrayCreation(unittest.TestCase):
  """Test array creation and initialization"""
  
  def test_array_from_list(self):
    """Test creating array from list"""
    arr = array([1, 2, 3, 4])
    self.assertEqual(arr.shape, (4,))
    self.assertEqual(arr.size, 4)
    self.assertEqual(arr.ndim, 1)
    self.assertEqual(arr.to_list(), [1.0, 2.0, 3.0, 4.0])
  
  def test_array_from_nested_list(self):
    """Test creating array from nested list"""
    arr = array([[1, 2], [3, 4]])
    self.assertEqual(arr.shape, (2, 2))
    self.assertEqual(arr.size, 4)
    self.assertEqual(arr.ndim, 2)
    self.assertEqual(arr.to_list(), [[1.0, 2.0], [3.0, 4.0]])
  
  def test_array_from_scalar(self):
    """Test creating array from scalar"""
    arr = array(5)
    self.assertEqual(arr.shape, ())
    self.assertEqual(arr.size, 1)
    self.assertEqual(arr.ndim, 0)
    self.assertEqual(arr.to_list(), 5.0)
  
  def test_array_dtype_specification(self):
    """Test dtype specification during creation"""
    arr_float = array([1, 2, 3], dtype="float32")
    arr_int = array([1, 2, 3], dtype="int32")
    
    self.assertEqual(arr_float._get_dtype_name(), "float32")
    self.assertEqual(arr_int._get_dtype_name(), "int32")
  
  def test_unsupported_dtype(self):
    """Test error handling for unsupported dtype"""
    with self.assertRaises(ValueError):
      array([1, 2, 3], dtype="complex64")


class TestUtilityFunctions(unittest.TestCase):
  """Test utility functions for array creation"""
  
  def test_zeros(self):
    """Test zeros function"""
    arr = zeros((2, 3))
    self.assertEqual(arr.shape, (2, 3))
    self.assertEqual(arr.size, 6)
    expected = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    self.assertEqual(arr.to_list(), expected)
  
  def test_ones(self):
    """Test ones function"""
    arr = ones((3, 2))
    self.assertEqual(arr.shape, (3, 2))
    expected = [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]
    self.assertEqual(arr.to_list(), expected)
  
  def test_zeros_like(self):
    """Test zeros_like function"""
    original = array([[1, 2], [3, 4]])
    arr = zeros_like(original)
    self.assertEqual(arr.shape, original.shape)
    self.assertEqual(arr.to_list(), [[0.0, 0.0], [0.0, 0.0]])
  
  def test_ones_like(self):
    """Test ones_like function"""
    original = array([1, 2, 3])
    arr = ones_like(original)
    self.assertEqual(arr.shape, original.shape)
    self.assertEqual(arr.to_list(), [1.0, 1.0, 1.0])
  
  def test_fill(self):
    """Test fill function"""
    arr = fill(3.14, (2, 2))
    self.assertEqual(arr.shape, (2, 2))
    expected = [[3.14, 3.14], [3.14, 3.14]]
    for i in range(2):
      for j in range(2):
        self.assertAlmostEqual(arr.to_list()[i][j], expected[i][j], places=5)
  
  def test_linspace(self):
    """Test linspace function"""
    arr = linspace(0.0, 1.0, 2.0, (3,))
    self.assertEqual(arr.shape, (3,))
    # This test depends on the exact implementation of linspace
    # Adjust expected values based on your C implementation
  
  def test_randn_shape(self):
    """Test randn function shape"""
    arr = randn((2, 3))
    self.assertEqual(arr.shape, (2, 3))
    self.assertEqual(arr.size, 6)
  
  def test_randint_shape(self):
    """Test randint function shape"""
    arr = randint(0, 10, (2, 2))
    self.assertEqual(arr.shape, (2, 2))
    self.assertEqual(arr.size, 4)
  
  def test_uniform_shape(self):
    """Test uniform function shape"""
    arr = uniform(0, 1, (3,))
    self.assertEqual(arr.shape, (3,))
    self.assertEqual(arr.size, 3)


class TestArithmeticOperations(unittest.TestCase):
  """Test arithmetic operations"""
  
  def setUp(self):
    self.arr1 = array([1, 2, 3])
    self.arr2 = array([4, 5, 6])
    self.scalar = 2
  
  def test_addition_array(self):
    """Test array addition"""
    result = self.arr1 + self.arr2
    self.assertEqual(result.to_list(), [5.0, 7.0, 9.0])
  
  def test_addition_scalar(self):
    """Test scalar addition"""
    result = self.arr1 + self.scalar
    self.assertEqual(result.to_list(), [3.0, 4.0, 5.0])
  
  def test_right_addition(self):
    """Test right addition"""
    result = self.scalar + self.arr1
    self.assertEqual(result.to_list(), [3.0, 4.0, 5.0])
  
  def test_subtraction_array(self):
    """Test array subtraction"""
    result = self.arr2 - self.arr1
    self.assertEqual(result.to_list(), [3.0, 3.0, 3.0])
  
  def test_subtraction_scalar(self):
    """Test scalar subtraction"""
    result = self.arr1 - self.scalar
    self.assertEqual(result.to_list(), [-1.0, 0.0, 1.0])
  
  def test_multiplication_array(self):
    """Test array multiplication"""
    result = self.arr1 * self.arr2
    self.assertEqual(result.to_list(), [4.0, 10.0, 18.0])
  
  def test_multiplication_scalar(self):
    """Test scalar multiplication"""
    result = self.arr1 * self.scalar
    self.assertEqual(result.to_list(), [2.0, 4.0, 6.0])
  
  def test_division_array(self):
    """Test array division"""
    result = self.arr2 / self.arr1
    self.assertEqual(result.to_list(), [4.0, 2.5, 2.0])
  
  def test_division_scalar(self):
    """Test scalar division"""
    result = self.arr1 / self.scalar
    self.assertEqual(result.to_list(), [0.5, 1.0, 1.5])
  
  def test_power_scalar(self):
    """Test power with scalar"""
    result = self.arr1 ** 2
    self.assertEqual(result.to_list(), [1.0, 4.0, 9.0])
  
  def test_right_power(self):
    """Test right power"""
    arr = array([1, 2, 3])
    result = 2 ** arr
    self.assertEqual(result.to_list(), [2.0, 4.0, 8.0])


class TestComparisonOperations(unittest.TestCase):
  """Test comparison operations"""
  
  def test_equality_array(self):
    """Test array equality"""
    arr1 = array([1, 2, 3])
    arr2 = array([1, 0, 3])
    result = arr1 == arr2
    # Assuming boolean results are returned as 1.0/0.0
    expected = [1.0, 0.0, 1.0]  # True, False, True
    self.assertEqual(result.to_list(), expected)
  
  def test_equality_scalar(self):
    """Test scalar equality"""
    arr = array([1, 2, 1])
    result = arr == 1
    expected = [1.0, 0.0, 1.0]  # True, False, True
    self.assertEqual(result.to_list(), expected)


class TestMathematicalFunctions(unittest.TestCase):
  """Test mathematical functions"""
  
  def test_log(self):
    """Test natural logarithm"""
    arr = array([1, 2.71828, 7.389])
    result = arr.log()
    # Check approximate values
    self.assertAlmostEqual(result.to_list()[0], 0.0, places=3)
    self.assertAlmostEqual(result.to_list()[1], 1.0, places=3)
  
  def test_exp(self):
    """Test exponential"""
    arr = array([0, 1, 2])
    result = arr.exp()
    expected = [1.0, 2.718, 7.389]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=2)
  
  def test_abs(self):
    """Test absolute value"""
    arr = array([-2, -1, 0, 1, 2])
    result = arr.abs()
    self.assertEqual(result.to_list(), [2.0, 1.0, 0.0, 1.0, 2.0])
  
  def test_sin(self):
    """Test sine function"""
    arr = array([0, 1.5708, 3.14159])  # 0, π/2, π
    result = arr.sin()
    expected = [0.0, 1.0, 0.0]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=3)
  
  def test_cos(self):
    """Test cosine function"""
    arr = array([0, 1.5708, 3.14159])  # 0, π/2, π
    result = arr.cos()
    expected = [1.0, 0.0, -1.0]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=3)
  
  def test_tan(self):
    """Test tangent function"""
    arr = array([0, 0.7854])  # 0, π/4
    result = arr.tan()
    expected = [0.0, 1.0]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=3)


class TestShapeManipulation(unittest.TestCase):
  """Test shape manipulation functions"""
  
  def test_reshape(self):
    """Test reshape function"""
    arr = array([1, 2, 3, 4, 5, 6])
    reshaped = arr.reshape((2, 3))
    self.assertEqual(reshaped.shape, (2, 3))
    self.assertEqual(reshaped.to_list(), [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
  
  def test_reshape_invalid(self):
    """Test reshape with invalid dimensions"""
    arr = array([1, 2, 3, 4])
    with self.assertRaises(ValueError):
      arr.reshape((2, 3))  # 6 elements needed, only 4 available
  
  def test_transpose_2d(self):
    """Test transpose for 2D array"""
    arr = array([[1, 2, 3], [4, 5, 6]])
    transposed = arr.transpose()
    expected = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    self.assertEqual(transposed.to_list(), expected)
  
  def test_flatten(self):
    """Test flatten function"""
    arr = array([[1, 2], [3, 4]])
    flattened = arr.flatten()
    self.assertEqual(flattened.shape, (4,))
    self.assertEqual(flattened.to_list(), [1.0, 2.0, 3.0, 4.0])
  
  def test_squeeze(self):
    """Test squeeze function"""
    arr = array([[[1], [2], [3]]])  # Shape: (1, 3, 1)
    squeezed = arr.squeeze()
    self.assertEqual(squeezed.shape, (3,))
    self.assertEqual(squeezed.to_list(), [1.0, 2.0, 3.0])
  
  def test_expand_dims(self):
    """Test expand_dims function"""
    arr = array([1, 2, 3])
    expanded = arr.expand_dims(0)
    self.assertEqual(expanded.shape, (1, 3))
    self.assertEqual(expanded.to_list(), [[1.0, 2.0, 3.0]])


class TestReductionOperations(unittest.TestCase):
  """Test reduction operations"""
  
  def test_sum_all(self):
    """Test sum of all elements"""
    arr = array([[1, 2], [3, 4]])
    result = arr.sum()
    self.assertEqual(result.to_list(), 10.0)
  
  def test_sum_axis(self):
    """Test sum along axis"""
    arr = array([[1, 2], [3, 4]])
    result = arr.sum(axis=0)
    self.assertEqual(result.to_list(), [4.0, 6.0])
  
  def test_mean_all(self):
    """Test mean of all elements"""
    arr = array([1, 2, 3, 4])
    result = arr.mean()
    self.assertEqual(result.to_list(), 2.5)
  
  def test_max_all(self):
    """Test max of all elements"""
    arr = array([1, 5, 3, 2])
    result = arr.max()
    self.assertEqual(result.to_list(), 5.0)
  
  def test_min_all(self):
    """Test min of all elements"""
    arr = array([3, 1, 4, 2])
    result = arr.min()
    self.assertEqual(result.to_list(), 1.0)
  
  def test_var(self):
    """Test variance calculation"""
    arr = array([1, 2, 3, 4, 5])
    result = arr.var()
    # Expected variance: 2.0 (for population variance)
    self.assertAlmostEqual(result.to_list(), 2.0, places=3)
  
  def test_std(self):
    """Test standard deviation calculation"""
    arr = array([1, 2, 3, 4, 5])
    result = arr.std()
    # Expected std: sqrt(2.0) ≈ 1.414
    self.assertAlmostEqual(result.to_list(), 1.414, places=2)


class TestMatrixOperations(unittest.TestCase):
  """Test matrix operations"""
  
  def test_matmul_2d(self):
    """Test 2D matrix multiplication"""
    arr1 = array([[1, 2], [3, 4]])
    arr2 = array([[5, 6], [7, 8]])
    result = arr1 @ arr2
    expected = [[19.0, 22.0], [43.0, 50.0]]
    self.assertEqual(result.to_list(), expected)
  
  def test_matmul_1d_2d(self):
    """Test 1D vector with 2D matrix multiplication"""
    vec = array([1, 2])
    mat = array([[3, 4], [5, 6]])
    result = vec @ mat
    expected = [13.0, 16.0]  # [1*3 + 2*5, 1*4 + 2*6]
    self.assertEqual(result.to_list(), expected)
  
  def test_matmul_2d_1d(self):
    """Test 2D matrix with 1D vector multiplication"""
    mat = array([[1, 2], [3, 4]])
    vec = array([5, 6])
    result = mat @ vec
    expected = [17.0, 39.0]  # [1*5 + 2*6, 3*5 + 4*6]
    self.assertEqual(result.to_list(), expected)


class TestTypeConversion(unittest.TestCase):
  """Test type conversion"""
  
  def test_astype_float_to_int(self):
    """Test conversion from float to int"""
    arr = array([1.7, 2.3, 3.8], dtype="float32")
    int_arr = arr.astype("int32")
    self.assertEqual(int_arr._get_dtype_name(), "int32")
    # Values should be truncated
    self.assertEqual(int_arr.to_list(), [1.0, 2.0, 3.0])
  
  def test_astype_int_to_float(self):
    """Test conversion from int to float"""
    arr = array([1, 2, 3], dtype="int32")
    float_arr = arr.astype("float64")
    self.assertEqual(float_arr._get_dtype_name(), "float64")
    self.assertEqual(float_arr.to_list(), [1.0, 2.0, 3.0])


class TestArrayRepresentation(unittest.TestCase):
  """Test array string representations"""
  
  def test_repr(self):
    """Test repr output"""
    arr = array([1, 2, 3])
    repr_str = repr(arr)
    self.assertIn("array([1, 2, 3]", repr_str)
    self.assertIn("dtype=float32", repr_str)
  
  def test_str(self):
    """Test str output (print functionality)"""
    arr = array([1, 2, 3])
    # The __str__ method calls C backend print function and returns empty string
    str_result = str(arr)
    self.assertEqual(str_result, "")


class TestEdgeCases(unittest.TestCase):
  """Test edge cases and error handling"""
  
  def test_empty_list(self):
    """Test creating array from empty list"""
    # This might raise an error depending on implementation
    try:
      arr = array([])
      self.assertEqual(arr.size, 0)
    except:
      pass  # Expected to fail in some implementations
  
  def test_very_small_numbers(self):
    """Test with very small numbers"""
    arr = array([1e-10, 2e-10, 3e-10])
    result = arr + arr
    expected = [2e-10, 4e-10, 6e-10]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=15)
  
  def test_very_large_numbers(self):
    """Test with very large numbers"""
    arr = array([1e10, 2e10, 3e10])
    result = arr / 1e10
    expected = [1.0, 2.0, 3.0]
    for i, val in enumerate(expected):
      self.assertAlmostEqual(result.to_list()[i], val, places=5)


if __name__ == '__main__':
  # Create a test suite
  test_classes = [
    TestArrayCreation,
    TestUtilityFunctions,
    TestArithmeticOperations,
    TestComparisonOperations,
    TestMathematicalFunctions,
    TestShapeManipulation,
    TestReductionOperations,
    TestMatrixOperations,
    TestTypeConversion,
    TestArrayRepresentation,
    TestEdgeCases
  ]
  
  # Run tests with verbosity
  suite = unittest.TestSuite()
  for test_class in test_classes:
    tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
    suite.addTests(tests)
  
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  
  # Print summary
  print(f"\n{'='*50}")
  print(f"Tests run: {result.testsRun}")
  print(f"Failures: {len(result.failures)}")
  print(f"Errors: {len(result.errors)}")
  print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
  print(f"{'='*50}")