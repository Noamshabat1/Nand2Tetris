"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.Symbol_func = dict() # the dic holds : key :(name) ---- value:(type , kind, index) - arg, var
        self.Symbol_class = dict() # the dic holds : key :(name) ---- value:(type , kind, index) - static, field
        self.count_Static = 0
        self.count_Field = 0
        self.count_Var = 0
        self.count_Args = 0


    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's symbol table).
        """
        self.count_Var = 0 # statr of new subroutine scope
        self.count_Args = 0 # statr of new subroutine scope
        self.Symbol_func.clear() # statr of new subroutine scope


    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind in {"STATIC", "FIELD"}:
            if kind == "STATIC":
                self.Symbol_func[name] = (type, kind, self.count_Static)
                self.count_Static +=1

            else: # kind == "FIELD"
                self.Symbol_func[name] = (type, kind, self.count_Field)
                self.count_Field +=1

        else: # kind is one of Args or Vars
            if kind == "ARG":
                self.Symbol_func[name] = (type, kind, self.count_Args)
                self.count_Args +=1

            else: # kind == "VAR"
                self.Symbol_func[name] = (type, kind, self.count_Var)
                self.count_Var +=1


    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind == "STATIC":
            return self.count_Static

        if kind == "FIELD":
            return self.count_Field

        if kind == "ARG":
            return self.count_Args

        if kind == "VAR":
            return self.count_Var


    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.Symbol_func:
            return self.Symbol_func[name][1]


        elif name in self.Symbol_class:
            return self.Symbol_class[name][1]

        else:
            return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.Symbol_func:
            return self.Symbol_func[name][0]


        elif name in self.Symbol_class:
            return self.Symbol_class[name][0]

        else:
            return None


    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.Symbol_func:
            return self.Symbol_func[name][2]


        elif name in self.Symbol_class:
            return self.Symbol_class[name][2]

        else:
            return None
