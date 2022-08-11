# Jack Compiler (nand2tetris)

Compiler for the Jack programming language, part of the [nand2tetris computer architecture course](https://www.coursera.org/learn/build-a-computer).

## Usage
```
jack_compiler.py [-h] [--sym] jack_files

positional arguments:
  jack_files  Jack file (with .jack extension) or directory containing Jack files

optional arguments:
  -h, --help  show this help message and exit
  --sym       Write symbol tables to text
```

## TODO:
- [ ] Remove various calls to ```self._create_tag()``` in ```compilation_engine.py``` to make the compiler more readable. Perhaps make the writing of the parse tree XML happen in a seperate module.
- [ ] Only read the Jack code once. Advance the tokenizer, write the XML tag, and do compilation steps at once.
- [ ] Add informative error handling to compiler to notify user of syntax/grammar errors.