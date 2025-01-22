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
    NEWLINE = "newline"
    INDENT = "indent"
    DEDENT = "dedent"

    INT = "int"

    DEF = "def"
    RETURN = "return"
    IDENTIFIER = "identifier"

    EOF = "eof"


@dataclass
class Token:
    kind: TokenKind
    line: int
    text: str = ""
    value: object | None = None


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.start = 0
        self.line = 1
        self.tokens = []
        self.character = self.source[self.position]

    def advance(self):
        c = self.source[self.position]
        self.position += 1
        return c

    def add_token(self, kind: TokenKind, value: object | None = None):
        text = self.source[self.start : self.position]
        token = Token(kind=kind, line=self.line, text=text, value=value)
        self.tokens.append(token)

    def tokenize(self) -> list[Token]:
        while not self.is_done():
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
            else:
                ...

        self.tokens.append(Token(kind=TokenKind.EOF, line=self.line))

        return self.tokens

    def is_done(self):
        return self.position >= len(self.source)


def tokenize(source: str):
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    return tokens


def run(source: str):
    print(source)


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
