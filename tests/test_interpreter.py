import pytest
from tinypy.interpreter import interpret


@pytest.mark.parametrize(
    "source",
    [
        "10 + 1",
        "(10 + 1)",
        "((10 + (1 + (1 + 10))))",
        "10 + 2.9 * 4 / 3.4 - 1.2 + 1",
        "(10.7 + 3.1) * 2",
        "10.4 - 1\n(17.4 - 3) * 2",
        "print(10 + 1)\n6.7 - 1",
    ],
)
def test_interpret(source: str):
    interpret(source)
