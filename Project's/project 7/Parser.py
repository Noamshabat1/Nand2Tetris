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
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
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

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        lines = input_file.read().splitlines()
        self.all_commends = [self._strip_comments(line) for line in lines if
                             not self._is_whitespace_or_comment(line)]
        self.current_command_index = 0

    @staticmethod
    def _strip_comments(line: str) -> str:
        """
        Strips comments from a line of code.
        """
        return line.partition("//")[0].strip()

    @staticmethod
    def _is_whitespace_or_comment(line: str) -> bool:
        """
        Checks if a line is whitespace or a comment.
        """
        stripped_line = line.strip()
        return not stripped_line or stripped_line.startswith("//")

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_command_index < len(self.all_commends)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        if self.has_more_commands():
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
        arithmetic_commands = {"add", "sub", "and", "or", "eq", "gt", "lt",
                               "neg", "not", "shiftleft", "shiftright"}

        # set the current command.
        command = self.all_commends[self.current_command_index].split(" ")[0]

        # Determine the type of the current command.
        if command in arithmetic_commands:
            return "C_ARITHMETIC"

        elif command == "push":
            return "C_PUSH"

        elif command == "pop":
            return "C_POP"

        # project 8

        # elif command == "label":
        #     return "C_LABEL"
        #
        # elif command == "if-goto":
        #     return "C_IF"
        #
        # elif command == "goto":
        #     return "C_GOTO"
        #
        # elif command == "function":
        #     return "C_FUNCTION"
        #
        # elif command == "return":
        #     return "C_RETURN"
        #
        # elif command == "call":
        #     return "C_CALL"

        else:
            raise ValueError(f"Unexpected command type: {command}")

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_RETURN":
            raise ValueError(
                "The 'C_RETURN' command does not have an argument.")

        current_command_parts = self._current_command_split()
        arg1 = current_command_parts[0] if \
            self.command_type() == "C_ARITHMETIC" else current_command_parts[1]
        return arg1

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        arg2 = int(self.all_commends[self.current_command_index].split(" ")[2])
        return arg2

    def _current_command_split(self) -> list[str]:
        """
        Splits the current command into its constituent parts.

        Returns:
            list[str]: The split parts of the current command.
        """
        return self.all_commends[self.current_command_index].split()
