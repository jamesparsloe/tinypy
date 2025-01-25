from typing import Any
from tinypy.tokenizer import TokenKind
from tinypy.parser import (
    Var,
    Visitor,
    Stmt,
    Expr,
    Literal,
    Node,
    BinaryExpr,
    GroupingExpr,
    ExprStmt,
    PrintStmt,
    VarStmt,
    parse,
    AssignStmt,
)


class Interpreter(Visitor):
    def __init__(self):
        self.values: dict[str, Any] = {}

    def interpret(self, stmts: list[Stmt]):
        for stmt in stmts:
            self.execute(stmt)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

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

    def visit_expr_stmt(self, stmt: ExprStmt):
        value = self.evaluate(stmt.expr)

    def visit_print_stmt(self, stmt: PrintStmt):
        value = self.evaluate(stmt.expr)
        print(value)

    def visit_var_stmt(self, stmt: VarStmt):
        name = stmt.name.text

        if name in self.values:
            raise Exception(f"{name} has already been defined")
        else:
            value = self.evaluate(stmt.expr)
            self.values[name] = value

    def visit_var(self, expr: Var):
        value = self.values.get(expr.name.value)

        if value is None:
            raise Exception(f"Variable {expr.name.value} is not defined")

        return value

    # TODO: there's no type checking
    def visit_assign_stmt(self, stmt: AssignStmt):
        name = stmt.name.value
        curr_value = self.values.get(name)

        if curr_value is None:
            raise Exception(f"Variable {stmt.name.value} is not defined")

        value = self.evaluate(stmt.value)

        self.values[name] = value


def interpret(source: str):
    stmts = parse(source)
    interpreter = Interpreter()
    interpreter.interpret(stmts)
