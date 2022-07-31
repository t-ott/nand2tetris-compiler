import os
from symbol_table import SymbolTable

class VMWriter:
    def __init__(self, vm_fn):
        self.vm_fn = vm_fn
        self.vm_lines = []

    def write_push(self, segment, index: int) -> None:
        self.vm_lines.append(f'push {segment} {index}')

    def write_pop(self, segment, index: int):
        pass

    # def write_arithmetic(self, command):
    #     pass
    # original API suggestion ^ with command being ADD, SUB, GT, etc.

    def write_arithmetic(self, op_symbol: str):
        if op_symbol == '+':
            self.vm_lines.append('add')
        elif op_symbol == '-':
            self.vm_lines.append('sub')
        else:
            raise ValueError(
                f'op_symbol {op_symbol} not yet implementated into vm_writer.write_arthimetic()'
            )

    def write_label(self, label: str):
        pass

    def write_goto(self, label: str):
        pass

    def write_if(self, label: str):
        pass

    def write_call(self, name: str, n_args: int) -> None:
        self.vm_lines.append(f'call {name} {n_args}')

    def write_function(self, name: str, n_locals: int) -> None:
        self.vm_lines.append(f'function {name} {n_locals}')

    def write_return(self, is_void=False):
        # TODO: Is the param is_void even necessary? Other way to tell if it's void?
        if is_void:
            self.vm_lines.append("push constant 0")
        self.vm_lines.append("return")

    def close(self):
        if os.path.exists(self.vm_fn):
            print(f'Overwriting {self.vm_fn}')
            os.remove(self.vm_fn)

        with open(self.vm_fn, 'w') as f:
            f.write('\n'.join(self.vm_lines))
