from __future__ import annotations
from typing import TypedDict, Literal
from typing_extensions import override

class Monomial:
    """Represents a product of variables raised to integer powers.

    A Monomial does not contain a coefficient. It is internally represented
    as a mapping from variable names to integer exponents and is
    immutable after initialization.
    """
    _exponents: dict[str, int]

    def __init__(self, exponents: dict[str, int] | None = None) -> None:
        if exponents is None:
            exponents = {}

        # Data validation - keys must be variables (1 lowercase letter)
        if not all(
            len(key) == 1 and key.isascii() and key.islower()
            for key in exponents
        ):
            raise ValueError("Variables must be single lowercase letters")

        # Clean (remove zero entries) on init
        self._exponents = {
            key : value
            for key, value in exponents.items()
            if value != 0
        }


    # NOTE: __add__, __sub__, __neg__, __setitem__ not implemented for architectural reasons

    @override
    def __hash__(self) -> int:
        return hash(frozenset(self._exponents.items()))

    # Returns a variable's degree
    def __getitem__(self, key: str) -> int:
        return self._exponents.get(key, 0)

    @override
    def __repr__(self) -> str:
        return f"Monomial({self._exponents!r})"

    @override
    def __str__(self) -> str:
        if not self._exponents:
            return "1"

        return "".join(
            f"{key}{value if value != 1 else ''}"
            for key, value in sorted(self._exponents.items())
        )

    @override
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

    @classmethod
    def from_dict(cls, dictionary: dict[str, int]) -> Monomial:
        return cls(dictionary)

    # Methods

    def reciprocal(self) -> Monomial:
        result_data = {
            key: -value
            for key, value in self._exponents.items()
        }
        return Monomial(result_data)

    def to_dict(self) -> dict[str, int]:
        return self._exponents.copy()

    # Properties

    @property
    def total_degree(self) -> int:
        return sum(self._exponents.values())

class Polynomial:
    """Stores a normalized mapping of Monomials to numeric coefficients.

    Monomial() represents the non-variable (constant) term.
    """
    _coef: dict[Monomial, int | float]

    def __init__(self, coef: dict[Monomial, int | float]) -> None:
        self._coef = coef.copy()
        if Monomial() not in self._coef:
            self._coef[Monomial()] = 0
        self.clean()

    # Returns a coefficient
    def __getitem__(self, key: Monomial) -> int | float:
        return self._coef.get(key, 0)

    # Sets a coefficient
    def __setitem__(self, key: Monomial, value: int | float) -> None:
        self._coef[key] = value

    @override
    def __repr__(self) -> str:
        return f"Polynomial({self._coef!r})"

    @override
    def __str__(self) -> str:
        # Sort by total degree of each monomial
        sorted_monomials = sorted(
            self._coef,
            key=lambda m: m.total_degree,
            reverse=True
        )
        terms: list[str] = []
        # Combine each coef with each monomial
        for i, mono in enumerate(sorted_monomials):
            # Case 1: Coefficient of the constant term
            if mono == Monomial():
                abscoefmono = str(abs(self._coef[mono]))
            # Case 2: Absolute value of coefficient is 1
            elif abs(self._coef[mono]) == 1:
                abscoefmono = str(mono)
            # Case 3: All other conditions
            else:
                abscoefmono = f"{abs(self._coef[mono])}{mono}"

            if i == 0:
                if self._coef[mono] < 0:
                    terms.append(f"-{abscoefmono}")
                else:
                    terms.append(f"{abscoefmono}")
            else:
                joiner = " - " if self._coef[mono] < 0 else " + "
                terms.append(f"{joiner}{abscoefmono}")

        # Remove trailing zero
        try:
            terms.remove(" + 0")
        except ValueError:
            pass

        # Combine terms
        return "".join(terms)

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            return self._coef == Polynomial.from_number(other)._coef
        if isinstance(other, Polynomial):
            return self._coef == other._coef
        return False

    def __add__(self, other: Polynomial | int | float) -> Polynomial:
        if isinstance(other, (int, float)):
            other = Polynomial.from_number(other)

        result_data: dict[Monomial, int | float] = {}
        for key in self._coef.keys() | other._coef.keys():
            result_data[key] = (
                self._coef.get(key, 0)
                + other._coef.get(key, 0)
            )
        result = Polynomial(result_data)
        result.clean()
        return result

    def __radd__(self, other: Polynomial | int | float) -> Polynomial:
        return self + other

    def __sub__(self, other: Polynomial | int | float) -> Polynomial:
        return self + -other

    def __rsub__(self, other: Polynomial | int | float) -> Polynomial:
        return self + -other

    def __mul__(self, other: object) -> Polynomial:
        if isinstance(other, (int, float)):
            result_data = {
                mono: coef * other
                for mono, coef in self._coef.items()
            }
            return Polynomial(result_data)
        elif isinstance(other, Polynomial):
            result_data: dict[Monomial, int | float] = {}

            for mono1, coef1 in self._coef.items():
                for mono2, coef2 in other._coef.items():
                    mono, coef = self._multiply_terms(
                        mono1, coef1, mono2, coef2
                    )
                    # If mono already exists, add coef to its value
                    result_data[mono] = result_data.get(mono, 0) + coef

            return Polynomial(result_data)
        else:
            return NotImplemented

    def __rmul__(self, other: object) -> Polynomial:
        return self * other
            
    # Note: Only scalar division currently supported
    def __truediv__(self, scalar: int | float) -> Polynomial:
        return Polynomial({
            mono: coef / scalar
            for mono, coef in self._coef.items()
        })

    def __neg__(self) -> Polynomial:
        result_data = {
            key: -value
            for key, value in self._coef.items()
        }
        return Polynomial(result_data)

    # Class Methods

    @classmethod
    def from_dict(cls, dictionary: PolynomialData) -> Polynomial:
        data: dict[Monomial, int | float] = {}
        for term in dictionary["terms"]:
            mono = Monomial.from_dict(term["monomial"])
            coef = term["coefficient"]
            data[mono] = coef
        return cls(data)

    @classmethod
    def from_number(cls, num: int | float) -> Polynomial:
        return cls({Monomial(): num})

    @classmethod
    def zero(cls) -> Polynomial:
        return cls({Monomial(): 0})

    # Methods
   
    def to_dict(self) -> PolynomialData:
        term_list: list[TermData] = [
            {
                "monomial": mono.to_dict(),
                "coefficient": value,
            }
            for mono, value in self._coef.items()
        ]
        return {
            "__type__": "Polynomial",
            "terms": term_list,
        }

    # Remove zero entries
    def clean(self) -> None:
        for key in list(self._coef):
            if self[key] == 0 and key != Monomial():
                del self._coef[key]

    # Static Methods
    @staticmethod
    def _multiply_terms(
        mono1: Monomial,
        coef1: int | float,
        mono2: Monomial,
        coef2: int | float,
    ) -> tuple[Monomial, int | float]:
        return mono1 * mono2, coef1 * coef2

class TermData(TypedDict):
    monomial: dict[str, int]
    coefficient: int | float

class PolynomialData(TypedDict):
    __type__: Literal["Polynomial"]
    terms: list[TermData]
