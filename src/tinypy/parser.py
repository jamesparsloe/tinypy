from abc import ABC, abstractmethod
from typing import Any
from tinypy.tokenizer import Token, TokenKind, tokenize


class Node(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor") -> Any: ...


class Expr(Node): ...


class Stmt(Node): ...


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"Literal({self.value})"


class GroupingExpr(Expr):
    def __init__(self, expr: Node):
        self.expr = expr

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_grouping_expr(self)

    def __repr__(self) -> str:
        return f"({self.expr})"


class BinaryExpr(Expr):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_binary_expr(self)

    def __repr__(self) -> str:
        return f"({self.left} {self.op} {self.right})"


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_expr_stmt(self)

    def __repr__(self) -> str:
        return self.expr.__repr__()


class PrintStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_print_stmt(self)

    def __repr__(self) -> str:
        return f"print({self.expr})"


class VarStmt(Stmt):
    def __init__(self, name: Token, type_annotation: Token, expr: Expr):
        self.name = name
        self.type_annotation = type_annotation
        self.expr = expr

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_var_stmt(self)

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_annotation} = {self.expr}"


class IfStmt(Stmt):
    def __init__(self, cond: Expr, if_branch: Stmt, else_branch: Stmt | None):
        self.cond = cond
        self.if_branch = if_branch
        self.else_branch = else_branch

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_if_stmt(self)


class Var(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: "Visitor"):
        return visitor.visit_var(self)

    def __repr__(self) -> str:
        return f"{self.name.value}"


class AssignStmt(Stmt):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: "Visitor"):
        return visitor.visit_assign_stmt(self)

    def __repr__(self) -> str:
        return f"{self.name.value} = {self.value}"


# NOTE: making it optional to implement all of these
class Visitor:
    def visit_literal(self, expr: Literal):
        raise NotImplementedError()

    def visit_grouping_expr(self, expr: GroupingExpr):
        raise NotImplementedError()

    def visit_binary_expr(self, expr: BinaryExpr):
        raise NotImplementedError()

    def visit_expr_stmt(self, stmt: ExprStmt):
        raise NotImplementedError()

    def visit_var_stmt(self, stmt: VarStmt):
        raise NotImplementedError()

    def visit_print_stmt(self, stmt: PrintStmt):
        raise NotImplementedError()

    def visit_var(self, expr: Var):
        raise NotImplementedError()

    def visit_assign_stmt(self, stmt: AssignStmt):
        raise NotImplementedError()

    def visit_if_stmt(self, stmt: IfStmt):
        raise NotImplementedError()


class Parser:
    def __init__(self, tokens: list[Token]):
        self.position = 0
        self.tokens = tokens

    def peek(self) -> Token:
        return self.tokens[self.position]

    def is_done(self):
        return self.peek().kind == TokenKind.EOF

    def check(self, kind: TokenKind):
        if self.is_done():
            return False
        else:
            return self.peek().kind == kind

    def previous(self):
        return self.tokens[self.position - 1]

    def advance(self):
        if not self.is_done():
            self.position += 1
        return self.previous()

    def match(self, *kinds: TokenKind):
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True

        return False

    def consume(self, kind: TokenKind):
        if self.check(kind):
            return self.advance()
        else:
            raise SyntaxError(f"Expected {kind} got {self.peek()}")

    def number(self):
        expr = None
        if self.match(TokenKind.INT, TokenKind.FLOAT):
            expr = Literal(self.previous().value)

        assert expr is not None

        return expr

    # NOTE: other compilers/interpreters can use "atomic" or "factor" for this
    def primary(self):
        if self.match(TokenKind.IDENTIFIER):
            return Var(self.previous())
        elif self.match(TokenKind.LEFT_PAREN):
            expr = self.expr()

            if not self.match(TokenKind.RIGHT_PAREN):
                raise SyntaxError("Expected ')' after expression")

            return GroupingExpr(expr)
        elif self.match(TokenKind.STR):
            expr = Literal(self.previous().value)
            return expr
        elif self.match(TokenKind.BOOL):
            expr = Literal(self.previous().value)
            return expr
        else:
            return self.number()

    def factor(self):
        expr = self.primary()

        while self.match(TokenKind.STAR, TokenKind.SLASH):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, op, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenKind.PLUS, TokenKind.MINUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, op, right)

        assert expr is not None

        return expr

    def expr(self) -> Expr:
        return self.term()

    def print_stmt(self):
        if not self.match(TokenKind.LEFT_PAREN):
            raise SyntaxError("Expected '(' after print")

        value = self.expr()

        if not self.match(TokenKind.RIGHT_PAREN):
            raise SyntaxError("Expected ')'")

        if not self.match(TokenKind.NEWLINE):
            raise SyntaxError("Expected '\n' after print statment")

        return PrintStmt(value)

    def var_stmt(self):
        if self.match(TokenKind.IDENTIFIER):
            if self.check(TokenKind.EQUAL):
                name = self.previous()
                _ = self.advance()
                value = self.expr()

                _ = self.consume(TokenKind.NEWLINE)
                return AssignStmt(name, value)
            else:
                name = self.previous()

                if not self.match(TokenKind.COLON):
                    raise SyntaxError("Expected ':' after variable name")

                # TODO: str etc
                if not self.match(
                    TokenKind.INT, TokenKind.FLOAT, TokenKind.STR, TokenKind.BOOL
                ):
                    raise SyntaxError("Expected type annotation")

                type_annotation = self.previous()

                if not self.match(TokenKind.EQUAL):
                    raise SyntaxError("Expected '=' after type annotation")

                expr = self.expr()

                _ = self.consume(TokenKind.NEWLINE)

                return VarStmt(name, type_annotation, expr)
        else:
            return self.stmt()

    def if_stmt(self):
        cond = self.expr()
        _ = self.consume(TokenKind.COLON)
        _ = self.consume(TokenKind.NEWLINE)
        _ = self.consume(TokenKind.INDENT)
        if_branch = self.stmt()
        _ = self.consume(TokenKind.DEDENT)  # don't forget dedents!
        else_branch = None
        if self.match(TokenKind.ELSE):
            _ = self.consume(TokenKind.COLON)
            _ = self.consume(TokenKind.NEWLINE)
            _ = self.consume(TokenKind.INDENT)
            else_branch = self.stmt()
            _ = self.consume(TokenKind.DEDENT)

        return IfStmt(cond, if_branch, else_branch)

    def stmt(self):
        if self.match(TokenKind.PRINT):
            return self.print_stmt()
        elif self.match(TokenKind.IF):
            return self.if_stmt()
        else:
            expr = self.expr()

            if not self.match(TokenKind.NEWLINE):
                raise SyntaxError("Expected '\n' after expression statement")

            return ExprStmt(expr)

    def parse(self) -> list[Stmt]:
        stmts = []

        while not self.is_done():
            stmts.append(self.var_stmt())

        return stmts


def parse(source: str):
    tokens = tokenize(source)
    print(tokens)
    parser = Parser(tokens)
    stmts = parser.parse()
    return stmts


class Evaluator(Visitor):
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr):
        return self.evaluate(expr.expr)

    def visit_binary_expr(self, expr: BinaryExpr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        kind = expr.op.kind

        if kind == TokenKind.PLUS:
            return left + right
        elif kind == TokenKind.MINUS:
            return left - right
        elif kind == TokenKind.STAR:
            return left * right
        elif kind == TokenKind.SLASH:
            return left / right
        else:
            return None


def evaluate(source: str):
    tokens = tokenize(source)
    parser = Parser(tokens)
    expr = parser.expr()
    evaluator = Evaluator()
    result = evaluator.evaluate(expr)
    return result
