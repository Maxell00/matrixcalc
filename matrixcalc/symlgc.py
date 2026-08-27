from __future__ import annotations

# Monomial contains a series of variables and degrees, but not a coefficient
# Monomial is internally structured as a dictionary, with keys representing variables, and values representing degrees
# Monomial is immutable
class Monomial:
    _exponents: dict[str, int]

    def __init__(self, exponents: dict[str, int] | None = None) -> None:
        if exponents is None:
            exponents = {}

        # Clean (remove zero entries) on init
        self._exponents = {
            key : value
            for key, value in exponents.items()
            if value != 0
        }

        # Data validation - keys must be variables (lowercase str), values must be integers
        # PLACEHOLDER

    # NOTE: __add__, __sub__, __neg__, __setitem__ not implemented for architectural reasons

    def __hash__(self) -> int:
        return hash(frozenset(self._exponents.items()))

    # Returns a variable's degree
    def __getitem__(self, key: str) -> int:
        return self._exponents.get(key, 0)

    def __repr__(self) -> str:
        return f"Monomial({self._exponents!r})"

    def __str__(self) -> str:
        if not self._exponents:
            return "1"

        return "".join(
            f"{key}{value if value != 1 else ''}"
            for key, value in sorted(self._exponents.items())
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Monomial):
            return False

        return self._exponents == other._exponents

    def __mul__(self, other: object) -> Monomial:
        if not isinstance(other, Monomial):
            return NotImplemented

        result_data: dict[str, int] = {}
        for key in self._exponents.keys() | other._exponents.keys():
            result_data[key] = (
                self._exponents.get(key, 0)
                + other._exponents.get(key, 0)
            )
        return Monomial(result_data)

    def __rmul__(self, other: object) -> Monomial:
        return self * other
            
    def __truediv__(self, other: object) -> Monomial:
        if not isinstance(other, Monomial):
            return NotImplemented

        return self * other.reciprocal()
    
    # Class Methods

    # Methods

    def reciprocal(self) -> Monomial:
        result_data = {
            key: -value
            for key, value in self._exponents.items()
        }
        return Monomial(result_data)

class Polynomial:
    """Stores a normalized mapping of Monomials to numeric coefficients.

    Monomial() represents the non-variable (constant) term.
    """
    _coef: dict[Monomial, int | float]

    def __init__(self, coef: dict[Monomial, int | float]) -> None:
        # DATA VALIDATION
        # coef must contain Monomial()
        # PLACEHOLDER

        self._coef = coef.copy()

    # Returns a coefficient
    def __getitem__(self, key: Monomial) -> int | float:
        return self._coef.get(key, 0)

    # Sets a coefficient
    def __setitem__(self, key: Monomial, value: int | float) -> None:
        self._coef[key] = value

    def __repr__(self) -> str:
        return f"Polynomial({self._coef!r})"

    def __str__(self):
        # Implementation TBD
        return

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            return self._coef == Polynomial.from_number(other)._coef
        if isinstance(other, Polynomial):
            return self._coef == other._coef
        return False

    def __add__(self, other: Polynomial | int | float) -> Polynomial:
        if isinstance(other, (int, float)):
            other = Polynomial.from_number(other)

        result_data = {}
        for key in self._coef.keys() | other._coef.keys():
            result_data[key] = (
                self._coef.get(key, 0)
                + other._coef.get(key, 0)
            )
        result = Polynomial(result_data)
        result.clean()
        return result

    def __sub__(self, other):
        # Placeholder

    def __mul__(self, other):
        # Placeholder

    def __rmul__(self, other):
        # Placeholder
            
    # Needed?
    def __truediv__(self, scalar):
        # Placeholder

    def __neg__(self):
        result_data = {
            key: -value
            for key, value in self._coef
        }
        return Polynomial(result_data)

    # Class Methods

    @classmethod
    def from_number(cls, num: int | float) -> Polynomial:
        return cls({Monomial(): num})

    @classmethod
    def zero(cls) -> Polynomial:
        return cls({Monomial(): 0})

    # Methods

    # Remove zero entries
    def clean(self) -> None:
        for key in list(self._coef):
            if self[key] == 0 and key != Monomial():
                del self._coef[key]

