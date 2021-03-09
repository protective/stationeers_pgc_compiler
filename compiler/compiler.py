import os
from contextlib import contextmanager

import sys
from pathlib import Path

from compiler.InstBuilder import InstBuilder
from compiler.exceptions import MipsSyntaxError, MipsException

try:
    from lark import Lark, Tree
    from lark import exceptions as lark_exceptions
    from lark.lexer import Token
    from lark.indenter import Indenter

except ImportError:
    print('Missing Module lark install with pip \"pip install lark-parser\"')
    sys.exit(1)

grammar = None

with open(Path(__file__).parent / 'gramma', 'r') as fd:
    grammar = fd.read()


class TreeIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


class Compiler:
    def __init__(self, debug=False):
        self.debug = debug
        self.final_program = []

    def compile(self, program):
        parser = Lark(grammar, start='root', parser='lalr', postlex=TreeIndenter())
        try:
            tree = parser.parse(program + os.linesep)
        except lark_exceptions.UnexpectedToken as exc:
            msg = "Unexpected token %s at line %s, column %s.\n" % (exc.token.type, exc.line, exc.column)
            raise MipsSyntaxError(msg)
        except lark_exceptions.UnexpectedCharacters as exc:
            raise MipsSyntaxError(exc)

        if self.debug:
            print(tree)
        builder = InstBuilder()
        builder.visit(tree)

        self.program = builder.program
        self.labels = builder.labels
        self.resolve_labels()
        self.validate()
        return "\n".join([f'{line:20} // {i:2}: {desc}' for i, (line, desc) in enumerate(self.final_program)])

    def resolve_labels(self):

        for line, desc in self.program:
            line = line.format(**self.labels)
            desc = desc.format(**self.labels)
            self.final_program.append((line, desc))

    def validate(self):
        if len(self.final_program) > 127:
            raise Exception(f"program to large {len(self.final_program)} > 127")


def compile_file(file: Path, debug=False):
    file_o = Path(f'{file}.mips')
    with file.open('r') as fd_r, file_o.open('w') as fd_w:
        output = compile_src(fd_r.read(), debug)
        fd_w.write(output)
        print(output)


def compile_src(src: str, debug=False):
    try:
        compiler = Compiler(debug=debug)
        compiler.compile(src)

        output = ""
        if debug:

            output += "Begin Python**************************\n"
            output = src.strip() + '\n'
            output += "End Python*****************************\n"

            output += "IDTable******************************\n"
            output += "\n".join([f'{key} ==> {value}' for key, value in compiler.idtable.items()])
            output += "\n"
            output += "JumpTable******************************\n"
            output += "\n".join([f'{key} ==> {value}' for key, value in compiler.labels.items()])
            output += "\n"
            for i, (line, desc) in enumerate(compiler.program):
                output += f'{line:35} {i:2}: {desc}\n'

            output += "MIPS***********************************\n"
            for i, (line, desc) in enumerate(compiler.final_program):
                output += f'{line:35} {i:2}: {desc}\n'

        else:
            for i, (line, desc) in enumerate(compiler.final_program):
                output += f'{line}\n'
    except MipsException as exc:
        return str(exc)
    except Exception as exc:
        return str(exc)
    return output.strip()
