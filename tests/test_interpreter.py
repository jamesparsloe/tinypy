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
def test_logical_operators(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    # Get the last print call's argument
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ("x: int = 5\nprint(x)", "5"),
        ("x: float = 3.14\nprint(x)", "3.14"),
        ('x: str = "hello"\nprint(x)', "hello"),
        ("x: bool = True\nprint(x)", "True"),
    ],
)
def test_variable_declaration(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ("x: int = 5\nx = 10\nprint(x)", "10"),
        ("x: int = 1\nx = x + 1\nprint(x)", "2"),
    ],
)
def test_variable_reassignment(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ("x: int = 5\nif x > 3:\n    print(1)", "1"),
        ("x: int = 2\nif x > 3:\n    print(1)\nelse:\n    print(0)", "0"),
        # Nested if/else
        (
            "x: int = 5\nif x > 3:\n    if x > 4:\n        print(2)\n    else:\n        print(1)",
            "2",
        ),
    ],
)
def test_if_else_statements(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


@pytest.mark.parametrize(
    "source,expected_output",
    [
        # Simple function, no params
        ("def greet() -> int:\n    print(42)\n    return 0\ngreet()", "42"),
        # Function with parameter
        ("def double(x: int) -> int:\n    return x * 2\nprint(double(5))", "10"),
        # Function returning expression
        ("def square(n: int) -> int:\n    return n * n\nprint(square(4))", "16"),
    ],
)
def test_function_definitions(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ("def get_five() -> int:\n    return 5\nprint(get_five())", "5"),
        # Note: early return requires else branch (interpreter limitation)
        (
            "def sign(x: int) -> int:\n    if x > 0:\n        return 1\n    else:\n        return 0\nprint(sign(5))",
            "1",
        ),
        (
            "def sign(x: int) -> int:\n    if x > 0:\n        return 1\n    else:\n        return 0\nprint(sign(-5))",
            "0",
        ),
    ],
)
def test_return_statements(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


def test_recursive_factorial(mocker):
    # Note: uses else branch due to interpreter early-return limitation
    source = (
        "def factorial(n: int) -> int:\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    else:\n"
        "        return n * factorial(n - 1)\n"
        "print(factorial(5))"
    )
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called_with(120)


def test_recursive_fibonacci(mocker):
    # Note: uses else branch due to interpreter early-return limitation
    source = (
        "def fib(n: int) -> int:\n"
        "    if n <= 1:\n"
        "        return n\n"
        "    else:\n"
        "        return fib(n - 1) + fib(n - 2)\n"
        "print(fib(10))"
    )
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called_with(55)


@pytest.mark.parametrize(
    "source,expected_output",
    [
        ('x: str = "hello"\nprint(x)', "hello"),
        ('print("hello" + " " + "world")', "hello world"),
        ('x: str = "a"\ny: str = "b"\nprint(x + y)', "ab"),
    ],
)
def test_string_operations(source: str, expected_output: str, mocker):
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called()
    last_call_args = mock_print.call_args_list[-1][0]
    assert str(last_call_args[0]) == expected_output


def test_multi_param_functions(mocker):
    """Functions with multiple parameters should work"""
    source = "def add(a: int, b: int) -> int:\n    return a + b\nprint(add(3, 4))"
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called_with(7)


def test_none_return_type(mocker):
    """Functions with -> None return type should work"""
    source = "def greet() -> None:\n    print(42)\ngreet()"
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called_with(42)


def test_early_return(mocker):
    """Return inside if should exit function without needing else"""
    source = (
        "def sign(x: int) -> int:\n"
        "    if x > 0:\n"
        "        return 1\n"
        "    return 0\n"
        "print(sign(5))"
    )
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    mock_print.assert_called_with(1)


def test_composing_functions(mocker):
    """Using the result of one function call as an argument to another"""
    source = (
        "def add(a: int, b: int) -> int:\n"
        "    return a + b\n"
        "\n"
        "def mul(a: int, b: int) -> int:\n"
        "    return a * b\n"
        "\n"
        "def main() -> None:\n"
        "    a: int = 10\n"
        "    b: int = 20\n"
        "\n"
        "    c: int = add(a, b)\n"
        "    d: int = mul(3, c)\n"
        "\n"
        "    print(d)\n"
        "\n"
        "main()"
    )
    mock_print = mocker.patch("builtins.print")
    interpret(source)
    # (10 + 20) * 3 = 90
    mock_print.assert_called_with(90)
