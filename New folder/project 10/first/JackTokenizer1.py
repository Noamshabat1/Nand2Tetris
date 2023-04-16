"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """
    KEYWORDS_set = {'class',
                    'constructor',
                    'function',
                    'method',
                    'field',
                    'static',
                    'var',
                    'int',
                    'char',
                    'boolean',
                    'void',
                    'true',
                    'false',
                    'null',
                    'this',
                    'let',
                    'do',
                    'if',
                    'else',
                    'while',
                    'return'
                    }

    SYMBOLS_set = {'{', '}',
                   '(', ')',
                   '[', ']',
                   '.',
                   ',',
                   ';',
                   '+',
                   '-',
                   '*',
                   '/',
                   '&',
                   '|',
                   '<',
                   '>',
                   '=',
                   '~',
                   '^',
                   '#'
                   }

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """

        input_lines = input_stream.read().splitlines()
        input_lines = self.delete_white_spaces(input_lines)
        self.tokens_list = self.turn_lines_into_tokens(input_lines)  # make a list (token, token_type)
        self.cur_token_index = 0
        self.cmd = None
        self.current_token_counter = 0
        if len(self.tokens_list) != 0:
            self.cmd = f"<{self.tokens_list[0][1]}> {self.fix(self.tokens_list[0][0])} </{self.tokens_list[0][1]}>\n"
        self.current_token = self.fix(self.tokens_list[self.cur_token_index][0])

    @staticmethod
    def is_it_empty_line(current_array: list[list], i: int) -> bool:
        return current_array[i] == ""

    @staticmethod
    def fix(item) -> str:
        if item == '<':
            return "&lt;"

        elif item == '>':
            return "&gt;"

        elif item == '"':
            return "&quot;"

        elif item == '&':
            return "&amp;"

        return item

    @staticmethod
    def is_it_inline_comment(current_array: list[list], i: int) -> bool:
        return current_array[i][0:2] == "//"

    @staticmethod
    def not_a_string(current_array):
        """checking if there's an even numbers of parenthesising """
        number_of_q = 0
        for item in current_array[0]:
            if item == "\"":

                number_of_q += 1

        is_even = number_of_q % 2
        return not is_even

    @staticmethod
    def drop_white_space_from_command(current_array: list, i: int) -> str:
        all_list = current_array[i].partition("//")
        if JackTokenizer.not_a_string(all_list):
            cur = all_list[0]

        else:
            cur = current_array[i]

        return cur.strip()

    @staticmethod
    def drop_comments_from_input(input_lines: list) -> list:
        """
        this Function is dropping the lines that are comments
        """
        lines_number = len(input_lines)
        clean_lines = []
        current_com = 0
        change = False

        if lines_number > 0:
            flag = True

        else:
            flag = False

        cur = 0

        while flag:
            if  ("/*" in input_lines[cur]) and JackTokenizer.not_a_string(
                    input_lines[cur].partition("/*")):
                while "*/" not in input_lines[cur]:  # multiline comment
                    cur += 1

                cur += 1
                temp_multiline = input_lines[cur].partition("*/")[2]
                current_com += 1

                if temp_multiline == "":
                    continue

                else:

                    clean_lines.append(temp_multiline)

            elif change:
                current_com = 0
                flag = False
                clean_lines = input_lines

            elif ("//" in input_lines[cur]) and JackTokenizer.not_a_string(input_lines[cur].partition("//")):
                temp_line = input_lines[cur].partition("//")[0]
                clean_lines.append(temp_line)

            elif input_lines[cur] != '':
                clean_lines.append(input_lines[cur])

            cur += 1
            if len(input_lines) == cur:
                flag = False

        return clean_lines

    def delete_white_spaces(self, input_arr: list) -> list:
        number_of_lines = len(input_arr)
        clean_lines = []
        for i in range(number_of_lines):
            if i == number_of_lines:
                break  # finished

            else:
                if not (self.is_it_inline_comment(input_arr, i) and not self.is_it_empty_line(input_arr, i)):
                    tmp = self.drop_white_space_from_command(input_arr, i)
                    if tmp != "":
                        clean_lines.append(tmp)
        return self.drop_comments_from_input(clean_lines)

    @staticmethod
    def is_it_string_constant(current_token: str) -> bool:
        """   StringConstant: '"' A sequence of Unicode characters not including double quote or newline '"'   """
        current_token = current_token.strip()
        return current_token[0] == '"' and current_token[-1] == '"' and len(current_token) >= 2

    @staticmethod
    def is_it_integer_constant(current_token: str) -> bool:
        """integerConstant: A decimal number in the range 0-32767."""
        return type(current_token[0]) == int()

    @staticmethod
    def turn_lines_into_tokens(input_lines: list) -> list:
        final_tokens_list = []
        current_token = ""
        is_in_st = False
        for line in input_lines:
            for char in line:

                if char in JackTokenizer.SYMBOLS_set and not is_in_st:
                    if current_token:
                        final_tokens_list.append(JackTokenizer.creat_token(current_token))
                        current_token = ""

                    final_tokens_list.append(JackTokenizer.creat_token(char))

                elif char == " " and not is_in_st:
                    if current_token:
                        final_tokens_list.append(JackTokenizer.creat_token(current_token))
                        current_token = ""

                elif char == '"' and not is_in_st:
                    if current_token:
                        final_tokens_list.append(JackTokenizer.creat_token(current_token))
                        current_token = ""

                    is_in_st = True
                    current_token += char

                elif char == '"' and is_in_st and current_token[-1] != '\\':
                    is_in_st = False
                    current_token += char

                    if current_token:
                        final_tokens_list.append(JackTokenizer.creat_token(current_token))
                        current_token = ""

                else:
                    current_token += char

        return final_tokens_list

    @staticmethod
    def creat_token(string: str) -> tuple:
        if string in JackTokenizer.SYMBOLS_set:
            return string, "symbol"

        if string in JackTokenizer.KEYWORDS_set:
            return string, "keyword"

        if string.isdecimal():
            return string, "integerConstant"

        if string[0] == '"' and string[-1] == '"':
            return string[1:-1], "stringConstant"

        return string, "identifier"

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return len(self.tokens_list) > self.cur_token_index

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if it has_more_tokens() is true.
        Initially there is no current token.
        """
        self.cur_token_index += 1
        if self.has_more_tokens():
            self.cmd = f"<{self.tokens_list[self.cur_token_index][1]}> {self.fix(self.tokens_list[self.cur_token_index][0])} </{self.tokens_list[self.cur_token_index][1]}>\n"
            self.current_token = self.fix(self.tokens_list[self.cur_token_index][0])

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        current_token_couple = self.tokens_list[self.cur_token_index]
        return current_token_couple[1]

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        current_token = self.tokens_list[self.cur_token_index][0]
        return current_token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        current_token = self.tokens_list[self.cur_token_index][0]

        if current_token == '<':
            current_token = "&lt;"

        elif current_token == '>':
            current_token = "&gt;"

        elif current_token == '"':
            current_token = "&quot;"

        elif current_token == '&':
            current_token = "&amp;"

        return current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        current_token = self.tokens_list[self.cur_token_index][0]
        return current_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        current_token = self.tokens_list[self.cur_token_index][0]
        return current_token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
        """
        current_token = self.tokens_list[self.cur_token_index][0]
        return current_token


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

"""explanation section for nil:"""

"""
The strip() method removes any leading (spaces at the beginning) and trailing (spaces at the end) characters (space is the default leading character to remove)
"""

"""
The partition() method searches for a specified string, and splits the string into a tuple containing three elements.

The first element contains the part before the specified string.

The second element contains the specified string.

The third element contains the part after the string.
"""
