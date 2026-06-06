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
    r'\S'
)

def tokenize(source):
    tokens = []
    for match in TOKEN_REGEX.finditer(source):
        tok = match.group()
        if tok.startswith('#'):
            continue
        if tok in KEYWORDS:
            tokens.append(('KEYWORD', tok))
        elif tok.isdigit():
            tokens.append(('NUMBER', int(tok)))
        elif re.match(r'\d+\.\d+', tok):
            tokens.append(('FLOAT', float(tok)))
        elif tok == '..':
            tokens.append(('RANGE', '..'))
        elif tok in ('+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                     'and', 'or', 'not', '//', '**', '@'):
            tokens.append(('OPERATOR', tok))
        elif tok == 'this':
            tokens.append(('THIS', 'this'))
        elif tok in '(){},;:.':
            tokens.append(('PUNCT', tok))
        elif tok.isidentifier():
            tokens.append(('IDENT', tok))
        elif tok.startswith('"') or tok.startswith("'"):
            # safe eval for string literals
            tokens.append(('STRING', eval(tok)))
        else:
            tokens.append(('UNKNOWN', tok))
    return tokens
