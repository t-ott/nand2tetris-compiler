import os


class VMWriter:
    def __init__(self, vm_fn):
        self.vm_fn = vm_fn
        self.vm_lines = []

    def write_push(self, segment, index: int) -> None:
        self.vm_lines.append(f"push {segment} {index}")

    def write_pop(self, segment, index: int) -> None:
        self.vm_lines.append(f"pop {segment} {index}")

    def write_arithmetic(self, op_symbol: str):
        if op_symbol == "+":
            self.vm_lines.append("add")
        elif op_symbol == "-":
            self.vm_lines.append("sub")
        elif op_symbol == "*":
            # Use built-in Math library
            self.write_call("Math.multiply", 2)
        elif op_symbol == "/":
            # Use built-in Math library
            self.write_call("Math.divide", 2)
        elif op_symbol == "&":
            self.vm_lines.append("and")
        elif op_symbol == "|":
            self.vm_lines.append("or")
        elif op_symbol == "<":
            self.vm_lines.append("lt")
        elif op_symbol == ">":
            self.vm_lines.append("gt")
        elif op_symbol == "=":
            self.vm_lines.append("eq")
        else:
            raise SyntaxError(
                f'op_symbol "{op_symbol}" not implementated into '
                "vm_writer.write_arthimetic()"
            )

    def write_unary_arithmetic(self, unary_op_symbol: str):
        if unary_op_symbol == "-":
            self.vm_lines.append("neg")
        elif unary_op_symbol == "~":
            self.vm_lines.append("not")
        else:
            raise SyntaxError(
                f'unary_op_symbol "{unary_op_symbol}" not implemented into '
                "vm_writer.write_unary_arithmetic()"
            )

    def write_label(self, label: str):
        self.vm_lines.append(f"label {label}")

    def write_goto(self, label: str):
        self.vm_lines.append(f"goto {label}")

    def write_if(self, label: str):
        self.vm_lines.append(f"if-goto {label}")

    def write_call(self, name: str, n_args: int) -> None:
        self.vm_lines.append(f"call {name} {n_args}")

    def write_function(self, name: str, n_locals: int) -> None:
        # deal with constructors
        if name.endswith(".new"):
            self.vm_lines.append(f"function {name} 0")

            # TODO: Remove this print statement
            # print(f"WARNING: Allocating {n_locals} fields for object. Is this correct?")

            # allocate memory for appropriate number of object fields and pop
            # base address of new object
            self.write_push("constant", str(n_locals))
            self.write_call("Memory.alloc", 1)
            self.write_pop("pointer", 0)

        else:
            self.vm_lines.append(f"function {name} {n_locals}")

    def write_return(self, is_void=False):
        # TODO: Is the param is_void even necessary? Other way to tell if it's void?
        if is_void:
            self.vm_lines.append("push constant 0")
        self.vm_lines.append("return")

    def close(self):
        if os.path.exists(self.vm_fn):
            print(f"Overwriting {self.vm_fn}")
            os.remove(self.vm_fn)

        with open(self.vm_fn, "w") as f:
            f.write("\n".join(self.vm_lines))
            f.write("\n")
