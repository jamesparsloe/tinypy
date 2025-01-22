import sys
from enum import StrEnum
from dataclasses import dataclass

__version__ = "0.1.0"
USAGE = "usage: tinypy or tinypy script.py"


class TokenKind(StrEnum):
    L_PAREN = "("
    R_PAREN = ")"
    COLON = ":"
    PLUS = "+"
    MINUS = "-"
    LESS_THAN = "<"
    ARROW = "->"

    NEWLINE = "newline"
    INDENT = "indent"
    DEDENT = "dedent"

    INT = "int"

    IF = "if"
    ELSE = "else"

    DEF = "def"
    RETURN = "return"
    IDENTIFIER = "identifier"

    EOF = "eof"


KEYWORDS = {
    "int": TokenKind.INT,
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
            return f"{self.kind} {self.value}"
        else:
            return self.kind


INDENT_SPACES = 4


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.start = 0
        self.line = 1
        self.tokens: list[Token] = []
        self.character = self.source[self.position]
        self.indent_stack: list[int] = [0]

    # NOTE(james): also seen this in various places as `consume`
    def advance(self):
        c = self.source[self.position]
        self.position += 1
        return c

    # NOTE(james): peek **doesn't** consume the character
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

        print(f"{indent_level=} {current_level=} {self.indent_stack}")

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

                # FIXME(james)
                self.start = self.position

            c = self.advance()

            if c == "(":
                self.add_token(TokenKind.L_PAREN)
            elif c == ")":
                self.add_token(TokenKind.R_PAREN)
            elif c == ":":
                self.add_token(TokenKind.COLON)
            elif c == "+":
                self.add_token(TokenKind.PLUS)
            elif c == "<":
                self.add_token(TokenKind.LESS_THAN)
            elif c == "\n":
                # TODO(james): line number for new line??
                self.add_token(TokenKind.NEWLINE)
                self.line += 1
            elif c == " ":
                ...
            elif c == "-":
                if self.match(">"):
                    self.add_token(TokenKind.ARROW)
                else:
                    self.add_token(TokenKind.MINUS)
            elif c.isdigit():
                while self.peek().isdigit():
                    self.advance()
                text = self.source[self.start : self.position]
                value = int(text)
                self.add_token(TokenKind.INT, value=value)
            elif c.isalpha() or c == "_":
                while self.peek().isalpha() or self.peek() == "_":
                    self.advance()
                text = self.source[self.start : self.position]
                kind = KEYWORDS.get(text, TokenKind.IDENTIFIER)
                print(kind, text)
                self.add_token(kind, value=text)
            else:
                # TODO(james): proper error handling
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


def run(source: str):
    tokens = tokenize(source)
    for token in tokens:
        print(token)


def run_repl():
    print(f"tinypy {__version__}")
    while True:
        try:
            source = input(">>> ")
            run(source)
        except EOFError:
            print()
            break


def run_script(file: str):
    with open(file, "r") as f:
        source = f.read()

    run(source)


def main() -> None:
    args = sys.argv[1:]

    # TODO(james) correct error codes
    if len(args) == 0:
        run_repl()
    elif len(args) == 1:
        if args[0] in ("-v", "--version"):
            print(f"tinypy {__version__}")
        elif args[0] in ("-h", "--help"):
            print(USAGE)
        else:
            run_script(args[0])
    else:
        print(USAGE)
