import os
import json


class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.static_index = 0
        self.field_index = 0

    def start_subroutine(self):
        self.subroutine_table = {}
        self.arg_index = 0
        self.var_index = 0

    def define(self, name: str, type: str, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a
        running index. STATIC and FIELD identifiers have a class scope, while ARG and
        VAR identifiers have a subroutine scope
        """

        # print(f"Defining symbol with name: {name} ; type: {type} ; kind: {kind}")

        if kind == "static":
            self.class_table[name] = (kind, type, self.static_index)
            self.static_index += 1
        elif kind == "field":
            self.class_table[name] = (kind, type, self.field_index)
            self.field_index += 1
        elif kind == "arg":
            self.subroutine_table[name] = (kind, type, self.arg_index)
            self.arg_index += 1
        elif kind == "var":
            self.subroutine_table[name] = (kind, type, self.var_index)
            self.var_index += 1
        else:
            # TODO: Enumerate various values allowable for kind?
            raise ValueError(f'Symbol with name: "{name}" has invalid kind: "{kind}"')

    def lookup(self, name: str) -> tuple:
        kind = self._kind_of(name)
        if kind is None:
            # TODO: Define the symbol here or raise an var undefined error?
            raise ValueError(f'Identifier "{name}" is not defined in the current scope')
        type = self._type_of(name)
        index = self._index_of(name)

        return kind, type, index

    def var_count(self, kind: str) -> int:
        """
        Returns the number of variables of the given kind already defined in the
        current scope.
        """
        if kind == "static":
            return self.static_index
        elif kind == "field":
            return self.field_index
        elif kind == "arg":
            return self.arg_index
        elif kind == "var":
            return self.var_index

    def _kind_of(self, name: str):
        """
        Returns the kind of the named identifier in the current scope. Returns NONE if
        the identifier is unknown in the current scope
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name][0]
        elif name in self.class_table:
            return self.class_table[name][0]
        else:
            return None

    def _type_of(self, name: str) -> str:
        """Returns the type of the named identifier in the current scope"""
        if name in self.subroutine_table:
            return self.subroutine_table[name][1]
        elif name in self.class_table:
            return self.class_table[name][1]
        else:
            raise ValueError(
                f'Cannot get type of identifier "{name}" as it is not defined in the '
                "current scope"
            )

    def _index_of(self, name: str) -> int:
        if name in self.subroutine_table:
            return self.subroutine_table[name][2]
        elif name in self.class_table:
            return self.class_table[name][2]
        else:
            raise ValueError(
                f'Cannot get index of identifier "{name}" as it is not defined in the '
                "current scope"
            )

    def write_symbol_tables(self, dir: str) -> None:
        """Wrtie symbol tables as strings to .txt files"""
        if not os.path.isdir(dir):
            os.mkdir(dir)

        with open(os.path.join(dir, "class_table.txt"), "w") as f:
            f.write(json.dumps(self.class_table, indent=2))
        with open(os.path.join(dir, "subroutine_table.txt"), "w") as f:
            f.write(json.dumps(self.subroutine_table, indent=2))
