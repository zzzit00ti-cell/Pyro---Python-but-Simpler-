import pytest
from pyro.lexer import tokenize

def test_numbers():
    tokens = tokenize("42 3.14")
    assert tokens == [('NUMBER', 42), ('FLOAT', 3.14)]

def test_keywords():
    tokens = tokenize("func if else end make print")
    assert tokens == [
        ('KEYWORD', 'func'), ('KEYWORD', 'if'), ('KEYWORD', 'else'),
        ('KEYWORD', 'end'), ('KEYWORD', 'make'), ('KEYWORD', 'print')
    ]

def test_range():
    tokens = tokenize("1..5")
    assert tokens == [('NUMBER', 1), ('RANGE', '..'), ('NUMBER', 5)]

def test_this():
    tokens = tokenize("this")
    assert tokens == [('THIS', 'this')]
