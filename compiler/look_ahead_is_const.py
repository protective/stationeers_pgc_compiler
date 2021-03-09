from lark import Tree

from compiler.expr_look_ahead import ExprLookAhead
from compiler.types import FunctionBuiltIn


class LAIsConst(ExprLookAhead):

    def __init__(self, build_env, node):
        super().__init__(build_env)
        ret = self.visit(node)
        self.result = False if ret is None else True

    def loc(self, loc):
        return True

    def const_true(self, token):
        return True

    def const_false(self, token):
        return True

    def number(self, number):
        return True