import pytest
from tinypy.parser import evaluate


@pytest.mark.parametrize(
    "source",
    [
        # Basic arithmetic
        "10 + 1",
        "(10 + 1)",
        "((10 + (1 + (1 + 10))))",
        "10 + 2.9 * 4 / 3.4 - 1.2 + 1",
        "(10.7 + 3.1) * 2",
        # Unary minus
        "-5",
        "-(-10)",
        "5 + -3",
        # Floor division
        "17 // 5",
        "10 // 3",
        "-17 // 5",
        "7.5 // 2.0",
        # Modulo
        "17 % 5",
        "10 % 3",
        "-17 % 5",
        "7.5 % 2.0",
        # Exponentiation
        "2 ** 3",
        "2 ** 10",
        "3.0 ** 2.0",
        "2 ** 0",
        "(-2) ** 3",
    ],
)
def test_arithmetic(source: str):
    actual = evaluate(source)
    expected = eval(source)
    assert actual == expected


@pytest.mark.parametrize(
    "source",
    [
        # Right-associative: 2 ** 3 ** 2 = 2 ** (3 ** 2) = 2 ** 9 = 512
        "2 ** 3 ** 2",
        "3 ** 3 ** 1",
    ],
)
def test_exponentiation_right_associative(source: str):
    actual = evaluate(source)
    expected = eval(source)
    assert actual == expected


@pytest.mark.parametrize(
    "source",
    [
        # ** has higher precedence than unary minus: -2 ** 2 = -(2 ** 2) = -4
        "-2 ** 2",
        "-3 ** 2",
    ],
)
def test_exponentiation_precedence(source: str):
    actual = evaluate(source)
    expected = eval(source)
    assert actual == expected


@pytest.mark.parametrize(
    "source",
    [
        # Operator precedence: ** > * / // % > + -
        "2 + 3 * 4",
        "2 * 3 + 4",
        "10 - 6 / 2",
        "2 ** 3 * 4",
        "4 * 2 ** 3",
        "10 + 5 % 3",
        "10 + 8 // 3",
        "2 ** 3 + 4 * 5 - 6 // 2",
    ],
)
def test_operator_precedence(source: str):
    actual = evaluate(source)
    expected = eval(source)
    assert actual == expected
