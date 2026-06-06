import pytest
from pyro.lexer import tokenize
from pyro.parser import Parser
from pyro.ast_nodes import *

def test_simple_assign():
    source = "x = 10"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    assert isinstance(ast, Program)
    assert len(ast.statements) == 1
    stmt = ast.statements[0]
    assert isinstance(stmt, Assign)
    assert stmt.target == "x"
    assert isinstance(stmt.value, Number)
    assert stmt.value.value == 10

def test_if_stmt():
    source = "if x > 5\nprint 'ok'\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, IfStmt)
    assert isinstance(stmt.cond, BinOp)
    assert stmt.cond.op == '>'
