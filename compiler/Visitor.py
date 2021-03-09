from compiler.types import Function, Device, FunctionBuiltIn


class Visitor:

    def visit(self, node, **kwargs):
        f = getattr(self, node.data)
        return f(node, **kwargs)


class CompileEnv(Visitor):
    def __init__(self, build_env):
        self.build_env = build_env

