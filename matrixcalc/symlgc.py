from __future__ import annotations

# Monomial contains a series of variables and degrees, but not a coefficient
# Monomial is a dictionary, with keys representing variables, and values representing degrees
class Monomial:
    def __init__(self, exponents: dict[str, int]) -> None:
        if not data:
            # Arch decision -- allow empty monomial? -- leaning yes
        # Internal structure with dictionary
        # {}

        # Data validation - keys must be variables (lowercase str), values must be integers


    # NOTE: __add__, __sub__, and __neg__ not implemented for architectural reasons

    # Returns a variable's degree
    def __getitem__(self, key: str) -> int:
        return self._exponents[key]

    # Sets a variable's degree
    def __setitem__(self, key: str, value: int) -> none:
        self._exponents[key] = value

    def __repr__(self) -> str:
        return f"Monomial({self._exponents!r})"

    def __str__(self) -> str:
        # Have to decide how to make exponents look nice in terminal-friendly way

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Monomial):
            return False

        return self._exponents == other._exponents

    def __mul__(self, other: object) -> Monomial:
        if not isinstance(other, Monomial):
            return NotImplemented

        result_data = {}
        for key in self._exponents.keys() | other._exponents.keys():
            result_data[key] = (
                self._exponents.get(key, 0)
                + other._exponents.get(key, 0)
            )
        return Monomial(result_data).clean()

    def __rmul__(self, other: object) -> Monomial:
        return self * other
            
    def __truediv__(self, other: object) -> Monomial:
        if not isinstance(other, Monomial):
            return NotImplemented

        return self * other.reciprocal()
    
    # Methods

    # Remove zero entries
    def clean(self) -> None:
        for key, value in self.items():
            if value == 0:
                self.pop(key)

    def reciprocal(self) -> Monomial:
        result_data = {
            key: -value
            for key, value in self._exponents.items()
        }
        return Monomial(result_data)

# A Polynomial stores only nonzero coefficients, with integer exponents ≥ 0
# Its internal mapping is normalized so that each exponent occurs exactly once.

class Polynomial:
    def __init__(self, data):
        # Placeholder

    # Returns a coefficient
    def __getitem__(self, index):
        # Placeholder
    
    # Sets a coefficient
    def __setitem__(self, index, value):
        # Placeholder

    def __repr__(self):
        # Placeholder

    def __str__(self):
        # Placeholder

    def __eq__(self, other):
        # Placeholder

    def __add__(self, other):
        # Placeholder

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
        return -1 * self

