import pytest

from unittests.mips_vm import MIPSVM


def test_if_else_ternary_false():
    program = """
out = 1 if 0 else 2
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 2
    assert vm.mips_len == 4


def test_if_else_ternary_true():
    program = """
out = 1 if 1 else 2
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 4


def test_if_else_ternary_expr_l_true():
    program = """
out = 10 + (1 if 1 else 2)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 11


def test_if_else_ternary_expr_r_true():
    program = """
out = (1 if 1 else 2) + 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 11


def test_if_false_eq():
    program = """
if 1 == 0:
    out = 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 0
    assert vm.mips_len == 2


def test_if_true_eq():
    program = """
if 1 == 1:
    out = 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 2


def test_if_false():
    program = """
if 0:
    out = 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 0
    assert vm.mips_len == 2


def test_if_true():
    program = """
if 1:
    out = 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 2


def test_if_neg():
    program = """
if -1:
    out = 1
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 2


def test_if_else_false():
    program = """
if 0:
    out = 1
else:
    out = 2
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 2
    assert vm.mips_len == 4


def test_if_else_true():
    program = """
if 1:
    out = 1
else:
    out = 2
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 4


def test_if_then_else_true_false():
    program = """
if 1:
    out = 1
elif 0:
    out = 2
else:
    out = 3
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 7


def test_if_then_else_true_true():
    program = """
if 1:
    out = 1
elif 1:
    out = 2
else:
    out = 3
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len == 7


def test_if_then_else_false_true():
    program = """
if 0:
    out = 1
elif 1:
    out = 2
else:
    out = 3
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 2
    assert vm.mips_len == 7


def test_if_then_else_false_false():
    program = """
if 0:
    out = 1
elif 0:
    out = 2
else:
    out = 3
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 3
    assert vm.mips_len == 7


def test_if_else_ternary_false_expr():
    program = """
out = 1 * 10 if 0 * 2 else 2 * 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 20


def test_if_else_ternary_true_expr():
    program = """
out = 1 * 10 if 1 * 2 else 2 * 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 10


def test_if_then_else_true_false_expr():
    program = """
if 1 * 2:
    out = 1 * 10
elif 0 * 2:
    out = 2 * 10
else:
    out = 3 * 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 10


def test_if_then_else_false_true_expr():
    program = """
if 0 * 2:
    out = 1 * 10
elif 1 * 2:
    out = 2 * 10
else:
    out = 3 * 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 20


def test_if_then_else_false_false_expr():
    program = """
if 0 * 2:
    out = 1 * 10
elif 0 * 2:
    out = 2 * 10
else:
    out = 3 * 10
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 30


def test_if_then_else_false_false_ternary_nested_false():
    program = """
if 0 * 2:
    out = 1 * 10 if 0 else 1 * 100
elif 0 * 2:
    out = 2 * 10 if 0 else 2 * 100
else:
    out = 3 * 10 if 0 else 3 * 100
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 300


def test_if_then_else_false_false_ternary_nested_true():
    program = """
if 0 * 2:
    out = 1 * 10 if 1 else 1 * 100
elif 0 * 2:
    out = 2 * 10 if 1 else 2 * 100
else:
    out = 3 * 10 if 1 else 3 * 100
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 30


def test_if_then_else_false_true_ternary_nested_false():
    program = """
if 0 * 2:
    out = 1 * 10 if 0 else 1 * 100
elif 1 * 2:
    out = 2 * 10 if 0 else 2 * 100
else:
    out = 3 * 10 if 0 else 3 * 100
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 200


def test_if_then_else_false_true_ternary_nested_true():
    program = """
if 0 * 2:
    out = 1 * 10 if 1 else 1 * 100
elif 1 * 2:
    out = 2 * 10 if 1 else 2 * 100
else:
    out = 3 * 10 if 1 else 3 * 100
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 20


def test_ternary_call_false():
    program = """
out = min(1, 2) if 0 else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4
    assert vm.mips_len <= 5


def test_ternary_call_true():
    program = """
out = min(1, 2) if 1 else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len <= 5


def test_ternary_call_cond_false():
    program = """
out = min(1, 2) if min(0, 1) else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4
    assert vm.mips_len <= 6

def test_ternary_call_cond_true():
    program = """
out = min(1, 2) if max(0, 1) else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len <= 6


@pytest.mark.skip
def test_ternary_call_false_improve():
    program = """
out = min(1, 2) if 0 else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4
    assert vm.mips_len <= 4

@pytest.mark.skip
def test_ternary_call_true_improve():
    program = """
out = min(1, 2) if 1 else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len <= 4

@pytest.mark.skip
def test_ternary_call_cond_false_improve():
    program = """
out = min(1, 2) if min(0, 1) else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 4
    assert vm.mips_len <= 4

@pytest.mark.skip
def test_ternary_call_cond_true_improve():
    program = """
out = min(1, 2) if max(0, 1) else max(3, 4)
"""
    vm = MIPSVM(program)
    vm.execute()
    assert vm.get_variable('o') == 1
    assert vm.mips_len <= 4



def test_tmp():
    program = """
sensor = device(d0, "Sensor")
valve = device(d1, "Valve")
while sensor.Pressure > 1000:
    valve.On = True
    yield_tick
valve.On = False
"""
    vm = MIPSVM(program)
    vm.execute({('d0', 'Pressure'): 1, ('db', 'Setting'): 1})
