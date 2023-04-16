"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    s_table = SymbolTable()  # initialization

    #  First Pass
    address = 0
    parser_1 = Parser(input_file)
    while parser_1.has_more_commands():
        if parser_1.command_type() == "L_COMMAND":
            symbol = parser_1.symbol()
            s_table.add_entry(symbol, address)
        else:
            address += 1
        parser_1.advance()
    parser_1.restart()

    #  Second Pass
    variable_available_address = 16
    while parser_1.has_more_commands():
        if parser_1.command_type() == "A_COMMAND":
            symbol = parser_1.symbol()
            if not symbol.isdigit():
                if not s_table.contains(symbol):
                    s_table.add_entry(symbol, variable_available_address)
                    variable_available_address += 1

                decimal_address = s_table.get_address(symbol)
                command = bin(int(decimal_address)).replace("0b", "")
                output_file.write("0" * (16 - len(command)) + command + "\n")
            else:
                command = bin(int(symbol)).replace("0b", "")
                while len(command) != 15:
                    command = "0" + command
                output_file.write("0" + command + "\n")
        elif parser_1.command_type() == "C_COMMAND":
            dest = parser_1.dest()
            comp = parser_1.comp()
            is_shift = False
            if ">>" in comp or "<<" in comp:
                is_shift = True
            jump = parser_1.jump()
            dest = Code.dest(dest)
            comp = Code.comp(comp)
            jump = Code.jump(jump)
            if is_shift:
                command = f"101{comp}{dest}{jump}"
            else:
                command = f"111{comp}{dest}{jump}"
            output_file.write(command + "\n")
        parser_1.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")

    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [os.path.join(argument_path, filename) for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]

    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
