import pytest

from matrixcalc.symlgc import Monomial, Polynomial


# ---------------------------------------------------------------------------
# Monomial construction and representation
# ---------------------------------------------------------------------------


def test_monomial_default():
    mono = Monomial()

    assert mono._exponents == {}
    assert str(mono) == "1"


def test_monomial_removes_zero_exponents():
    mono = Monomial({"x": 2, "y": 0, "z": 3})

    assert mono._exponents == {"x": 2, "z": 3}


def test_monomial_rejects_invalid_variable_names():
    with pytest.raises(ValueError):
        Monomial({"xy": 2})

    with pytest.raises(ValueError):
        Monomial({"X": 2})


def test_monomial_getitem():
    mono = Monomial({"x": 2, "y": 3})

    assert mono["x"] == 2
    assert mono["y"] == 3
    assert mono["z"] == 0


def test_monomial_repr():
    mono = Monomial({"x": 2, "y": 3})

    assert repr(mono) == "Monomial({'x': 2, 'y': 3})"


def test_monomial_str():
    assert str(Monomial()) == "1"
    assert str(Monomial({"x": 2})) == "x2"
    assert str(Monomial({"x": 2, "y": 1})) == "x2y"
    assert str(Monomial({"z": 8, "x": 2, "y": -1})) == "x2y-1z8"


# ---------------------------------------------------------------------------
# Monomial equality, hashing, and degree
# ---------------------------------------------------------------------------


def test_monomial_equality():
    assert Monomial({"x": 2, "y": 3}) == Monomial({"y": 3, "x": 2})
    assert Monomial({"x": 2}) != Monomial({"x": 3})
    assert Monomial({"x": 2}) != 2


def test_monomial_hash():
    mono1 = Monomial({"x": 2, "y": 3})
    mono2 = Monomial({"y": 3, "x": 2})

    assert hash(mono1) == hash(mono2)


def test_monomial_can_be_dict_key():
    mono = Monomial({"x": 2})

    data = {mono: 5}

    assert data[Monomial({"x": 2})] == 5


def test_monomial_total_degree():
    assert Monomial().total_degree == 0
    assert Monomial({"x": 4}).total_degree == 4
    assert Monomial({"x": 2, "y": 3}).total_degree == 5


# ---------------------------------------------------------------------------
# Monomial arithmetic
# ---------------------------------------------------------------------------


def test_monomial_multiplication():
    x2 = Monomial({"x": 2})
    xy = Monomial({"x": 1, "y": 1})

    assert x2 * xy == Monomial({"x": 3, "y": 1})


def test_monomial_multiplication_with_missing_variables():
    x2 = Monomial({"x": 2})
    yz = Monomial({"y": 1, "z": 1})

    assert x2 * yz == Monomial({"x": 2, "y": 1, "z": 1})


def test_monomial_multiplication_cancels_exponents():
    xy = Monomial({"x": 1, "y": 1})
    x_reciprocal = Monomial({"x": -1})

    assert xy * x_reciprocal == Monomial({"y": 1})


def test_monomial_reciprocal():
    mono = Monomial({"x": 2, "y": -3})

    assert mono.reciprocal() == Monomial({"x": -2, "y": 3})


def test_monomial_division():
    x2y = Monomial({"x": 2, "y": 1})
    xy2 = Monomial({"x": 1, "y": 2})

    assert x2y / xy2 == Monomial({"x": 1, "y": -1})


# ---------------------------------------------------------------------------
# Polynomial construction and representation
# ---------------------------------------------------------------------------


def test_polynomial_default_constant_term():
    poly = Polynomial({Monomial({"x": 2}): 3})

    assert Monomial() in poly._coef
    assert poly[Monomial()] == 0


def test_polynomial_copies_input():
    data = {Monomial({"x": 2}): 3}

    poly = Polynomial(data)
    data[Monomial({"y": 1})] = 5

    assert Monomial({"y": 1}) not in poly._coef


def test_polynomial_removes_zero_terms():
    poly = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial({"y": 1}): 0,
        Monomial(): 0,
    })

    assert Monomial({"x": 2}) in poly._coef
    assert Monomial({"y": 1}) not in poly._coef
    assert Monomial() in poly._coef


def test_polynomial_getitem():
    poly = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 5,
    })

    assert poly[Monomial({"x": 2})] == 3
    assert poly[Monomial({"y": 1})] == 0
    assert poly[Monomial()] == 5


def test_polynomial_repr():
    mono = Monomial({"x": 2})
    poly = Polynomial({mono: 3})

    assert repr(poly) == "Polynomial({Monomial({'x': 2}): 3, Monomial({}): 0})"


# ---------------------------------------------------------------------------
# Polynomial equality
# ---------------------------------------------------------------------------


def test_polynomial_equality():
    assert Polynomial({Monomial({"x": 2}): 3}) == Polynomial(
        {Monomial({"x": 2}): 3}
    )


def test_polynomial_inequality():
    assert Polynomial({Monomial({"x": 2}): 3}) != Polynomial(
        {Monomial({"x": 2}): 4}
    )


def test_polynomial_equals_number():
    assert Polynomial.from_number(3) == 3
    assert Polynomial.from_number(3.5) == 3.5


def test_zero_polynomial_equals_zero():
    assert Polynomial.zero() == 0


# ---------------------------------------------------------------------------
# Polynomial addition and subtraction
# ---------------------------------------------------------------------------


def test_polynomial_addition():
    p = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 2,
    })

    q = Polynomial({
        Monomial({"x": 2}): 4,
        Monomial(): 5,
    })

    assert p + q == Polynomial({
        Monomial({"x": 2}): 7,
        Monomial(): 7,
    })


def test_polynomial_addition_combines_like_terms():
    p = Polynomial({Monomial({"x": 2}): 3})
    q = Polynomial({Monomial({"x": 2}): -3})

    assert p + q == Polynomial.zero()


def test_polynomial_addition_with_scalar():
    p = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 2,
    })

    assert p + 5 == Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 7,
    })


def test_polynomial_subtraction():
    p = Polynomial({
        Monomial({"x": 2}): 5,
        Monomial(): 7,
    })

    q = Polynomial({
        Monomial({"x": 2}): 2,
        Monomial(): 3,
    })

    assert p - q == Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 4,
    })


def test_polynomial_negation():
    p = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): -5,
    })

    assert -p == Polynomial({
        Monomial({"x": 2}): -3,
        Monomial(): 5,
    })


# ---------------------------------------------------------------------------
# Polynomial multiplication
# ---------------------------------------------------------------------------


def test_polynomial_scalar_multiplication():
    p = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 2,
    })

    assert p * 2 == Polynomial({
        Monomial({"x": 2}): 6,
        Monomial(): 4,
    })


def test_polynomial_right_scalar_multiplication():
    p = Polynomial({
        Monomial({"x": 2}): 3,
        Monomial(): 2,
    })

    assert 2 * p == Polynomial({
        Monomial({"x": 2}): 6,
        Monomial(): 4,
    })


def test_polynomial_multiplication():
    x = Monomial({"x": 1})

    p = Polynomial({x: 2, Monomial(): 3})
    q = Polynomial({x: 1, Monomial(): 4})

    assert p * q == Polynomial({
        Monomial({"x": 2}): 2,
        Monomial(): 12,
        x: 11,
    })


def test_polynomial_multiplication_combines_like_terms():
    x = Monomial({"x": 1})

    p = Polynomial({x: 1, Monomial(): 1})
    q = Polynomial({x: 1, Monomial(): -1})

    assert p * q == Polynomial({
        Monomial({"x": 2}): 1,
        Monomial(): -1,
    })
