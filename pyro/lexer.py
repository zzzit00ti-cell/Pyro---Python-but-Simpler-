import re

KEYWORDS = {
    'func', 'class', 'if', 'else', 'for', 'while', 'return',
    'constructor', 'this', 'and', 'or', 'not', 'True', 'False',
    'None', 'import', 'from', 'as', 'try', 'except', 'finally',
    'raise', 'with', 'yield', 'end', 'make', 'print'
}

TOKEN_REGEX = re.compile(
    r'#[^\n]*|'
    r'"[^"\\]*(\\.[^"\\]*)*"|'
    r"'[^'\\]*(\\.[^'\\]*)*'|"
    r'\d+\.\d+|\d+|\.\.|'
    r'[a-zA-Z_][a-zA-Z0-9_]*|'
    r'[+\-*/%=<>!&|]+|'
    r'[(){}\[\],;.:]|'
    r'\n|'
    r'\S'
)

def tokenize(source):
    tokens = []
    line = 1
    col = 1
    for match in TOKEN_REGEX.finditer(source):
        tok = match.group()
        start_line = line
        start_col = col
        # Update line/col before processing
        if tok == '\n':
            line += 1
            col = 1
            continue
        # Skip comments
        if tok.startswith('#'):
            col += len(tok)
            continue
        # Classify token
        if tok in KEYWORDS:
            typ = 'KEYWORD'
        elif tok.isdigit():
            typ = 'NUMBER'
            tok = int(tok)
        elif re.match(r'\d+\.\d+', tok):
            typ = 'FLOAT'
            tok = float(tok)
        elif tok == '..':
            typ = 'RANGE'
        elif tok in ('+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                     'and', 'or', 'not', '//', '**', '@'):
            typ = 'OPERATOR'
        elif tok == 'this':
            typ = 'THIS'
        elif tok in '(){},;:.':
            typ = 'PUNCT'
        elif tok.isidentifier():
            typ = 'IDENT'
        elif tok.startswith('"') or tok.startswith("'"):
            typ = 'STRING'
            tok = eval(tok)  # safe for simple strings
        else:
            typ = 'UNKNOWN'
        tokens.append((typ, tok, start_line, start_col))
        col += len(match.group())
    return tokens
