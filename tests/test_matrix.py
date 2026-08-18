from matrixcalc.matrix import Matrix
import pytest

def test_matrix_shape():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    assert A.rows == 2
    assert A.cols == 3
    assert A.shape == (2,3)

def test_matrix_indexing():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert A[0, 0] == 1
    assert A[0, 1] == 2
    assert A[1, 0] == 3
    assert A[1, 1] == 4

def test_matrix_assignment():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    A[0, 1] = 99

    assert A[0, 1] == 99

def test_matrix_rejects_irregular_rows():
    with pytest.raises(ValueError):
        Matrix([
            [1, 2],
            [3]
        ])

def test_matrix_rejects_empty_matrix():
    with pytest.raises(ValueError):
        Matrix([])

def test_matrix_equality():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert A == B


def test_matrix_inequality():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2],
        [3, 5]
    ])

    assert A != B


def test_matrix_different_shapes_are_not_equal():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    assert A != B


def test_matrix_not_equal_to_non_matrix():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert A != [[1, 2], [3, 4]]

def test_matrix_addition():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [5, 6],
        [7, 8]
    ])

    expected = Matrix([
        [6, 8],
        [10, 12]
    ])

    assert A + B == expected


def test_matrix_addition_does_not_modify_operands():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [5, 6],
        [7, 8]
    ])

    A + B

    assert A == Matrix([
        [1, 2],
        [3, 4]
    ])

    assert B == Matrix([
        [5, 6],
        [7, 8]
    ])


def test_matrix_addition_requires_same_shape():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(ValueError):
        A + B

def test_matrix_subtraction():
    A = Matrix([
        [5, 6],
        [7, 8]
    ])

    B = Matrix([
        [1, 2],
        [3, 4]
    ])

    expected = Matrix([
        [4, 4],
        [4, 4]
    ])

    assert A - B == expected


def test_matrix_subtraction_does_not_modify_operands():
    A = Matrix([
        [5, 6],
        [7, 8]
    ])

    B = Matrix([
        [1, 2],
        [3, 4]
    ])

    A - B

    assert A == Matrix([
        [5, 6],
        [7, 8]
    ])

    assert B == Matrix([
        [1, 2],
        [3, 4]
    ])


def test_matrix_subtraction_requires_same_shape():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(ValueError):
        A - B

def test_matrix_scalar_multiplication():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    expected = Matrix([
        [3, 6],
        [9, 12]
    ])

    assert A * 3 == expected


def test_matrix_scalar_multiplication_does_not_modify_matrix():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    A * 3

    assert A == Matrix([
        [1, 2],
        [3, 4]
    ])


def test_matrix_scalar_multiplication_with_float():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    expected = Matrix([
        [0.5, 1.0],
        [1.5, 2.0]
    ])

    assert A * 0.5 == expected


def test_matrix_scalar_multiplication_requires_scalar():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    with pytest.raises(TypeError):
        A * Matrix([
            [1, 2],
            [3, 4]
        ])

def test_scalar_multiplication_left():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    expected = Matrix([
        [3, 6],
        [9, 12]
    ])

    assert 3 * A == expected

def test_matrix_multiplication():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    B = Matrix([
        [7, 8],
        [9, 10],
        [11, 12]
    ])

    expected = Matrix([
        [58, 64],
        [139, 154]
    ])

    assert A @ B == expected


def test_matrix_multiplication_does_not_modify_operands():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [5, 6],
        [7, 8]
    ])

    A @ B

    assert A == Matrix([
        [1, 2],
        [3, 4]
    ])

    assert B == Matrix([
        [5, 6],
        [7, 8]
    ])


def test_matrix_multiplication_requires_compatible_dimensions():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    B = Matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    with pytest.raises(ValueError):
        A @ B


def test_matrix_multiplication_requires_matrix():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    with pytest.raises(TypeError):
        A @ 2

def test_matrix_scalar_division():
    A = Matrix([
        [2, 4],
        [6, 8]
    ])

    expected = Matrix([
        [1, 2],
        [3, 4]
    ])

    assert A / 2 == expected


def test_matrix_scalar_division_with_float():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    expected = Matrix([
        [2, 4],
        [6, 8]
    ])

    assert A / 0.5 == expected


def test_matrix_scalar_division_does_not_modify_matrix():
    A = Matrix([
        [2, 4],
        [6, 8]
    ])

    A / 2

    assert A == Matrix([
        [2, 4],
        [6, 8]
    ])


def test_matrix_scalar_division_requires_scalar():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    with pytest.raises(TypeError):
        A / Matrix([
            [1, 2],
            [3, 4]
        ])


def test_matrix_scalar_division_by_zero():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    with pytest.raises(ZeroDivisionError):
        A / 0

def test_matrix_negation():
    A = Matrix([
        [1, -2],
        [3, 4]
    ])

    expected = Matrix([
        [-1, 2],
        [-3, -4]
    ])

    assert -A == expected


def test_matrix_negation_does_not_modify_matrix():
    A = Matrix([
        [1, -2],
        [3, 4]
    ])

    -A

    assert A == Matrix([
        [1, -2],
        [3, 4]
    ])


def test_matrix_double_negation():
    A = Matrix([
        [1, -2],
        [3, 4]
    ])

    assert -(-A) == A

def test_matrix_transpose():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    expected = Matrix([
        [1, 4],
        [2, 5],
        [3, 6]
    ])

    assert A.T == expected


def test_matrix_transpose_does_not_modify_matrix():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    A.T

    assert A == Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])


def test_matrix_double_transpose():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    assert A.T.T == A

def test_matrix_identity():
    I = Matrix.identity(3)

    expected = Matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    assert I == expected


def test_matrix_identity_shape():
    I = Matrix.identity(4)

    assert I.shape == (4, 4)


def test_matrix_identity_size_one():
    I = Matrix.identity(1)

    assert I == Matrix([
        [1]
    ])


def test_matrix_identity_multiplication():
    A = Matrix([
        [1, 2],
        [3, 4]
    ])

    I = Matrix.identity(2)

    assert A @ I == A
    assert I @ A == A

def test_matrix_zeros():
    Z = Matrix.zeros(2, 3)

    expected = Matrix([
        [0, 0, 0],
        [0, 0, 0]
    ])

    assert Z == expected


def test_matrix_zeros_shape():
    Z = Matrix.zeros(3, 4)

    assert Z.shape == (3, 4)


def test_matrix_zeros_requires_positive_integer_dimensions():
    with pytest.raises(TypeError):
        Matrix.zeros(2.5, 3)

    with pytest.raises(TypeError):
        Matrix.zeros(2, 3.5)

    with pytest.raises(TypeError):
        Matrix.zeros("2", 3)

    with pytest.raises(ValueError):
        Matrix.zeros(0, 3)

    with pytest.raises(ValueError):
        Matrix.zeros(2, 0)

    with pytest.raises(ValueError):
        Matrix.zeros(-2, 3)

    with pytest.raises(ValueError):
        Matrix.zeros(2, -3)

def test_matrix_trace():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    assert A.trace == 15


def test_matrix_trace_with_negative_values():
    A = Matrix([
        [-1, 2],
        [3, -4]
    ])

    assert A.trace == -5


def test_matrix_trace_requires_square_matrix():
    A = Matrix([
        [1, 2, 3],
        [4, 5, 6]
    ])

    with pytest.raises(ValueError):
        A.trace

def test_to_list():
    matrix = Matrix([[1, 2], [3, 4]])

    assert matrix.to_list() == [[1, 2], [3, 4]]

def test_to_list_returns_copy():
    matrix = Matrix([[1, 2], [3, 4]])

    data = matrix.to_list()
    data[0][0] = 99

    assert matrix == Matrix([[1, 2], [3, 4]])
