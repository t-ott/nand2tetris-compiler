from xml.dom import minidom

KEYWORDS = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]

SYMBOLS = [
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
]


class Tokenizer:
    def __init__(self, jack_file: str):
        with open(jack_file) as f:
            jack = f.read()

        # Initialize xml
        self.tokenizer_root = minidom.Document()
        self.tokenizer_xml = self.tokenizer_root.createElement("tokens")
        self.tokenizer_root.appendChild(self.tokenizer_xml)

        # Pre-process jack code
        jack = self._remove_comment_lines(jack)
        jack = self._remove_inline_comments(jack)
        jack = self._remove_multi_line_comments(jack)
        jack = self._remove_whitespace(jack)

        self.tokens = self._get_tokens(jack)

        # Initialize token indexer, call self.advance() for first token
        self.current_token_index = -1
        self.current_token = None

    def _remove_comment_lines(self, jack: str) -> str:
        jack_lines = jack.splitlines()
        return "\n".join(
            [
                jack_line
                for jack_line in jack_lines
                if not jack_line.strip().startswith("//")
            ]
        )

    def _remove_inline_comments(self, jack: str) -> str:
        return "\n".join([jack_line.split("//")[0] for jack_line in jack.splitlines()])

    def _remove_multi_line_comments(self, jack: str) -> str:
        jack_chars = [char for char in jack]

        jack_no_comments = ""

        # manually enumerate char by char
        char_iter = enumerate(jack_chars)
        in_comment = False
        while True:
            index, char = next(char_iter)

            if not in_comment and char == "/" and jack_chars[index + 1] == "*":
                # start of comment
                in_comment = True
                next(char_iter)  # skip forward one char
            elif in_comment and char == "*" and jack_chars[index + 1] == "/":
                # end of comment
                in_comment = False
                next(char_iter)  # skip forward one char
            elif in_comment:
                # do not include this char
                continue
            else:
                jack_no_comments += char

            if index == len(jack_chars) - 1:
                # end of chars
                break

        return jack_no_comments

    def _remove_whitespace(self, jack: str) -> str:
        return "".join(line.strip() for line in jack.splitlines())

    def _get_tokens(self, jack: str) -> list:
        tokens = []

        current_token = ""
        in_token = False
        current_string_const = ""
        in_string_const = False

        for char in jack:
            if in_token:
                if char == " ":
                    # end of token, flush current_token
                    tokens.append(current_token)
                    current_token = ""
                    in_token = False
                elif char in SYMBOLS:
                    # end of token, flush current_token and add symbol token
                    tokens.append(current_token)
                    tokens.append(char)
                    current_token = ""
                    in_token = False
                else:
                    # continue current_token
                    current_token += char
            elif in_string_const:
                if char == '"':
                    # end of string_const, flush current_string_const
                    current_string_const += char
                    tokens.append(current_string_const)
                    current_string_const = ""
                    in_string_const = False
                else:
                    # continue string_const
                    current_string_const += char
            else:
                # not in_token or in_string_const
                if char in SYMBOLS:
                    tokens.append(char)
                elif char == '"':
                    # start of string_const
                    in_string_const = True
                    current_string_const += char
                elif char == " ":
                    # ignore spaces
                    continue
                else:
                    # start of new token
                    in_token = True
                    current_token += char

        return tokens

    def token_type(self, token):
        if token in KEYWORDS:
            return "keyword"
        elif token in SYMBOLS:
            return "symbol"

        try:
            int(token)
            return "integerConstant"
        except ValueError:
            pass

        if token.startswith('"'):
            return "stringConstant"
        else:
            return "identifier"

    def has_more_tokens(self) -> bool:
        return self.current_token_index < len(self.tokens) - 1

    def advance(self) -> tuple([str, str]):
        self.current_token_index += 1
        self.current_token = self.tokens[self.current_token_index]
        token_type = self.token_type(self.current_token)
        token = (
            self.string_val() if token_type == "stringConstant" else self.current_token
        )

        return token, token_type

    def string_val(self) -> str:
        # remove quotes around string const
        return self.current_token[1:-1]

    def write_token_tag(self, token_type: str, token: str):
        # write tag to *T.xml output
        tokenizer_tag = self.tokenizer_root.createElement(token_type)
        token_text = self.tokenizer_root.createTextNode(token)
        tokenizer_tag.appendChild(token_text)
        self.tokenizer_xml.appendChild(tokenizer_tag)

    def write_xml_file(self, output_file: str):
        xml_str = self.tokenizer_root.toprettyxml()
        # remove xml header
        xml_str = "\n".join([l for l in xml_str.splitlines()[1:]])
        with open(output_file, "w") as f:
            f.write(xml_str)
