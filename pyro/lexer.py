import re

KEYWORDS = {
    'func', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
    'constructor', 'and', 'or', 'not', 'True', 'False',
    'None', 'import', 'from', 'as', 'try', 'except', 'finally',
    'raise', 'with', 'yield', 'end', 'make', 'print', 'in'
}

# Multi-char operators must come before single-char to avoid greedy mismatches
TOKEN_REGEX = re.compile(
    r'#[^\n]*|'                           # comments
    r'"[^"\\]*(\\.[^"\\]*)*"|'            # double-quoted strings
    r"'[^'\\]*(\\.[^'\\]*)*'|"            # single-quoted strings
    r'\d+\.\d+|'                          # float literals
    r'\d+|'                               # integer literals
    r'\.\.|'                              # range operator
    r'[a-zA-Z_][a-zA-Z0-9_]*|'           # identifiers/keywords
    r'==|!=|<=|>=|\*\*|//|'               # multi-char operators (must be before single-char)
    r'[+\-*/%=<>]|'                       # single-char operators
    r'[(){}[\],;.:]|'                     # punctuation
    r'\n|'                                # newlines
    r'\S'                                 # catch-all
)


def tokenize(source):
    tokens = []
    line = 1
    col = 1
    for match in TOKEN_REGEX.finditer(source):
        tok = match.group()
        start_line = line
        start_col = col
        # Update line/col for newlines
        if tok == '\n':
            line += 1
            col = 1
            continue
        # Skip comments
        if tok.startswith('#'):
            col += len(tok)
            continue
        # Classify token
        if tok == 'this':
            typ = 'THIS'
        elif tok in ('and', 'or', 'not'):
            typ = 'OPERATOR'
        elif tok in ('True', 'False', 'None'):
            typ = 'KEYWORD'
        elif tok in KEYWORDS:
            typ = 'KEYWORD'
        elif re.fullmatch(r'\d+\.\d+', tok):
            typ = 'FLOAT'
            tok = float(tok)
        elif tok.isdigit() or re.fullmatch(r'\d+', tok):
            typ = 'NUMBER'
            tok = int(tok)
        elif tok == '..':
            typ = 'RANGE'
        elif tok in ('+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                     '//', '**', '@'):
            typ = 'OPERATOR'
        elif tok in '(){}[],;.:':
            typ = 'PUNCT'
        elif tok.isidentifier():
            typ = 'IDENT'
        elif tok.startswith('"') or tok.startswith("'"):
            typ = 'STRING'
            tok = eval(tok)  # safe for simple string literals
        else:
            typ = 'UNKNOWN'
        tokens.append((typ, tok, start_line, start_col))
        col += len(match.group())
    return tokens
