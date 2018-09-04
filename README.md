## thicc ##

An x86_64 C compiler written in Python, hopefully with many tests.

Currently works for a small subset of C: 
* Programs
    - A single `.c` file with a single function
* Functions
    - `int` returning functions with no arguments, comprised of several statements.
* Statements
    - The `return` statement, which contains a single expression.
    - (int) Variable declarations (with optional initializations)
    - Expression evaluation
    - Conditional statement (if/else), each branch containing only a single statement.
* Expressions
    - Integer constants
    - Variable references
    - Unary operations: - ! ~
    - Binary operations: + - * / % == != < <= > >= && || & | ^ << >>
    - Variable assignment: = += -= \*= /= %= <<= >>= &= |= ^=
    - Pre/post increment and decrement: ++ --
    - Conditional Expressions (Ternary Operator): a ? b : c

They cannot yet print their output!  To check a program has correctly compiled, check the return code with `$?`:
```bash
$ thicc return_42.c
$ ./a.out
$ echo $?
42
```

### Install

To install for development:
```bash
$ python setup.py develop
```

### Run

This package will install the `thicc` command, which emulates the basic behviour of `gcc`:
```bash
$ thicc myfile.c            #Produces executable a.out
$ thicc -o myfile myfile.c  #Produces executable myfile
$ thicc -S myfile.c         #Produces assembly file myfile.s
```
Additionally, passing `--lex` or `--parse` will only run the lexer or parser and print the output.



### Tests

From the project directory, run:
```bash
$ python -m unittest discover
```
This runs a (growing) number of small unit tests and @nlsandler's tests from [https://github.com/nlsandler/write_a_c_compiler](https://github.com/nlsandler/write_a_c_compiler).

Following Nora Sandler's blog: [https://norasandler.com/2017/11/29/Write-a-Compiler.html](https://norasandler.com/2017/11/29/Write-a-Compiler.html).

