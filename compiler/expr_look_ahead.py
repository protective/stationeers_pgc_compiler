from lark.lexer import Token

from compiler.Visitor import CompileEnv


class ExprLookAhead(CompileEnv):

    def reduce_expr(self, tree):
        lst = tree.children.copy()
        for node in lst:
            if not isinstance(node, Token):
                self.visit(node)

    def unary_operator(self, right):
        self.visit(right)

    def expr(self, expr):
        return self.reduce_expr(expr)

    def term(self, expr):
        return self.reduce_expr(expr)

    def arith_expr(self, expr):
        return self.reduce_expr(expr)

    def comparison(self, expr):
        self.reduce_expr(expr)

    def atom_expr(self, expr):
        pass

    def call(self, expr):
        pass

    def attr_get(self, expr):
        self.visit(expr.children[1])

    def dot_access(self, expr):
        pass

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
        pass

    def const_true(self, token):
        pass

    def const_false(self, token):
        pass

    def loc(self, loc):
        pass

    def factor(self, number):
        pass

    def number(self, number):
        pass

    def subscriptlist(self, expr):
        return self.visit(expr.children[0])

    def subscript(self, expr):
        return self.visit(expr.children[0])
