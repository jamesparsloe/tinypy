from tinypy.tokenizer import tokenize, Token, TokenKind
import pytest


@pytest.mark.parametrize(
    "source,expected",
    [
        (
            "1 + 2",
            [
                Token(kind=TokenKind.INT, value=1),
                Token(kind=TokenKind.PLUS),
                Token(kind=TokenKind.INT, value=2),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "x: int = 1",
            [
                Token(kind=TokenKind.IDENTIFIER, value="x"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.INT, value="int"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.INT, value=1),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "y: float = 42.0",
            [
                Token(kind=TokenKind.IDENTIFIER, value="y"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.FLOAT, value="float"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.FLOAT, value=42.0),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "x: int = 1 + 2",
            [
                Token(kind=TokenKind.IDENTIFIER, value="x"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.INT, value="int"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.INT, value=1),
                Token(kind=TokenKind.PLUS),
                Token(kind=TokenKind.INT, value=2),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "x: bool = True\ny: int = 42\nif x:\n    y = y + 10",
            [
                Token(kind=TokenKind.IDENTIFIER, value="x"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.BOOL, value="bool"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.BOOL, value=True),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.IDENTIFIER, value="y"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.INT, value="int"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.INT, value=42),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.IF, value="if"),
                Token(kind=TokenKind.IDENTIFIER, value="x"),
                Token(kind=TokenKind.COLON),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.INDENT),
                Token(kind=TokenKind.IDENTIFIER, value="y"),
                Token(kind=TokenKind.EQUALS),
                Token(kind=TokenKind.IDENTIFIER, value="y"),
                Token(kind=TokenKind.PLUS),
                Token(kind=TokenKind.INT, value=10),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.DEDENT),
                Token(kind=TokenKind.EOF),
            ],
        ),
    ],
)
def test_tokenizer(source, expected):
    tokens = tokenize(source)
    assert len(tokens) == len(expected)

    for token, expected_token in zip(tokens, expected):
        assert token.kind == expected_token.kind
        assert token.value == expected_token.value
