import pytest

from unittests.mips_vm import MIPSVM


@pytest.mark.skip
def test_hydro_control():

    with open('scripts/hydro_control_chip.py', 'r') as fd:
        program = fd.read()

    vm = MIPSVM(program)
    vm.execute({('d0', 'Setting'): 1,
                ('d1', 'Open'): 0,
                ('d1', 'Lock'): 0,
                ('d2', 'On'): 0,
                ('d2', 'Mode'): 0,
                ('d3', 'On'): 0,
                ('d3', 'Mode'): 0,
                ('d4', 'Pressure'): 50,
                ('d4', 'RatioVolatiles'): 0,
                ('db', 'Setting'): 0
                })
    for _ in range(0, 3):
        vm.execute()
    assert vm.get_variable(('d2', 'On')) == 1

    vm.execute({('d4', 'Pressure'): 0})
    assert vm.get_variable(('d2', 'On')) == 0

    vm.execute({('d4', 'Pressure'): 0})
    vm.execute({('d4', 'Pressure'): 0})
    vm.execute({('d4', 'Pressure'): 0})
    assert vm.get_variable(('d3', 'On')) == 1

    vm.execute({('d4', 'Pressure'): 11})
    assert vm.get_variable(('d3', 'On')) == 0

    vm.execute({('d4', 'Pressure'): 11})
    assert vm.get_variable(('db', 'Setting')) == 1
