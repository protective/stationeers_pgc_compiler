import math
import traceback

from compiler.compiler import Compiler


class MIPSVM:

    MAX_INST = 128
    def __init__(self, program=None):
        self._indput = {}
        self._output = {f'o': 0 for k in range(1)}
        self._registers = {f'r{k}': 0 for k in range(15)}
        self._pc = 0
        self._no_inst = 0
        self._program = []
        self.mips_len = None
        self.highest_register_used = 0
        self._total_sleep = 0
        if program:
            mips = Compiler().compile(program)
            self.parse(mips)
            self.mips_len = len(self._program)
            print()
            print("================================================")
            print(program)
            print("------------------------------------------------")
            print(mips)
            print()
            pass

    def __str__(self):
        ret = []

        ret.append(f'pc: {self._pc}')
        ret.append('Indput')
        for k, v in self._indput.items():
            ret.append(f'{k}: {v}')

        ret.append('Output')
        for k, v in self._output.items():
            ret.append(f'{k}: {v}')

        ret.append('Registers')
        for k, v in self._registers.items():
            ret.append(f'{k}: {v}')

        return "\n".join(ret)

    def _next_inst(self):
        if self._pc >= len(self._program):
            return None
        ret = self._program[self._pc]
        self._pc += 1
        return ret

    def parse(self, program):
        for line in program.strip().split('\n'):
            args = line.split(' ')
            self._program.append(args)

    def get_total_sleep(self)-> float:
        return self._total_sleep

    def get_variable(self, variable):
        return float(self._get_variable(variable))

    def _get_variable(self, variable):
        if variable in self._registers:
            reg_id = int(variable[1:])
            self.highest_register_used = max(reg_id, self.highest_register_used)
            return self._registers[variable]
        elif variable in self._indput:
            return self._indput[variable]
        elif variable in self._output:
            return self._output[variable]
        try:
            float(variable)
        except Exception as exc:
            print(f"unable to find variable {variable}")
            raise
        return variable

    def _set_variable(self, variable, value):
        if variable in self._registers:
            self._registers[variable] = value
        elif variable in self._indput:
            self._indput[variable] = value
        elif variable in self._output:
            self._output[variable] = value
        else:
            raise Exception(f"Unknown variable {variable}")

    def _execute_inst(self, args):
        inst = args[0]

        if inst == 'yield':
            return False
        elif inst == 'j':
            self._pc = int(args[1])
        elif inst == 'l':
            self._set_variable(args[1], self._get_variable((args[2], args[3])))
        elif inst == 'ls':
            self._set_variable(args[1], self._get_variable((args[2], args[4], int(float(self._get_variable(args[3]))))))
        elif inst == 'lr':
            self._set_variable(args[1], self._get_variable((args[2], 'Reagent', args[3], args[4])))
        elif inst == 's':
            self._set_variable((args[1], args[2]), self._get_variable(args[3]))
        elif inst == 'move':
            self._set_variable(args[1], self._get_variable(args[2]))
        elif inst == 'and':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) and float(self._get_variable(args[3]))))
        elif inst == 'or':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) or float(self._get_variable(args[3]))))
        elif inst == 'xor':
            self._set_variable(args[1], str(int(bool(float(self._get_variable(args[2]))) != bool(float(self._get_variable(args[3]))))))
        elif inst == 'add':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) + float(self._get_variable(args[3]))))
        elif inst == 'sub':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) - float(self._get_variable(args[3]))))
        elif inst == 'mul':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) * float(self._get_variable(args[3]))))
        elif inst == 'div':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) / float(self._get_variable(args[3]))))
        elif inst == 'mod':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) % float(self._get_variable(args[3]))))
        elif inst == 'slt':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) < float(self._get_variable(args[3])) else 0))
        elif inst == 'sgt':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) > float(self._get_variable(args[3])) else 0))
        elif inst == 'sle':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) <= float(self._get_variable(args[3])) else 0))
        elif inst == 'sge':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) >= float(self._get_variable(args[3])) else 0))
        elif inst == 'seq':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) == float(self._get_variable(args[3])) else 0))
        elif inst == 'sne':
            self._set_variable(args[1], str(1 if float(self._get_variable(args[2])) != float(self._get_variable(args[3])) else 0))
        elif inst == 'bgtz':
            if float(self._get_variable(args[1])) > 0:
                self._pc = int(args[2])
        elif inst == 'beq':
            if float(self._get_variable(args[1])) == float(self._get_variable(args[2])):
                self._pc = int(args[3])
        elif inst == 'bne':
            if float(self._get_variable(args[1])) != float(self._get_variable(args[2])):
                self._pc = int(args[3])
        elif inst == 'min':
            self._set_variable(args[1], str(min(float(self._get_variable(args[2])), float(self._get_variable(args[3])))))
        elif inst == 'max':
            self._set_variable(args[1], str(max(float(self._get_variable(args[2])), float(self._get_variable(args[3])))))
        elif inst == 'sleep':
            self._total_sleep += float(self._get_variable(args[1]))
        elif inst == 'rand':
            # Set random to 0.5 for unitest
            self._set_variable(args[1], str(float(0.5)))
        elif inst == 'cos':
            self._set_variable(args[1], str(math.cos(float(self._get_variable(args[2])))))
        elif inst == 'sin':
            self._set_variable(args[1], str(math.sin(float(self._get_variable(args[2])))))
        elif inst == 'tam':
            self._set_variable(args[1], str(math.tan(float(self._get_variable(args[2])))))
        elif inst == 'acos':
            self._set_variable(args[1], str(math.acos(float(self._get_variable(args[2])))))
        elif inst == 'asin':
            self._set_variable(args[1], str(math.asin(float(self._get_variable(args[2])))))
        elif inst == 'atam':
            self._set_variable(args[1], str(math.atan(float(self._get_variable(args[2])))))
        elif inst == 'mod':
            self._set_variable(args[1], str(float(self._get_variable(args[2])) % float(self._get_variable(args[3]))))
        elif inst == 'abs':
            self._set_variable(args[1], str(abs(float(self._get_variable(args[2])))))
        elif inst == 'exp':
            self._set_variable(args[1], str(math.exp(float(self._get_variable(args[2])))))
        elif inst == 'floor':
            self._set_variable(args[1], str(math.floor(float(self._get_variable(args[2])))))
        elif inst == 'ceil':
            self._set_variable(args[1], str(math.ceil(float(self._get_variable(args[2])))))
        elif inst == 'log':
            self._set_variable(args[1], str(math.log(float(self._get_variable(args[2])))))
        elif inst == 'round':
            self._set_variable(args[1], str(round(float(self._get_variable(args[2])))))
        elif inst == 'sqrt':
            self._set_variable(args[1], str(math.sqrt(float(self._get_variable(args[2])))))

        return True

    def execute(self, indput=None):
        try:
            if indput:
                for k, v in indput.items():
                    self._indput[k] = v

            while self._no_inst < self.MAX_INST:
                inst = self._next_inst()
                if not inst:
                    break
                ret = self._execute_inst(inst)
                if not ret:
                    self._no_inst = 0
                    break
                self._no_inst += 1
        except Exception as exc:
            print(exc)
            traceback.print_exc()
            raise
