"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.commands = [
            self._remove_comments_from_line(line)
            for line in input_file.read().splitlines()
            if not self._is_line_empty_or_comment(line)
        ]
        self.current_command_index = 0

    @staticmethod
    def _remove_comments_from_line(line: str) -> str:
        """Removes comments from a line of assembly code."""
        return line.split("//")[0].strip()

    @staticmethod
    def _is_line_empty_or_comment(line: str) -> bool:
        """Checks if a line is empty or a comment."""
        stripped_line = line.strip()
        return not stripped_line or stripped_line.startswith("//")

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.current_command_index < len(self.commands)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        if self.has_more_commands():
            self.current_command_index += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        current_command = self.commands[self.current_command_index]
        if current_command.startswith("@"):
            return "A_COMMAND"
        elif current_command.startswith("("):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!
        current_command = self.commands[self.current_command_index]
        if self.command_type() in ["A_COMMAND", "L_COMMAND"]:
            return current_command.strip("@()")

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        current_command = self.commands[self.current_command_index]
        if "=" in current_command:
            return current_command.split("=")[0].strip()
        return ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        current_command = self.commands[self.current_command_index]
        parts = current_command.split("=")[-1].split(";")
        return parts[0].strip()

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        current_command = self.commands[self.current_command_index]
        if ";" in current_command:
            return current_command.split(";")[-1].strip()
        return ""

    def restart(self) -> None:
        """Resets the command index to the beginning of the file."""
        self.current_command_index = 0
