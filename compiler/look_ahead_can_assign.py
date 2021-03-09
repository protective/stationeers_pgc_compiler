from lark import Tree

from compiler.expr_look_ahead import ExprLookAhead
from compiler.types import FunctionBuiltIn


class LACanAssign(ExprLookAhead):

    def __init__(self, build_env, node):
        super().__init__(build_env)
        ret = self.visit(node)
        self.result = False if ret is None else ret

    def dot_access(self, expr):
        return True

    def attr_get(self, expr):
        return True

    def loc(self, loc):
        return True

    def test(self, stmt):
        return True

    def arith_expr(self, expr):
        return True

    def expr(self, expr):
        return True

    def term(self, expr):
        return True

    def and_test(self, stmt):
        return True

    def or_test(self, stmt):
        return True

    def not_test(self, stmt):
        return True

    def comparison(self, expr):
        return True

    def call(self, expr):
        if isinstance(expr.children[0], Tree):
            tree = expr.children[0]

            if tree.children[0].value in self.build_env.vtable:
                function = self.build_env.vtable[tree.children[0].value]
                if isinstance(function, FunctionBuiltIn):
                    if function.returns:
                        return True
        return False
