### thicc ###

A C compiler written in Python, hopefully with many tests.

# Install

To install for development:
```bash
$ python setup.py develop
```

# Run

This package will install the `thicc` command, which emulates the basic behviour of `gcc`:
```bash
$ thicc myfile.c   #Produces executable a.out
$ thicc -o myfile myfile.c #Produces executable myfile
```
Additionally, passing `--lex` or `--parse` will only run the lexer or parser and print the output.



# Tests

From the project directory, run:
```bash
$ python -m unittest discover
```
This runs a (growing) number of small unit tests and @nlsandler's tests from [https://github.com/nlsandler/write_a_c_compiler](https://github.com/nlsandler/write_a_c_compiler).

Following Nora Sandler's blog: [https://norasandler.com/2017/11/29/Write-a-Compiler.html](https://norasandler.com/2017/11/29/Write-a-Compiler.html).

