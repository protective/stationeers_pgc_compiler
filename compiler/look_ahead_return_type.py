from lark import Tree
from lark.lexer import Token

from compiler.exceptions import MipsUnboundLocalError
from compiler.expr_look_ahead import ExprLookAhead
from compiler.types import Device, Variable, VarType, FunctionBuiltIn


class LAReturnType(ExprLookAhead):

    def __init__(self, build_env, node):
        super().__init__(build_env)
        self.return_type = self.visit(node)


    def call(self, expr):

        id = expr.children[0].children[0].value
        if id in self.build_env.vtable:
            #    arguments = expr.children[1]
            #    ret = self.vtable[tree.children[0].value][1]
            if isinstance(self.build_env.vtable[id], FunctionBuiltIn):
                return VarType
            else:
                return self.build_env.vtable[id].var_type
        else:
            raise MipsUnboundLocalError(str(id))

    def reduce_expr(self, tree):
        lst = tree.children.copy()
        for node in lst:
            if not isinstance(node, Token):
                self.visit(node)

    def unary_operator(self, right):
        self.visit(right)

    def term(self, expr):
        return self.reduce_expr(expr)

    def arith_expr(self, expr):
        return self.reduce_expr(expr)

    def comparison(self, expr):
        self.reduce_expr(expr)

    def atom_expr(self, expr):
        pass

    def attr_get(self, expr):
        self.visit(expr.children[1])

    def dot_access(self, expr):
        ret = self.visit(expr.children[0])
        if isinstance(ret, Device):
            if ret.property_access == ['Reagent', 'Required']:
                return None
            elif ret.property_access == []:
                return None
        return ret

    def and_test(self, stmt):
        for node in stmt.children:
            self.visit(node)

    def or_test(self, stmt):
        for node in stmt.children:
            self.visit(node)

    def not_test(self, stmt):
        for node in stmt.children:
            self.unary_operator(node)

    def test(self, stmt):
        for node in stmt.children:
            self.visit(node)

    def var(self, var):
        if var.children[0].value in self.build_env.device_table:
            return self.build_env.device_table[var.children[0].value]

    def const_true(self, token):
        pass

    def const_false(self, token):
        pass

    def loc(self, loc):
        return Variable(loc, VarType)

    def factor(self, number):
        pass

    def number(self, number):
        return Variable(number, VarType)