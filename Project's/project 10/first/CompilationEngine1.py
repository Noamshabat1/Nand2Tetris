"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
# import typing
import JackTokenizer1

##################################################################

"""
CONSTANTS:
"""
CLASS_CONST = "class"


##################################################################


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    statements_list = {"let", "return", "if", "while", "do"}

    op = {'+', '-', '*', '/', "&amp;", '|', "&lt;", "&gt;", '='}

    def __init__(self, input_stream: "JackTokenizer1", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        self.tokenizer = input_stream
        self.output = output_stream
        self.cur = ""

    def beginning_to_comp(self, name, newline=True):
        """
        a function that we created
        """
        self.output.write(self.cur + f"<{name}>")
        if newline:
            self.output.write(self.cur + "\n")
        self.cur += "  "

    def stopping_to_comp(self, name, newline = False):
        """
        a function that we created
        """
        if newline:
            self.output.write(self.cur + "\n")
        else:
            self.cur = self.cur[:-2]
            self.output.write(self.cur + f"</{name}>\n")

    def write_to_and_advance(self, n=1):
        """
        a function that we created
        """
        for i in range(n):
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.beginning_to_comp(CLASS_CONST)

        while self.tokenizer.current_token in {"field", "static"}:
            self.compile_class_var_dec()

        while self.tokenizer.current_token in {"constructor", "function", "method"}:
            self.compile_subroutine()

        self.write_to_and_advance()
        self.stopping_to_comp(CLASS_CONST)

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self.beginning_to_comp("classVarDec")

        while self.tokenizer.current_token is not ";":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)

        self.tokenizer.advance()
        #print(cmd)
        self.stopping_to_comp("classVarDec")

    def comp_subroutine_body(self) -> None:
        """
        a function that we created
        """
        self.beginning_to_comp("subroutineBody") #start

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        while self.tokenizer.current_token == "var":
            self.compile_var_dec()

        self.compile_statements()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.stopping_to_comp("subroutineBody") #end

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """

        self.beginning_to_comp("subroutineDec") #start

        counter = 4
        while counter != 0:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            counter -=1

        self.compile_parameter_list()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.comp_subroutine_body()

        self.stopping_to_comp("subroutineDec") #end


    def compile_parameter_list(self) -> None:
        """
        Compiles a (possibly empty) parameter list, not including the enclosing "()".
        """
        self.beginning_to_comp("parameterList")

        while self.tokenizer.current_token != ")":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.stopping_to_comp("parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.beginning_to_comp("varDec")

        while self.tokenizer.current_token != ";":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.stopping_to_comp("varDec")


    def compile_statements(self) -> bool:
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        """
        self.beginning_to_comp("statements")
        while self.tokenizer.current_token in CompilationEngine.statements_list:
            if self.tokenizer.current_token == "if":
                self.compile_if()

            elif self.tokenizer.current_token == "return":
                self.compile_return()

            elif self.tokenizer.current_token == "while":
                self.compile_while()

            elif self.tokenizer.current_token == "do":
                self.compile_do()

            elif self.tokenizer.current_token == "let":
                self.compile_let()

            else:
                return False

        self.stopping_to_comp("statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.beginning_to_comp("doStatement")
        self.write_to_and_advance()
        while self.tokenizer.current_token != "(":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()


        self.write_to_and_advance()
        self.compile_expression_list()
        self.write_to_and_advance(2)

        self.stopping_to_comp("doStatement")


    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.beginning_to_comp("letStatement")
        self.write_to_and_advance(2)

        if self.tokenizer.current_token == '[':
            self.write_to_and_advance()
            self.compile_expression()
            self.write_to_and_advance()


        self.write_to_and_advance()
        self.compile_expression()
        self.write_to_and_advance()

        self.stopping_to_comp("letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.beginning_to_comp("whileStatement")
        self.write_to_and_advance(2)

        self.compile_expression()
        self.write_to_and_advance(2)

        self.compile_statements()
        self.write_to_and_advance()

        self.stopping_to_comp("whileStatement")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.beginning_to_comp("returnStatement")
        self.write_to_and_advance()

        if self.tokenizer.current_token != ";":
            self.compile_expression()
        self.write_to_and_advance()

        self.stopping_to_comp("returnStatement")


    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.beginning_to_comp("ifStatement")
        for i in range(2):
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
        self.compile_expression()

        for i in range(2):
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.compile_statements()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        if self.tokenizer.current_token == "else":
            for i in range(2):
                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()

            self.compile_statements()
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()


        self.stopping_to_comp("ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.beginning_to_comp("expression")
        self.compile_term()
        while self.tokenizer.current_token in CompilationEngine.op:
            self.write_to_and_advance()
            self.compile_term()

        self.stopping_to_comp("expression")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.beginning_to_comp("term")
        if self.tokenizer.current_token == "(":
            self.write_to_and_advance()

            self.compile_expression()
            self.write_to_and_advance()

        elif self.tokenizer.current_token in {"~", "-", "^", "#"}:
            self.write_to_and_advance()
            self.compile_term()

        else:
            self.write_to_and_advance()

        if self.tokenizer.current_token == "[":
            self.write_to_and_advance()
            self.compile_expression()
            self.write_to_and_advance()

        elif self.tokenizer.current_token == "(" or self.tokenizer.current_token == ".":
            while self.tokenizer.current_token != "(":
                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()

            self.write_to_and_advance()
            self.compile_expression_list()
            self.write_to_and_advance()

        self.stopping_to_comp("term")


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.beginning_to_comp("expressionList")
        if self.tokenizer.current_token != ')':
            self.compile_expression()

            while self.tokenizer.current_token == ',':
                self.write_to_and_advance()
                self.compile_expression()

        self.stopping_to_comp("expressionList")

