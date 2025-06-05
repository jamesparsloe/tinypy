import pytest
from tinypy.interpreter import interpret
from unittest.mock import patch, call


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


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ("print(not True)", "False"),
        ("print(not False)", "True"),
        ("print(True and False)", "False"),
        ("print(True and True)", "True"),
        ("print(False or False)", "False"),
        ("print(True or False)", "True"),
        ("print(not (True and False))", "True"),
        ("print(True and (False or True))", "True"),
        ("x: bool = True\nprint(not x)", "False"),
        ("x: bool = True\ny: bool = False\nprint(x and y)", "False"),
        ("x: bool = True\ny: bool = False\nprint(x or y)", "True"),
        # Test with comparisons
        ("x: int = 5\ny: int = 3\nprint((x > y) and (y > 0))", "True"),
        ("x: int = 5\ny: int = 3\nprint((x < y) or (y == 3))", "True"),
        # Test unary minus
        ("print(-5)", "-5"),
        ("x: int = 10\nprint(-x)", "-10"),
        ("print(-(-5))", "5"),
    ],
)
def test_logical_operators(source: str, expected_output: str):
    with patch("builtins.print") as mock_print:
        interpret(source)
        # Get the last print call's argument
        mock_print.assert_called()
        last_call_args = mock_print.call_args_list[-1][0]
        assert str(last_call_args[0]) == expected_output
