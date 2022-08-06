import os
import argparse

from compilation_engine import CompilationEngine
from tokenizer import Tokenizer


class JackCompiler:
    def __init__(self, target_path):
        if os.path.isdir(target_path):
            self.jack_fns = [
                os.path.join(target_path, fn)
                for fn in os.listdir(target_path)
                if fn.endswith(".jack")
            ]
            if len(self.jack_fns) == 0:
                raise ValueError("No jack files found in the target directory")
        elif os.path.isfile(target_path) and target_path.endswith(".jack"):
            self.jack_fns = [target_path]
        else:
            raise ValueError("Target file is a not a jack file")

    def compile(self):
        vm_fns = []

        for jack_fn in self.jack_fns:
            print(f"Compiling {jack_fn}")

            vm_dir = os.path.join(os.path.dirname(jack_fn), "vm")
            if not os.path.isdir(vm_dir):
                os.mkdir(vm_dir)
            basename = os.path.basename(jack_fn).split(".")[0]

            tokenizer = Tokenizer(jack_fn)
            compilation_engine = CompilationEngine(tokenizer, basename, vm_dir)

            # Run compilation engine to generate XML parse tree and compiled VM code
            while tokenizer.has_more_tokens():
                token, token_type = tokenizer.advance()

                if token == "class":
                    compilation_engine.compile_class(token, token_type)
                else:
                    raise SyntaxError(
                        f'Expected Jack file with one class, got token "{token}" with '
                        f'type: "{token_type}"'
                    )

            # vm_writer.close()
            # vm_fns.append(vm_fn)

            parse_tree_fn = os.path.join(vm_dir, basename + ".xml")
            compilation_engine.wrtie_xml_file(parse_tree_fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "jack_files",
        help="Jack file (with .jack extension) or directory containing Jack files",
    )
    args = parser.parse_args()

    if args.jack_files:
        compiler = JackCompiler(args.jack_files)
        compiler.compile()
    else:
        print("Please provide one or more Jack files. See help below:\n")
        parser.print_help()
