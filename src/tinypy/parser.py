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

    def __repr__(self):
        return f"if {self.cond}: {self.if_branch} else: {self.else_branch}"


class BlockStmt(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_block_stmt(self)

    def __repr__(self) -> str:
        return f"BlockStmt({self.stmts})"


class CommentStmt(Stmt):
    def __init__(self, comment: Token):
        self.comment = comment

    def accept(self, visitor: "Visitor"):
        return visitor.visit_comment_stmt(self)


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


class FunctionStmt(Stmt):
    def __init__(
        self,
        name: Token,
        params: list[tuple[Token, Token]],
        return_type: Token,
        body: BlockStmt,
    ):
        self.name = name
        self.params = params  # List of (name, type) tuples
        self.return_type = return_type
        self.body = body

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_function_stmt(self)

    def __repr__(self) -> str:
        params_str = ", ".join(
            f"{name.value}: {type_.value}" for name, type_ in self.params
        )
        return f"def {self.name.value}({params_str}) -> {self.return_type.value}: {self.body}"


class CallExpr(Expr):
    def __init__(self, callee: Token, arguments: list[Expr]):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_call_expr(self)

    def __repr__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.callee}({args_str})"


class ReturnStmt(Stmt):
    def __init__(self, keyword: Token, value: Expr | None):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_return_stmt(self)

    def __repr__(self) -> str:
        return f"return {self.value}" if self.value else "return"


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

    def visit_block_stmt(self, stmt: BlockStmt):
        raise NotImplementedError()

    def visit_comment_stmt(self, stmt: CommentStmt):
        raise NotImplementedError()

    def visit_function_stmt(self, stmt: FunctionStmt):
        raise NotImplementedError()

    def visit_call_expr(self, expr: CallExpr):
        raise NotImplementedError()

    def visit_return_stmt(self, stmt: ReturnStmt):
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
            raise SyntaxError(f"Expected '{kind}', but got '{self.peek()}' instead")

    def consume_empty_lines(self):
        while self.match(TokenKind.NEWLINE):
            ...

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
        elif self.match(TokenKind.INT, TokenKind.FLOAT, TokenKind.BOOL, TokenKind.STR):
            expr = Literal(self.previous().value)
            return expr
        else:
            raise Exception("Should be unreachable!")

    def factor(self):
        expr = self.call_expr()

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

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenKind.GREATER,
            TokenKind.GREATER_EQUALS,
            TokenKind.LESS,
            TokenKind.LESS_EQUALS,
        ):
            op = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, op, right)

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenKind.DOUBLE_EQUALS, TokenKind.NOT_EQUALS):
            op = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, op, right)

        return expr

    def expr(self) -> Expr:
        return self.equality()

    def print_stmt(self):
        if not self.match(TokenKind.LEFT_PAREN):
            raise SyntaxError("Expected '(' after print")

        value = self.expr()

        if not self.match(TokenKind.RIGHT_PAREN):
            raise SyntaxError("Expected ')'")

        if not self.match(TokenKind.NEWLINE):
            raise SyntaxError("Expected newline after print statment")

        return PrintStmt(value)

    def var_stmt(self):
        if self.match(TokenKind.IDENTIFIER):
            if self.check(TokenKind.EQUALS):
                name = self.previous()
                _ = self.advance()
                value = self.expr()

                _ = self.consume(TokenKind.NEWLINE)

                return AssignStmt(name, value)
            elif self.check(TokenKind.COLON):
                name = self.previous()

                _ = self.advance()

                if not self.match(
                    TokenKind.INT, TokenKind.FLOAT, TokenKind.STR, TokenKind.BOOL
                ):
                    raise SyntaxError("Expected type annotation")

                type_annotation = self.previous()

                if not self.match(TokenKind.EQUALS):
                    raise SyntaxError("Expected '=' after type annotation")

                expr = self.expr()

                _ = self.consume(TokenKind.NEWLINE)

                return VarStmt(name, type_annotation, expr)
            else:
                # NOTE: I assume backtracking is bad and I should maybe check?
                self.position -= 1
                return self.stmt()
        else:
            return self.stmt()

    def if_stmt(self):
        cond = self.expr()
        _ = self.consume(TokenKind.COLON)
        _ = self.consume(TokenKind.NEWLINE)

        if_branch = self.block_stmt()

        else_branch = None
        if self.match(TokenKind.ELSE):
            _ = self.consume(TokenKind.COLON)
            _ = self.consume(TokenKind.NEWLINE)
            else_branch = self.block_stmt()

        return IfStmt(cond, if_branch, else_branch)

    def expr_stmt(self):
        expr = self.expr()
        _ = self.consume(TokenKind.NEWLINE)
        return ExprStmt(expr)

    def block_stmt(self):
        self.consume_empty_lines()

        _ = self.consume(TokenKind.INDENT)

        stmts = []

        while not self.check(TokenKind.DEDENT):
            stmts.append(self.var_stmt())
            self.consume_empty_lines()

        _ = self.consume(TokenKind.DEDENT)

        self.consume_empty_lines()

        return BlockStmt(stmts)

    def stmt(self):
        if self.match(TokenKind.DEF):
            return self.function_stmt()
        elif self.match(TokenKind.RETURN):
            keyword = self.previous()
            value = self.expr()
            stmt = ReturnStmt(keyword, value)
            _ = self.consume(TokenKind.NEWLINE)
            return stmt
        elif self.match(TokenKind.PRINT):
            return self.print_stmt()
        elif self.match(TokenKind.IF):
            return self.if_stmt()
        elif self.match(TokenKind.COMMENT):
            stmt = CommentStmt(self.previous())
            _ = self.consume(TokenKind.NEWLINE)
            return stmt
        else:
            return self.expr_stmt()

    def function_stmt(self):
        name = self.consume(TokenKind.IDENTIFIER)

        self.consume(TokenKind.LEFT_PAREN)
        params = []

        if not self.check(TokenKind.RIGHT_PAREN):
            while True:
                param_name = self.consume(TokenKind.IDENTIFIER)
                _ = self.consume(TokenKind.COLON)

                if not self.match(
                    TokenKind.INT, TokenKind.FLOAT, TokenKind.STR, TokenKind.BOOL
                ):
                    raise SyntaxError()

                param_type = self.previous()

                params.append((param_name, param_type))

                if not self.match(TokenKind.COMMA):
                    break

        self.consume(TokenKind.RIGHT_PAREN)
        self.consume(TokenKind.ARROW)

        if not self.match(
            TokenKind.INT, TokenKind.FLOAT, TokenKind.BOOL, TokenKind.STR
        ):
            raise SyntaxError()

        return_type = self.previous()

        self.consume(TokenKind.COLON)
        self.consume(TokenKind.NEWLINE)

        body = self.block_stmt()

        return FunctionStmt(name, params, return_type, body)

    def call_expr(self):
        expr = self.primary()

        while True:
            if self.match(TokenKind.LEFT_PAREN):
                arguments = []
                if not self.check(TokenKind.RIGHT_PAREN):
                    while True:
                        arguments.append(self.expr())
                        if not self.match(TokenKind.COMMA):
                            break

                _ = self.consume(TokenKind.RIGHT_PAREN)
                expr = CallExpr(expr.name, arguments)
            else:
                break

        return expr

    def parse(self) -> list[Stmt]:
        stmts = []

        self.consume_empty_lines()

        while not self.is_done():
            stmts.append(self.var_stmt())
            self.consume_empty_lines()

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
    expr = parser.expr()
    evaluator = Evaluator()
    result = evaluator.evaluate(expr)
    return result
