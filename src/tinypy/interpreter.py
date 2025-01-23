from tinypy.tokenizer import TokenKind
from tinypy.parser import (
    Visitor,
    Stmt,
    Expr,
    Literal,
    Node,
    BinaryExpr,
    GroupingExpr,
    ExprStmt,
    PrintStmt,
    Variable,
    AssignmentStmt,
    parse,
)


class Interpreter(Visitor):
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

    def visit_variable(self, expr: Variable):
        # TODO: variable lookup
        return None

    def visit_assignment_stmt(self, expr: AssignmentStmt):
        value = self.evaluate(expr.value)
        # TODO: variable storage logic etc
        return None


def interpret(source: str):
    stmts = parse(source)
    interpreter = Interpreter()
    interpreter.interpret(stmts)
