import pytest
from pyro.lexer import tokenize


def _strip_pos(tokens):
    """Strip line/col info from tokens for comparison convenience."""
    return [(typ, val) for typ, val, _line, _col in tokens]


def test_numbers():
    tokens = tokenize("42 3.14")
    assert _strip_pos(tokens) == [('NUMBER', 42), ('FLOAT', 3.14)]


def test_keywords():
    tokens = tokenize("func if else end make print")
    assert _strip_pos(tokens) == [
        ('KEYWORD', 'func'), ('KEYWORD', 'if'), ('KEYWORD', 'else'),
        ('KEYWORD', 'end'), ('KEYWORD', 'make'), ('KEYWORD', 'print')
    ]


def test_range():
    tokens = tokenize("1..5")
    assert _strip_pos(tokens) == [('NUMBER', 1), ('RANGE', '..'), ('NUMBER', 5)]


def test_this():
    tokens = tokenize("this")
    assert _strip_pos(tokens) == [('THIS', 'this')]


def test_identifiers():
    tokens = tokenize("foo bar_baz")
    assert _strip_pos(tokens) == [('IDENT', 'foo'), ('IDENT', 'bar_baz')]


def test_strings():
    tokens = tokenize('"hello" \'world\'')
    assert _strip_pos(tokens) == [('STRING', 'hello'), ('STRING', 'world')]


def test_operators():
    tokens = tokenize("== != <= >= + - * / %")
    stripped = _strip_pos(tokens)
    assert stripped == [
        ('OPERATOR', '=='), ('OPERATOR', '!='), ('OPERATOR', '<='),
        ('OPERATOR', '>='), ('OPERATOR', '+'), ('OPERATOR', '-'),
        ('OPERATOR', '*'), ('OPERATOR', '/'), ('OPERATOR', '%')
    ]


def test_logical_operators():
    tokens = tokenize("and or not")
    assert _strip_pos(tokens) == [
        ('OPERATOR', 'and'), ('OPERATOR', 'or'), ('OPERATOR', 'not')
    ]


def test_in_keyword():
    tokens = tokenize("for x in items")
    stripped = _strip_pos(tokens)
    assert stripped == [
        ('KEYWORD', 'for'), ('IDENT', 'x'), ('KEYWORD', 'in'), ('IDENT', 'items')
    ]


def test_comments_ignored():
    tokens = tokenize("x = 1 # this is a comment")
    stripped = _strip_pos(tokens)
    assert stripped == [('IDENT', 'x'), ('OPERATOR', '='), ('NUMBER', 1)]


def test_line_tracking():
    tokens = tokenize("x\ny")
    assert tokens[0][2] == 1  # x is on line 1
    assert tokens[1][2] == 2  # y is on line 2


def test_punctuation():
    tokens = tokenize("(){}[],;.:")
    stripped = _strip_pos(tokens)
    assert stripped == [
        ('PUNCT', '('), ('PUNCT', ')'), ('PUNCT', '{'), ('PUNCT', '}'),
        ('PUNCT', '['), ('PUNCT', ']'), ('PUNCT', ','), ('PUNCT', ';'),
        ('PUNCT', '.'), ('PUNCT', ':')
    ]
