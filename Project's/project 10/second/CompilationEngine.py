"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import JackTokenizer

SPECIAL_TOKENS = ["~", "-", "^", "#"]
LET_WORD = "let"
DO_WORD = "do"
WHILE_WORD = "while"
RETURN_WORD = "return"
IF_WORD = "if"
CLASS_CONST = "class"
CLASS_VAR_CONST = "classVarDec"
SUB_BODY_CONST = "subroutineBody"
SUB_DEC_CONST = "subroutineDec"
PARM_LST_CONST = "parameterList"
VAR_DEC_CONST = "varDec"
STATEMENT_CONST = "statements"
DO_CONST = "doStatement"
LET_CONST = "letStatement"
WHILE_CONST = "whileStatement"
RETURN_CONST = "returnStatement"
IF_STAT_CONST = "ifStatement"
EXPRESSION_CONST = "expression"
TERM_CONST = "term"
EXPRESSION_LST_CONST = "expressionList"


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    statements_list = ["let", "return", "if", "while", "do"]

    op = ['+', '-', '*', '/', "&amp;", '|', "&lt;", "&gt;", '=']

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        self.tokenizer = input_stream
        self.output = output_stream
        self.cur = ""
        self.counter = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output.write(self.cur + f"<{CLASS_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.counter < 3:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        while self.tokenizer.current_token in {"field", "static"}:
            self.compile_class_var_dec()

        while self.tokenizer.current_token in {"constructor", "function", "method"}:
            self.compile_subroutine()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{CLASS_CONST}>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output.write(self.cur + f"<{CLASS_VAR_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "
        while self.tokenizer.current_token != ";":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{CLASS_VAR_CONST}>\n")

    def comp_subroutine_body(self) -> None:
        """
        a function that we created
        """
        self.output.write(self.cur + f"<{SUB_BODY_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        while self.tokenizer.current_token == "var":
            self.compile_var_dec()

        self.compile_statements()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{SUB_BODY_CONST}>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output.write(self.cur + f"<{SUB_DEC_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.counter < 4:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        self.compile_parameter_list()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.comp_subroutine_body()
        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{SUB_DEC_CONST}>\n")

    def compile_parameter_list(self) -> None:
        """
        Compiles a (possibly empty) parameter list, not including the enclosing "()".
        """
        self.output.write(self.cur + f"<{PARM_LST_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.tokenizer.current_token != ")":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{PARM_LST_CONST}>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output.write(self.cur + f"<{VAR_DEC_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.tokenizer.current_token != ";":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{VAR_DEC_CONST}>\n")

    def compile_statements(self) -> bool:
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        """
        self.output.write(self.cur + f"<{STATEMENT_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.tokenizer.current_token in CompilationEngine.statements_list:
            if self.tokenizer.current_token == IF_WORD:
                self.compile_if()

            elif self.tokenizer.current_token == RETURN_WORD:
                self.compile_return()

            elif self.tokenizer.current_token == WHILE_WORD:
                self.compile_while()

            elif self.tokenizer.current_token == DO_WORD:
                self.compile_do()

            elif self.tokenizer.current_token == LET_WORD:
                self.compile_let()

            else:
                return False

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{STATEMENT_CONST}>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output.write(self.cur + f"<{DO_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        while self.tokenizer.current_token != "(":
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.compile_expression_list()

        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{DO_CONST}>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output.write(self.cur + f"<{LET_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "
        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        if self.tokenizer.current_token == '[':
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.compile_expression()
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.compile_expression()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{LET_CONST}>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.output.write(self.cur + f"<{WHILE_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0
        self.compile_expression()

        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        self.compile_statements()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{WHILE_CONST}>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output.write(self.cur + f"<{RETURN_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        if self.tokenizer.current_token != ";":
            self.compile_expression()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{RETURN_CONST}>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output.write(self.cur + f"<{IF_STAT_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "
        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0
        self.compile_expression()

        while self.counter < 2:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()
            self.counter += 1
        self.counter = 0

        self.compile_statements()
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        if self.tokenizer.current_token == "else":
            while self.counter < 2:
                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()
                self.counter += 1
            self.counter = 0

            self.compile_statements()
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{IF_STAT_CONST}>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.output.write(self.cur + f"<{EXPRESSION_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        self.compile_term()

        while self.tokenizer.current_token in CompilationEngine.op:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

            self.compile_term()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{EXPRESSION_CONST}>\n")

    def compile_term_helper_open_parentheses(self):
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

        self.compile_expression_list()

        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()

    def compile_special_terms(self):
        self.output.write(self.cur + self.tokenizer.cmd)
        self.tokenizer.advance()
        self.compile_term()

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
        self.output.write(self.cur + f"<{TERM_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        if self.tokenizer.current_token == "(":
            self.compile_term_helper_open_parentheses()

        elif self.tokenizer.current_token in SPECIAL_TOKENS:
            self.compile_special_terms()

        else:
            self.output.write(self.cur + self.tokenizer.cmd)
            self.tokenizer.advance()

            if self.tokenizer.current_token == "[":
                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()

                self.compile_expression()

                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()

            elif self.tokenizer.current_token == "(" or self.tokenizer.current_token == ".":
                while self.tokenizer.current_token != "(":
                    self.output.write(self.cur + self.tokenizer.cmd)
                    self.tokenizer.advance()

            self.compile_term_helper_open_parentheses()

        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{TERM_CONST}>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # open statement
        self.output.write(self.cur + f"<{EXPRESSION_LST_CONST}>")
        self.output.write(self.cur + "\n")
        self.cur += "  "

        if self.tokenizer.current_token != ')':
            self.compile_expression()

            while self.tokenizer.current_token == ',':
                self.output.write(self.cur + self.tokenizer.cmd)
                self.tokenizer.advance()
                self.compile_expression()

        # close statement
        self.cur = self.cur[:-2]
        self.output.write(self.cur + f"</{EXPRESSION_LST_CONST}>\n")
