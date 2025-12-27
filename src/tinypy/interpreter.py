from typing import Any
from tinypy.tokenizer import TokenKind


class Return(Exception):
    """Exception used to unwind the stack when a return statement is executed."""

    def __init__(self, value: Any):
        self.value = value


from tinypy.parser import (
    CallExpr,
    IfStmt,
    Var,
    Visitor,
    Stmt,
    Expr,
    Literal,
    BinaryExpr,
    UnaryExpr,
    GroupingExpr,
    ExprStmt,
    PrintStmt,
    VarStmt,
    parse,
    AssignStmt,
    BlockStmt,
    CommentStmt,
    FunctionStmt,
    ReturnStmt,
)


class Interpreter(Visitor):
    def __init__(self):
        self.values: dict[str, Any] = {}
        self.functions: dict[str, FunctionStmt] = {}

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

        # FIXME: must be a better way
        if isinstance(left, str) or isinstance(right, str):
            left = str(left)
            right = str(right)

        if kind == TokenKind.PLUS:
            return left + right
        elif kind == TokenKind.MINUS:
            return left - right
        elif kind == TokenKind.STAR:
            return left * right
        elif kind == TokenKind.SLASH:
            return left / right
        elif kind == TokenKind.DOUBLE_SLASH:
            return left // right
        elif kind == TokenKind.PERCENT:
            return left % right
        elif kind == TokenKind.DOUBLE_STAR:
            return left**right
        elif kind == TokenKind.DOUBLE_EQUALS:
            return left == right
        elif kind == TokenKind.NOT_EQUALS:
            return left != right
        elif kind == TokenKind.LESS:
            return left < right
        elif kind == TokenKind.GREATER:
            return left > right
        elif kind == TokenKind.LESS_EQUALS:
            return left <= right
        elif kind == TokenKind.GREATER_EQUALS:
            return left >= right
        elif kind == TokenKind.AND:
            return left and right
        elif kind == TokenKind.OR:
            return left or right
        else:
            raise NotImplementedError(f"Binary operator {kind} not implemented")

    def visit_expr_stmt(self, stmt: ExprStmt):
        self.evaluate(stmt.expr)

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

    def visit_if_stmt(self, stmt: IfStmt):
        if self.evaluate(stmt.cond):
            self.execute(stmt.if_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_block_stmt(self, stmt: BlockStmt):
        for stmt in stmt.stmts:
            self.execute(stmt)

    def visit_comment_stmt(self, stmt: CommentStmt):
        pass

    def visit_function_stmt(self, stmt: FunctionStmt):
        name = stmt.name.value
        assert name not in self.functions, "Cannot redefine"
        self.functions[name] = stmt

    def visit_call_expr(self, expr: CallExpr):
        name = expr.callee.value
        function = self.functions.get(name)
        assert function is not None

        args = [self.evaluate(arg) for arg in expr.arguments]

        assert len(args) == len(function.params)

        # Create new scope for function
        previous_values = self.values.copy()

        # Bind parameters to arguments
        for (param_name, param_type), arg in zip(function.params, args):
            self.values[param_name.value] = arg

        return_value = None
        try:
            self.execute(function.body)
        except Return as ret:
            return_value = ret.value
        finally:
            self.values = previous_values

        return return_value

    def visit_return_stmt(self, stmt: ReturnStmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visit_unary_expr(self, expr: UnaryExpr):
        right = self.evaluate(expr.right)

        if expr.op.kind == TokenKind.NOT:
            return not right
        elif expr.op.kind == TokenKind.MINUS:
            return -right
        else:
            raise NotImplementedError(f"Unary operator {expr.op.kind} not implemented")


def interpret(source: str):
    stmts = parse(source)
    interpreter = Interpreter()
    interpreter.interpret(stmts)
