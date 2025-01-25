from enum import StrEnum
from dataclasses import dataclass


class TokenKind(StrEnum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    COLON = ":"
    EQUAL = "="
    PLUS = "+"
    STAR = "*"
    SLASH = "/"
    MINUS = "-"
    LESS_THAN = "<"
    ARROW = "->"

    NEWLINE = "newline"
    INDENT = "indent"
    DEDENT = "dedent"

    INT = "int"
    FLOAT = "float"

    IF = "if"
    ELSE = "else"
    PRINT = "print"

    DEF = "def"
    RETURN = "return"
    IDENTIFIER = "identifier"

    EOF = "eof"


KEYWORDS = {
    "int": TokenKind.INT,
    "float": TokenKind.FLOAT,
    "print": TokenKind.PRINT,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "def": TokenKind.DEF,
    "return": TokenKind.RETURN,
}


@dataclass
class Token:
    kind: TokenKind
    line: int
    text: str = ""
    value: object | None = None

    def __repr__(self) -> str:
        if self.value is not None and self.value not in KEYWORDS:
            return f"{self.kind}({self.value})"
        else:
            return self.kind


INDENT_SPACES = 4


class Tokenizer:
    def __init__(self, source: str):
        # TODO: is this okay?
        if source[-1] != "\n":
            source += "\n"
        self.source = source
        self.position = 0
        self.start = 0
        self.line = 1
        self.tokens: list[Token] = []
        self.character = self.source[self.position]
        self.indent_stack: list[int] = [0]

    # NOTE: also seen this in various places as `consume`
    def advance(self):
        c = self.source[self.position]
        self.position += 1
        return c

    # NOTE: peek **doesn't** consume the character
    def peek(self):
        if self.is_done():
            return "\0"
        else:
            return self.source[self.position]

    def match(self, expected: str):
        if self.is_done():
            return False
        elif self.source[self.position] != expected:
            return False
        else:
            self.position += 1
            return True

    def whitespace(self):
        spaces = 0
        while self.peek() == " ":
            spaces += 1
            self.advance()

        if self.peek() == "\t":
            raise Exception(f"line {self.line}: tabs are currently forbidden in tinypy")

        if len(self.tokens) > 0 and self.tokens[-1].kind != TokenKind.NEWLINE:
            return

        indent_level, rem = divmod(spaces, INDENT_SPACES)
        assert rem == 0, "Invalid indent"

        current_level = self.indent_stack[-1]

        if indent_level > current_level:
            self.indent_stack.append(indent_level)
            self.add_token(TokenKind.INDENT)
        elif indent_level < current_level:
            while indent_level < current_level:
                self.indent_stack.pop()
                self.add_token(TokenKind.DEDENT)
                current_level = self.indent_stack[-1]

    def add_token(self, kind: TokenKind, value: object | None = None):
        text = self.source[self.start : self.position]
        token = Token(kind=kind, line=self.line, text=text, value=value)
        self.tokens.append(token)

    def tokenize(self) -> list[Token]:
        while not self.is_done():
            self.start = self.position

            if len(self.tokens) == 0 or self.tokens[-1].kind == TokenKind.NEWLINE:
                self.whitespace()

                if self.peek() == "\n":
                    self.advance()
                    self.line += 1
                    continue

                # HACK
                self.start = self.position

            c = self.advance()

            if c == "(":
                self.add_token(TokenKind.LEFT_PAREN)
            elif c == ")":
                self.add_token(TokenKind.RIGHT_PAREN)
            elif c == ":":
                self.add_token(TokenKind.COLON)
            elif c == "+":
                self.add_token(TokenKind.PLUS)
            elif c == "*":
                self.add_token(TokenKind.STAR)
            elif c == "/":
                self.add_token(TokenKind.SLASH)
            elif c == "<":
                self.add_token(TokenKind.LESS_THAN)
            elif c == "#":
                # swallow comments for now
                while self.peek() != "\n" and not self.is_done():
                    self.advance()
            elif c == "\n":
                # TODO: line number for new line??
                self.add_token(TokenKind.NEWLINE)
                self.line += 1
            elif c == " ":
                ...
            elif c == "-":
                if self.match(">"):
                    self.add_token(TokenKind.ARROW)
                else:
                    self.add_token(TokenKind.MINUS)
            elif c == "=":
                self.add_token(TokenKind.EQUAL)
            elif c.isdigit():
                while self.peek().isdigit():
                    self.advance()

                if self.peek() == ".":
                    self.advance()  # consume the decimal point

                    if not self.peek().isdigit():
                        raise Exception(
                            f"line {self.line}. Expected digit after decimal point"
                        )

                    while self.peek().isdigit():
                        self.advance()

                    text = self.source[self.start : self.position]

                    value = float(text)

                    self.add_token(TokenKind.FLOAT, value=value)
                else:
                    text = self.source[self.start : self.position]
                    value = int(text)
                    self.add_token(TokenKind.INT, value=value)
            elif c.isalpha() or c == "_":
                while self.peek().isalpha() or self.peek() == "_":
                    self.advance()
                text = self.source[self.start : self.position]
                # NOTE: we can also produce the int/float type annotations here - they just will not be associated with a value unlike the literals
                kind = KEYWORDS.get(text, TokenKind.IDENTIFIER)
                self.add_token(kind, value=text)
            else:
                # TODO: proper error handling
                print(f"line {self.line} {self.tokens}")
                raise Exception(f"Did not handle '{c}' in tokenize")

        self.tokens.append(Token(kind=TokenKind.EOF, line=self.line))

        return self.tokens

    def is_done(self):
        return self.position >= len(self.source)


def tokenize(source: str):
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    return tokens
