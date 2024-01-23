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


def format_binary_command(address, bit_length=16):
    """
    Formats an address to a binary command string of specified Bit length.

    """
    binary_command = bin(int(address)).replace("0b", "")
    return binary_command.rjust(bit_length, '0')


def assemble_file(input_file: typing.TextIO,
                  output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    symbol_table_container = [SymbolTable()]
    parser_container = [Parser(input_file)]
    process_first_pass(parser_container, symbol_table_container)
    process_second_pass(parser_container, symbol_table_container, output_file)


def process_first_pass(parser_container, symbol_table_container):
    """Processes the first pass of the assembler and also processes the
    L_COMMAND type instructions.
    """
    address = 0
    while parser_container[0].has_more_commands():
        if parser_container[0].command_type() == "L_COMMAND":
            var = parser_container[0].symbol()
            symbol_table_container[0].add_entry(var, address)
        else:
            address += 1
        parser_container[0].advance()
    parser_container[0].restart()


def process_second_pass(parser_container, symbol_table_container, output_file):
    """Processes the second pass of the assembler.
    """
    variable_address = [16]
    while parser_container[0].has_more_commands():
        command_type = parser_container[0].command_type()
        if command_type == "A_COMMAND":
            process_A_command(parser_container, symbol_table_container,
                              variable_address, output_file)

        elif command_type == "C_COMMAND":
            process_C_command(parser_container, output_file)

        parser_container[0].advance()


def process_A_command(parser_container, symbol_table_container,
                      variable_open_address, output_file):
    """Processes A_COMMAND type instructions.
    """
    symbol = parser_container[0].symbol()
    if not symbol.isdigit():
        if not symbol_table_container[0].contains(symbol):
            symbol_table_container[0].add_entry(symbol,
                                                variable_open_address[0])
            variable_open_address[0] += 1

        address = symbol_table_container[0].get_address(symbol)
        command = bin(int(address)).replace("0b", "")
        output_file.write("0" * (16 - len(command)) + command + "\n")
        
    else:
        command = bin(int(symbol)).replace("0b", "")
        while len(command) != 15:
            command = "0" + command
        output_file.write("0" + command + "\n")


def process_C_command(parser_container, output_file):
    """Processes C_COMMAND type instructions.
    """
    dest, comp, jump = (parser_container[0].dest(),
                        parser_container[0].comp(),
                        parser_container[0].jump())
    is_shift = ">>" in comp or "<<" in comp

    dest = Code.dest(dest)
    comp = Code.comp(comp)
    jump = Code.jump(jump)

    command_prefix = "101" if is_shift else "111"
    output_file.write(f"{command_prefix}{comp}{dest}{jump}\n")


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
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
