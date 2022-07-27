import os
import argparse
import re

from tokenizer import Tokenizer
from compilation_engine import CompilationEngine

class Analyzer:
    def __init__(self, target_path):
        if os.path.isdir(target_path):
            self.jack_files = [
                os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith('.jack')
            ]
            if len(self.jack_files) == 0:
                raise ValueError('No jack files found in the target directory')
        elif os.path.isfile(target_path) and target_path.endswith('.jack'):
            self.jack_files = [target_path]
        else:
            raise ValueError('Target file is a not a jack file')


    def analyze(self):
        parser_output_files = []

        for jack_file in self.jack_files:
            print(f'Analyzing {jack_file}...')

            target_dir = os.path.join(os.path.dirname(jack_file), 'target')
            if not os.path.isdir(target_dir):
                os.mkdir(target_dir)
            basename = os.path.basename(jack_file).split('.')[0]

            tokenizer_output_file = os.path.join(target_dir, basename+'T.xml')
            parser_output_file = os.path.join(target_dir, basename+'.xml')

            tokenizer = Tokenizer(jack_file)
            compilation_engine = CompilationEngine(tokenizer)

            # Writing the *T.xml file
            while tokenizer.has_more_tokens():
                token, token_type = tokenizer.advance()
                if token_type == 'stringConstant':
                    token = tokenizer.string_val()

                tokenizer.write_token_tag(token_type, token)

            tokenizer.write_xml_file(tokenizer_output_file)
            # Reinitialize current_token_index
            tokenizer.current_token_index = -1

            # Writing the analyzed *.xml file
            while tokenizer.has_more_tokens():
                token, token_type = tokenizer.advance()

                if token == 'class':
                    compilation_engine.compile_class(token, token_type)

            compilation_engine.wrtie_xml_file(parser_output_file)

            parser_output_files.append(parser_output_file)
        
        return parser_output_files


class TextComparer:
    def __init__(self, compare_file_path):
        if os.path.isdir(compare_file_path):
            self.compare_files = [
                os.path.join(compare_file_path, f) for f in os.listdir(compare_file_path)
                if f.endswith('.xml') and f[-5] != 'T'
            ]
            self.tokenizer_compare_files = [
                os.path.join(f, compare_file_path) for f in os.listdir(compare_file_path)
                if f.endswith('.xml') and f[-5] == 'T'
            ]
        elif os.path.isfile(compare_file_path) and compare_file_path.endswith('.xml'):
            self.compare_files = [compare_file_path]
        else:
            raise ValueError('Compare file is not a valid .xml file')

    def compare(self, output_files):
        output_files.sort()
        self.compare_files.sort()

        for output_file, compare_file in zip(output_files, self.compare_files):
            print(f'Comparing "{output_file}" with "{compare_file}"...')
            
            with open(output_file, 'r') as f:
                output_lines = f.readlines()
            with open(compare_file, 'r') as f:
                compare_lines = f.readlines()

            comparison_failure = False
            for l_index, (l_output, l_compare) in enumerate(zip(output_lines, compare_lines)):
                open_tag_pattern = '<([^/].*?)>'
                open_output = re.search(open_tag_pattern, l_output)
                open_compare = re.search(open_tag_pattern, l_compare)
                if open_output is not None:
                    if open_compare is None or open_output.group(1) != open_compare.group(1):
                        comparison_failure = True
                        print(f'Comparison failure at line {l_index} in file {output_file}')
                        print(f'Output line: {l_output}')
                        print(f'Compare line: {l_compare}\n')
                        break

                tag_text_pattern = '>(.*)<'
                text_output = re.search(tag_text_pattern, l_output)
                text_compare = re.search(tag_text_pattern, l_compare)
                if text_output is not None:
                    if text_compare is None or text_output.group(1).strip() != text_compare.group(1).strip():
                        comparison_failure = True
                        print(f'Comparison failure at line {l_index} in file {output_file}')
                        print(f'Output line: {l_output}')
                        print(f'Compare line: {l_compare}\n')
                        break

                close_tag_pattern = '</(.*)>'
                close_output = re.search(close_tag_pattern, l_output)
                close_compare = re.search(close_tag_pattern, l_compare)
                if close_output is not None:
                    if close_compare is None or close_output.group(1) != close_compare.group(1):
                        comparison_failure = True
                        print(f'Comparison failure at line {l_index} in file {output_file}')
                        print(f'Output line: {l_output}')
                        print(f'Compare line: {l_compare}\n')
                        break
            
            if not comparison_failure:
                print('Success!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j',
        '--jack_files',
        help='Jack file (with .jack extension) or directory containing Jack files'
    )
    parser.add_argument(
        '-c',
        '--compare_files',
        help='Existing .xml file or directory of .xml files to compare analyzer output to'
    )
    parser.add_argument(
        '-t',
        '--testall',
        help='Test the Jack analyzer on the seven provided .jack files',
        action='store_true'
    )
    args = parser.parse_args()

    if args.testall:
        print('Testing all sample Jack files...')
        jack_dirs = ['ArrayTest', 'ExpressionLessSquare', 'Square']

        for jack_dir in jack_dirs:
            analyzer = Analyzer(jack_dir)
            output_files = analyzer.analyze()

            comparer = TextComparer(jack_dir)
            comparer.compare(output_files)

    elif args.compare_files and not args.jack_files:
        print(
            'Error. When providing compare_file(s), also provide a Jack file '
            'or directory of Jack files to compare to with the "-j" argument.'
            '\n\nEXAMPLE:'
            '\npython jack_analyzer.py -j Square/Main.jack -c Square/Main.xml'
        )
        
    elif args.jack_files:
        jack_analyzer = Analyzer(args.jack_files)
        output_files = jack_analyzer.analyze()

        if args.compare_files:
            comparer = TextComparer(args.compare_files)
            comparer.compare(output_files)
