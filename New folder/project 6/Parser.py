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

    @staticmethod
    def drop_comments(arr: list, i: int) -> str:
        line_list = arr[i].partition("//")
        line = line_list[0]
        return line.strip()

    def restart(self) -> None:
        self.current_command = 0

    @staticmethod
    def is_white_space(arr: list, i: int) -> bool:
        line = arr[i].replace(" ", "")
        return line == "" or line[0] == "/"

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.
        Args:
            input_file (typing.TextIO): input file.
        """
        # A good place to start is:
        # input_lines = input_file.read().splitlines()

        arr = input_file.read().splitlines()
        number_of_commends = len(arr)
        self.all_commends = []
        for i in range(number_of_commends):
            if i == number_of_commends:
                break
            if not self.is_white_space(arr, i):
                self.all_commends.append(self.drop_comments(arr, i))
        self.current_command = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?
        Returns:
            bool: True if there are more commands, False otherwise.
        """
        number_of_commands = len(self.all_commends)
        return self.current_command != number_of_commands

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if it has_more_commands() is true.
        """
        self.current_command += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.all_commends[self.current_command][0] == "@":
            return "A_COMMAND"
        elif self.all_commends[self.current_command][0] == "(":
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
        line = self.all_commends[self.current_command].replace(" ", "")
        if self.command_type() == "A_COMMAND":
            return line[1:]
        else:
            size = len(line)
            return line[1: size - 1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        line = self.all_commends[self.current_command].replace(" ", "")
        if line.find("=") == -1:
            return ""
        arr = line.partition("=")
        return arr[0].strip()

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        line = self.all_commends[self.current_command].replace(" ", "")
        if line.find("=") == -1:  # checking if the command doesn't include the dest part like 0;JMP
            arr = line.partition(";")
            return arr[0]
        elif line.find(";") == -1:  # checking if the command doesn't include the dest part like 0;JMP
            arr = line.partition("=")
            return arr[2]
        else:
            arr_first = line.partition("=")  # makes an array of prev = at [0] and next =
            arr_sec = arr_first[2].split(";")  # get the comp and the jmp in arr
            return arr_sec[0].strip()

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        line = self.all_commends[self.current_command]
        line = line.replace(" ", "")
        if line.find(";") == -1:
            return ""
        arr = line.partition(";")
        return arr[2].strip()
