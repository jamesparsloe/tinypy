import pytest
from tinypy.parser import evaluate, parse, VarStmt
from tinypy.tokenizer import TokenKind


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


def test_parse_union_type():
    """Test that union type annotations are parsed correctly."""
    stmts = parse("x: int | None = None")
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, VarStmt)
    assert stmt.name.value == "x"
    assert len(stmt.type_annotation) == 2
    assert stmt.type_annotation[0].kind == TokenKind.INT
    assert stmt.type_annotation[1].kind == TokenKind.NONE


def test_parse_multiple_union_types():
    """Test that multiple union types are parsed correctly."""
    stmts = parse("x: int | str | float = 1")
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, VarStmt)
    assert len(stmt.type_annotation) == 3
    assert stmt.type_annotation[0].kind == TokenKind.INT
    assert stmt.type_annotation[1].kind == TokenKind.STR
    assert stmt.type_annotation[2].kind == TokenKind.FLOAT
