from __future__ import annotations
import ast
from collections.abc import Sequence
from .symlgc import Polynomial, PolynomialData

# MatrixValue is valid cell type at runtime
MatrixValue = Polynomial | int | float
# MatrixData is valid cell type during serialization
MatrixData = PolynomialData | int | float

class Matrix:
    _data: list[list[MatrixValue]]

    def __init__(self, data: Sequence[Sequence[MatrixValue]]) -> None:

        ## DATA VALIDATION
        if not data:
            raise ValueError("Matrix cannot be empty")

        if not all(isinstance(row, list) for row in data):
            raise TypeError("Matrix must be list of lists")

        # Get number of columns from first row
        cols = len(data[0])

        if cols == 0:
            raise ValueError("Matrix cannot have empty rows")

        if not all(len(row) == cols for row in data):
            raise ValueError("All rows must have same length")

        # Shallow copy data to self._data
        # NOTE: May affect symbolic logic implementation
        self._data = [list(row) for row in data]

    # Dunder
    def __getitem__(self, index: tuple[int, int]) -> Polynomial | int | float:
        row, col = index
        return self._data[row][col]

    def __setitem__(self, index: tuple[int, int], value: Polynomial | int | float) -> None:
        row, col = index
        self._data[row][col] = value

    def __repr__(self) -> str:
        return f"Matrix({self._data!r})"

    def __str__(self) -> str:
        width = self.max_cell_length

        return "\n".join(
            " ".join(f"{str(value):>{width}}" for value in row)
            for row in self._data
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return False

        if self.shape != other.shape:
            return False

        return all(
            self._data[row][col] == other._data[row][col]
            for row in range(self.rows)
            for col in range(self.cols)
        )

    def __add__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            raise TypeError("Matrix must be added to another matrix")

        if self.shape != other.shape:
            raise ValueError("Matrix must be added to matrix of the same shape")

        data = [
            [
                self._data[row][col] + other._data[row][col]
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]

        return Matrix(data)

    def __sub__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            raise TypeError("Matrix must be added to another matrix")

        if self.shape != other.shape:
            raise ValueError("Matrix must be added to matrix of the same shape")

        data = [
            [
                self._data[row][col] - other._data[row][col]
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]

        return Matrix(data)

    def __mul__(self, scalar: Polynomial | int | float) -> Matrix:
        if not isinstance(scalar, (Polynomial | int, float)):
            raise TypeError("Scalar must be Polynomial, int or float")

        data = [
            [
                self._data[row][col] * scalar
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]

        return Matrix(data)

    def __rmul__(self, scalar: Polynomial | int | float) -> Matrix:
        return self * scalar

    def __matmul__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            raise TypeError("Matrix multiplication requires two matrices")

        if self.cols != other.rows:
            raise ValueError("Matrices are not compatible shapes")

        data = [
            [
                sum(
                    self._data[row][k] * other._data[k][col]
                    for k in range(self.cols)
                )
                for col in range(other.cols)
            ]
            for row in range(self.rows)
        ]

        return Matrix(data)

    def __truediv__(self, scalar: int | float) -> Matrix:
        if not isinstance(scalar, (int,float)):
            raise TypeError("Matrix must be divided by an int or float")

        return self * (1 / scalar)

    def __neg__(self) -> Matrix:
        return -1 * self

    # Properties
    @property
    def rows(self) -> int:
        return len(self._data)

    @property
    def cols(self) -> int:
        return len(self._data[0])

    @property
    def shape(self) -> tuple[int, int]:
        return (self.rows, self.cols)

    @property
    # transpose property
    def T(self) -> Matrix:
        data = [
            [self._data[row][col] for row in range(self.rows)]
            for col in range(self.cols)
        ]

        return Matrix(data)

    @property
    def trace(self) -> Polynomial | int | float:
        if self.cols != self.rows:
            raise ValueError("Trace not defined for non-square matrices")	

        return sum(self._data[k][k] for k in range(self.rows))

    @property
    def max_cell_length(self) -> int:
        return max(
            len(str(value))
            for row in self._data
            for value in row
        )

    # Class Methods
    @classmethod
    def identity(cls, n: int) -> Matrix:
        data = [
            [
                1 if row == col else 0
                for col in range(n)
            ]
            for row in range(n)
        ]

        return Matrix(data)

    @classmethod
    def zeros(cls, rows: int, cols: int) -> Matrix:

        if not isinstance(rows, int) or not isinstance(cols, int):
            raise TypeError("Dimensions must be integers")

        if rows <= 0 or cols <=0:
            raise ValueError("Dimensions must be positive")

        data = [
            [0] * cols
            for _ in range(rows)
        ]

        return Matrix(data)

    @classmethod
    def from_list(cls, data_list : list[list[MatrixData]]) -> Matrix:
        matrix_list: list[list[MatrixValue]] = []

        for row_data in data_list:
            row: list[MatrixValue] = []

            for cell_data in row_data:
                if isinstance(cell_data, dict):
                    if cell_data.get("__type__") == "Polynomial":
                        row.append(Polynomial.from_dict(cell_data))
                    else:
                        raise ValueError("Unknown dict as cell data")
                elif isinstance(cell_data, (int, float)):
                    row.append(cell_data)
                else:
                    raise ValueError("Invalid cell data")

            matrix_list.append(row)

        return cls(matrix_list)

    # Methods
    def to_list(self) -> list[list[MatrixData]]:
        return [
            [
                value.to_dict() if isinstance(value, Polynomial) else value
                for value in row
            ]
            for row in self._data
        ]

    def copy(self) -> Matrix:
        return Matrix(self.to_list())
