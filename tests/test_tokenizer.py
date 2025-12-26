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
        (
            "not True",
            [
                Token(kind=TokenKind.NOT, value="not"),
                Token(kind=TokenKind.BOOL, value=True),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "True and False",
            [
                Token(kind=TokenKind.BOOL, value=True),
                Token(kind=TokenKind.AND, value="and"),
                Token(kind=TokenKind.BOOL, value=False),
                Token(kind=TokenKind.NEWLINE),
                Token(kind=TokenKind.EOF),
            ],
        ),
        (
            "True or False",
            [
                Token(kind=TokenKind.BOOL, value=True),
                Token(kind=TokenKind.OR, value="or"),
                Token(kind=TokenKind.BOOL, value=False),
                Token(kind=TokenKind.NEWLINE),
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


def test_string_escape_sequences():
    """Test that escape sequences in strings are properly handled"""
    # Test newline escape
    tokens = tokenize('"Hello\\nWorld"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "Hello\nWorld"

    # Test tab escape
    tokens = tokenize('"Column1\\tColumn2"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "Column1\tColumn2"

    # Test backslash escape
    tokens = tokenize('"Path\\\\to\\\\file"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "Path\\to\\file"

    # Test quote escape
    tokens = tokenize('"She said \\"Hello\\""')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == 'She said "Hello"'

    # Test multiple escapes
    tokens = tokenize('"Line1\\nLine2\\tTabbed\\\\Backslash"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "Line1\nLine2\tTabbed\\Backslash"


def test_unterminated_string_error():
    """Test that unterminated strings raise SyntaxError"""
    with pytest.raises(SyntaxError, match="Unterminated string literal"):
        tokenize('"this string is not closed')

    with pytest.raises(SyntaxError, match="Unterminated string literal"):
        tokenize('"escape at end\\')


def test_unknown_escape_sequences():
    """Test that unknown escape sequences are treated literally"""
    tokens = tokenize('"\\x unknown escape"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "x unknown escape"

    tokens = tokenize('"\\z invalid"')
    assert tokens[0].kind == TokenKind.STR
    assert tokens[0].value == "z invalid"
