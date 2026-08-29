import pytest
from matrixcalc.cli import parse_polynomial, varlist_to_monomial
from matrixcalc.symlgc import Monomial, Polynomial

# ---------------------------------------------------------------------------
# varlist_to_monomial
# ---------------------------------------------------------------------------

def test_varlist_to_monomial_single_variable():
    assert varlist_to_monomial(["x"]) == Monomial({"x": 1})


def test_varlist_to_monomial_variable_with_exponent():
    assert varlist_to_monomial(["x2"]) == Monomial({"x": 2})


def test_varlist_to_monomial_multiple_variables():
    assert varlist_to_monomial(["x2", "y3", "z"]) == Monomial(
        {"x": 2, "y": 3, "z": 1}
    )


def test_varlist_to_monomial_repeated_variable():
    with pytest.raises(ValueError, match="repeated variables"):
        varlist_to_monomial(["x2", "x3"])


# ---------------------------------------------------------------------------
# parse_polynomial
# ---------------------------------------------------------------------------

def test_parse_polynomial_single_term():
    assert parse_polynomial("3x2") == Polynomial(
        {Monomial({"x": 2}): 3}
    )


def test_parse_polynomial_multiple_terms():
    assert parse_polynomial("3x2+4xy-7z") == Polynomial(
        {
            Monomial({"x": 2}): 3,
            Monomial({"x": 1, "y": 1}): 4,
            Monomial({"z": 1}): -7,
        }
    )


def test_parse_polynomial_implicit_coefficient():
    assert parse_polynomial("x2-y") == Polynomial(
        {
            Monomial({"x": 2}): 1,
            Monomial({"y": 1}): -1,
        }
    )


def test_parse_polynomial_negative_first_term():
    assert parse_polynomial("-3x2+y") == Polynomial(
        {
            Monomial({"x": 2}): -3,
            Monomial({"y": 1}): 1,
        }
    )


def test_parse_polynomial_positive_first_term():
    assert parse_polynomial("+3x2+y") == Polynomial(
        {
            Monomial({"x": 2}): 3,
            Monomial({"y": 1}): 1,
        }
    )


def test_parse_polynomial_repeated_monomial():
    with pytest.raises(ValueError, match="repeated Monomials"):
        parse_polynomial("3x2+4x2")


def test_parse_polynomial_multiple_variables():
    assert parse_polynomial("2x2y3z") == Polynomial(
        {Monomial({"x": 2, "y": 3, "z": 1}): 2}
    )
