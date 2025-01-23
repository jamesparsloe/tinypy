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


class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_variable(self)


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


class AssignmentStmt(Stmt):
    def __init__(self, name: Token, type_annotation: Token, value: Node):
        self.name = name
        self.type_annotation = type_annotation
        self.value = value

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_assignment_stmt(self)

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_annotation} = {self.value}"


class Visitor:
    def visit_literal(self, expr: Literal):
        pass

    def visit_grouping_expr(self, expr: GroupingExpr):
        pass

    def visit_binary_expr(self, expr: BinaryExpr):
        pass

    def visit_variable(self, expr: Variable):
        pass

    def visit_expr_stmt(self, stmt: ExprStmt):
        pass

    def visit_print_stmt(self, stmt: PrintStmt):
        pass

    def visit_assignment_stmt(self, stmt: AssignmentStmt):
        pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.position = 0
        self.tokens = tokens

    def check(self, kind: TokenKind):
        if self.is_done():
            return False
        else:
            return self.peek().kind == kind

    def match(self, *kinds: TokenKind):
        for kind in kinds:
            if self.check(kind):
                self.advance()
                return True

        return False

    def previous(self):
        return self.tokens[self.position - 1]

    def advance(self):
        if not self.is_done():
            self.position += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.position]

    def is_done(self):
        return self.peek().kind == TokenKind.EOF

    # NOTE: other compilers/interpreters can use "atomic" or "factor" for this
    def primary(self):
        if self.match(TokenKind.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(TokenKind.LEFT_PAREN):
            expr = self.expression()

            if not self.match(TokenKind.RIGHT_PAREN):
                raise SyntaxError("Expected ')' after expression")

            return GroupingExpr(expr)
        else:
            return self.number()

    def number(self):
        expr = None
        if self.match(TokenKind.INT, TokenKind.FLOAT):
            expr = Literal(self.previous().value)

        assert expr is not None

        return expr

    def factor(self):
        expr = self.primary()

        while self.match(TokenKind.STAR, TokenKind.SLASH):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, op, right)

        assert expr is not None

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenKind.PLUS, TokenKind.MINUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, op, right)

        assert expr is not None

        return expr

    # TODO: I don't really like the naming of these things at all
    # def assignment(self) -> Node:
    #     if self.match(TokenKind.IDENTIFIER):
    #         name = self.previous()

    #         if not self.match(TokenKind.COLON):
    #             raise SyntaxError("Expected ':' after variable name")

    #         if not self.match(TokenKind.INT, TokenKind.FLOAT):  # For type annotation
    #             raise SyntaxError("Expected type annotation")

    #         type_annotation = self.previous()

    #         if not self.match(TokenKind.EQUAL):
    #             raise SyntaxError("Expected '=' after type annotation")

    #         value = self.expression()
    #         return AssignmentStmt(name, type_annotation, value)
    #     else:
    #         return self.term()

    def expression(self) -> Expr:
        return self.term()

    def print_statement(self):
        value = self.expression()

        if not self.match(TokenKind.RIGHT_PAREN):
            raise SyntaxError("Expected ')'")

        if not self.match(TokenKind.NEWLINE):
            raise SyntaxError("Expected '\n' after print statment")

        return PrintStmt(value)

    def statement(self):
        if self.match(TokenKind.PRINT):
            if not self.match(TokenKind.LEFT_PAREN):
                raise SyntaxError("Expected '(' after print")

            return self.print_statement()
        else:
            expr = self.expression()

            if not self.match(TokenKind.NEWLINE):
                raise SyntaxError("Expected '\n' after expression statement")

            return ExprStmt(expr)

    def parse(self) -> list[Stmt]:
        stmts = []

        while not self.is_done():
            stmts.append(self.statement())

        return stmts


def parse(source: str):
    tokens = tokenize(source)
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
    expr = parser.expression()
    evaluator = Evaluator()
    result = evaluator.evaluate(expr)
    return result
