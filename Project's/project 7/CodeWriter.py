"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    # Create a class counter for unique labels.
    counter = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_file = output_stream

        # Symbols table for arithmetic op & assembly syntax.
        self.symbols = {

            # Arithmetic Operators

            "add": "M=D+M",
            "sub": "M=M-D",
            "and": "M=D&M",
            "or": "M=D|M",
            "neg": "M=-M",
            "not": "M=!M",
            "eq": "D;JEQ",
            "gt": "D;JGT",
            "lt": "D;JLT",

            # Assembly Symbols

            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "constant": "0",
            "static": "",
            "pointer": "3",
            "temp": "5"
        }

        self.filename = ""
        self.func = ""
        self.perv_func = ""
        self.i = 0
        self.perv_i = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:

        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        current_cmd = ""
        match command:
            case "add":
                current_cmd = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D+M"]
            case "sub":
                current_cmd = ["@SP", "M=M-1", "A=M", "D=-M", "A=A-1", "M=D+M"]
            case "and":
                current_cmd = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D&M"]
            case "or":
                current_cmd = ["@SP", "M=M-1", "A=M", "D=M", "A=A-1", "M=D|M"]
            case "neg":
                current_cmd = ["@SP", "A=M-1", "M=-M"]
            case "not":
                current_cmd = ["@SP", "A=M-1", "M=!M"]
            case "shiftleft":
                current_cmd = ["@SP", "A=M-1", "M=M<<"]
            case "shiftright":
                current_cmd = ["@SP", "A=M-1", "M=M>>"]
            case "eq":
                current_cmd = ["@SP",  # lest say that SP is at address 18.
                               "M=M-1",  # 17
                               "A=M",
                               "D=M",
                               "A=A-1",  # 16
                               "D=M-D",
                               "M=-1",  # if true
                               "@END" + str(CodeWriter.counter),
                               "D;JEQ",
                               "@SP",
                               "A=M-1",
                               "M=0",  # else false
                               "(END" + str(CodeWriter.counter) + ")"]
                CodeWriter.counter += 1

            case "gt":
                current_cmd = ["@SP",  # lest say that SP is at address 20.
                               "A=M-1",  # 19
                               "D=M",

                               # Last item is negative
                               "@NEG" + str(CodeWriter.counter),
                               "D;JLT",

                               # Last item is positive
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M",

                               "@FALSE" + str(CodeWriter.counter),
                               "D;JLT",

                               "@COMP" + str(CodeWriter.counter),
                               "D;JMP",

                               # Last item is negative
                               "(NEG" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M",

                               "@TRUE" + str(CodeWriter.counter),
                               "D;JGT",

                               # Same sign <=> no overflow
                               "(COMP" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "D=M",  # save the val of 19

                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M-D",  # 19 = 18 - 19

                               "@TRUE" + str(CodeWriter.counter),
                               "D;JGT",

                               "(FALSE" + str(CodeWriter.counter) + ")",
                               "@SP",
                               "A=M-1",
                               "A=A-1",
                               "M=0",  # false

                               "@END" + str(CodeWriter.counter),
                               "D;JMP",

                               "(TRUE" + str(CodeWriter.counter) + ")",
                               "@SP",
                               "A=M-1",
                               "A=A-1",
                               "M=-1",  # true

                               "(END" + str(CodeWriter.counter) + ")",
                               "@SP",
                               "M=M-1"]

                CodeWriter.counter += 1

            case "lt":
                current_cmd = ["@SP",  # lest say that SP is at address 20.
                               "A=M-1",  # 19
                               "D=M",

                               # Last item is negative
                               "@NEG" + str(CodeWriter.counter),
                               "D;JLT",

                               # Last item is positive
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M",

                               "@TRUE" + str(CodeWriter.counter),
                               "D;JLT",

                               "@COMP" + str(CodeWriter.counter),
                               "D;JMP",

                               # Last item is positive
                               "(NEG" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M",

                               "@FALSE" + str(CodeWriter.counter),
                               "D;JGT",

                               # Same sign <=> no overflow
                               "(COMP" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "D=M",

                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "D=M-D",  # 19 = 18 - 19

                               "@TRUE" + str(CodeWriter.counter),
                               "D;JLT",

                               "(FALSE" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "M=0",  # false

                               "@END" + str(CodeWriter.counter),
                               "D;JMP",

                               "(TRUE" + str(CodeWriter.counter) + ")",
                               "@SP",  # 20
                               "A=M-1",  # 19
                               "A=A-1",  # 18
                               "M=-1",  # true

                               "(END" + str(CodeWriter.counter) + ")",
                               "@SP",
                               "M=M-1"]

                CodeWriter.counter += 1

        self.write_doco_to_output_file(["// " + command])
        self.write_doco_to_output_file(current_cmd)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        cmd = ""
        if command == "C_PUSH":
            if segment == "static":
                cmd = [
                    "@" + self.filename + "." + str(index),
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]

            elif segment == "pointer":
                if index == 0:
                    cmd = ["@THIS",
                           "D=M",
                           "@SP",
                           "A=M",
                           "M=D",
                           "@SP",
                           "M=M+1"]
                else:
                    cmd = ["@THAT",
                           "D=M",
                           "@SP",
                           "A=M",
                           "M=D",
                           "@SP",
                           "M=M+1"]

            elif segment == "constant":
                cmd = ["@" + str(index),
                       "D=A",
                       "@SP",
                       "A=M",
                       "M=D",
                       "@SP",
                       "M=M+1"]

            elif segment == "temp":
                cmd = ["@" + str(index),
                       "D=A",
                       "@" + self.symbols[segment],
                       "A=A+D",
                       "D=M",
                       "@SP",
                       "A=M",
                       "M=D",
                       "@SP",
                       "M=M+1"]

            else:
                cmd = ["@" + str(index),
                       "D=A",
                       "@" + self.symbols[segment],
                       "A=M+D",
                       "D=M",
                       "@SP",
                       "A=M",
                       "M=D",
                       "@SP",
                       "M=M+1"]

        elif command == "C_POP":
            if segment == "static":
                cmd = [
                    "@SP",
                    "A=M-1",
                    "D=M",
                    "@" + self.filename + "." + str(index),
                    "M=D",
                    "@SP",
                    "M=M-1"]

            elif segment == "pointer":
                if index == 0:
                    cmd = ["@SP",
                           "A=M-1",
                           "D=M",
                           "@THIS",
                           "M=D",
                           "@SP",
                           "M=M-1"]
                else:
                    cmd = ["@SP",
                           "A=M-1",
                           "D=M",
                           "@THAT",
                           "M=D",
                           "@SP",
                           "M=M-1"]

            elif segment == "temp":
                cmd = [
                    "@" + str(index),
                    "D=A",

                    "@" + self.symbols[segment],
                    "D=A+D",
                    "@R15",
                    "M=D",

                    "@SP",
                    "A=M-1",
                    "D=M",
                    "@R15",
                    "A=M",
                    "M=D",

                    "@SP",
                    "M=M-1"]

            else:
                cmd = [
                    "@" + str(index),
                    "D=A",

                    "@" + self.symbols[segment],
                    "D=M+D",
                    "@R15",
                    "M=D",

                    "@SP",
                    "A=M-1",
                    "D=M",
                    "@R15",
                    "A=M",
                    "M=D",

                    "@SP",
                    "M=M-1"]

        self.write_doco_to_output_file(
            ["// " + command + " " + segment + " " + str(index)])
        self.write_doco_to_output_file(cmd)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""

        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass

    def write_doco_to_output_file(self, lines: list) -> None:
        for line in lines:
            self.output_file.write(line)
            self.output_file.write("\n")
