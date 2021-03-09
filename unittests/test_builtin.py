import pytest

from compiler.exceptions import MipsTypeErrorToManyArguments
from unittests.mips_vm import MIPSVM


def test_math_min_1():
    program = """
a = min(1, 2)

"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_min_2():
    program = """
a = min(2, 1)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_max_1():
    program = """
a = max(1, 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 2


def test_math_max_2():
    program = """
a = max(2, 1)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 2


def test_math_min_exp_1():
    program = """
a = min(1 if 1 else 2, 3)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_min_exp_2():
    program = """
a = min(1 if 0 else 2, 3)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 2


def test_math_min_exp_3():
    program = """
a = min(3, 1 if 1 else 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_min_exp_4():
    program = """
a = min(3, 1 if 0 else 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 2


def test_math_not_min_1():
    program = """
a = not min(0, 1)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_if_ternary_min_1():
    program = """
a = 0 if min(0, 1) else 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_if_min_1():
    program = """
if min(0, 1):
    a = 1
else:
    a = 0
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 0


def test_math_if_max_1():
    program = """
if max(0, 1):
    a = 1
else:
    a = 0
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_min_expr_1():
    program = """
a = 10 + min(1, 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 11


def test_math_min_expr_2():
    program = """
a =  min(1, 2) + 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 11

def test_math_min_expr_3():
    program = """
a = 1 if 10 + min(1, 2) else 0
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 1


def test_math_min_expr_4():
    program = """
a = min(1 + 10, 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 2


def test_math_min_expr_5():
    program = """
a = min(1 + 10, 1 - 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == -1


def test_math_min_expr_6():
    program = """
a = max(1 + 10, 20) + min(1 - 2, -25)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == -5
    assert vm.highest_register_used == 1


def test_math_min_nested_1():
    program = """
a = min(max(1 + 10, 20), min(1 - 2, -20))
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == -20
    assert vm.highest_register_used == 1


def test_math_min_nested_2():
    program = """
a = max(max(1 + 20, 20), min(1 - 2, -20))
b = 100
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('r0') == 21
    assert vm.highest_register_used == 1



def test_sleep():
    program = """
sleep(1)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_total_sleep() == 1


def test_sleep_args_1():
    program = """
a = 2
sleep(min(a + 1, a))
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_total_sleep() == 2


def test_sleep_args_2():
    program = """
a = 2
sleep(1 if a else 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_total_sleep() == 1


def test_exception_sleep_return_1():
    program = """
a = sleep(2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_total_sleep() == 2
    assert vm.get_variable('r0') == 0


def test_exception_sleep_return_2():
    program = """
a = sleep(2)
b = a + 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_total_sleep() == 2

    assert vm.get_variable('r0') == 0
    assert vm.get_variable('r1') == 1




def test_math_rand_1():
    program = """
a = rand()
"""
    vm = MIPSVM(program)
    vm.execute()

    assert vm.mips_len == 1
    assert vm.get_variable('r0') == 0.5


def test_math_rand_2():
    program = """
a = rand() if True else 0
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.mips_len == 4
    assert vm.get_variable('r0') == 0.5


def test_math_rand_3():
    program = """
a = min(rand(), 1)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.mips_len == 2
    assert vm.get_variable('r0') == 0.5


