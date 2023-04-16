"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright

    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, pointer, temp

    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.

    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    @staticmethod
    def drop_comments(arr: list, i: int) -> str:
        line_list = arr[i].partition("//")
        line = line_list[0]
        return line.strip()

    @staticmethod
    def is_white_space(arr: list, i: int) -> bool:
        line = arr[i].replace(" ", "")
        return line == "" or line[0] == "/"

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        arr = input_file.read().splitlines()

        number_of_commends = len(arr)
        self.all_commends: list[str] = []
        self.current_command_index = 0

        for i in range(number_of_commends):
            if not Parser.is_white_space(arr, i):
                self.all_commends.append(Parser.drop_comments(arr, i))

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        number_of_commands = len(self.all_commends)
        return self.current_command_index != number_of_commands

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if it has_more_commands() is true. Initially
        there is no current command.
        """
        self.current_command_index += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        arithmetic_commands = {"add", "sub", "and", "or", "eq", "gt", "lt", "neg", "not", "shiftleft", "shiftright"}
        cmd = self.all_commends[self.current_command_index].split(" ")[0]
        if cmd in arithmetic_commands:
            return "C_ARITHMETIC"
        elif cmd == "push":
            return "C_PUSH"
        elif cmd == "pop":
            return "C_POP"

        # project 8

        elif cmd == "label":
            return "C_LABEL"
        # Checking if-goto before goto
        elif cmd == "if-goto":
            return "C_IF"
        elif cmd == "goto":
            return "C_GOTO"
        elif cmd == "function":
            return "C_FUNCTION"
        elif cmd == "return":
            return "C_RETURN"
        elif cmd == "call":
            return "C_CALL"
        else:
            # "C_LABEL"
            # "C_GOTO",
            # "C_IF"
            # "C_FUNCTION"
            # "C_RETURN"
            # "C_CALL"
            raise NameError("Unexpected Command Type")

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            return self.all_commends[self.current_command_index].split(" ")[0]
        else:
            return self.all_commends[self.current_command_index].split(" ")[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        arg2 = int(self.all_commends[self.current_command_index].split(" ")[2])
        return arg2
