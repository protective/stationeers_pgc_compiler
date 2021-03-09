from compiler.expr_look_ahead import ExprLookAhead


class LACanBranch(ExprLookAhead):

    def __init__(self, build_env, node):
        super().__init__(build_env)
        ret = self.visit(node)
        self.result = False if ret is None else True


    def comparison(self, expr):
        if expr.children[1].value in ["==", "!="]:
            return True
