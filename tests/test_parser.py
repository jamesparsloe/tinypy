import pytest
from tinypy.parser import evaluate


@pytest.mark.parametrize(
    "source",
    [
        "10 + 1",
        "(10 + 1)",
        "((10 + (1 + (1 + 10))))",
        "10 + 2.9 * 4 / 3.4 - 1.2 + 1",
        "(10.7 + 3.1) * 2",
        # Logical operators
        "not True",
        "not False",
        "True and False",
        "True and True",
        "False or False",
        "True or False",
        "not (True and False)",
        "True and (False or True)",
        # Unary minus
        "-5",
        "-(-10)",
        "5 + -3",
    ],
)
def test_evaluate_arithmetic(source: str):
    actual = evaluate(source)
    expected = eval(source)
    assert actual == expected
