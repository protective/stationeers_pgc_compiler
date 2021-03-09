from unittests.mips_vm import MIPSVM


def test_assign_expr():
    program = """
a = 1
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1


def test_assign_add_expr():
    program = """
a = 2
a += 2
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4


def test_assign_sub_expr():
    program = """
a = 2
a -= 2
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 0


def test_assign_mult_expr():
    program = """
a = 2
a *= 2
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4


def test_assign_div_expr():
    program = """
a = 2
a /= 2
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1


def test_assign_add_var_1():
    program = """
a = 2
a += 2 + a
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 6


def test_assign_add_var_2():
    program = """
a = 2
a += a + 2
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 6


def test_assign_precedence_1():
    program = """
a = 2
a += a * 10
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 22
    assert vm.highest_register_used == 1


def test_assign_precedence_2():
    program = """
a = 2
a *= a + 10
out = a
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 24
    assert vm.highest_register_used == 1
