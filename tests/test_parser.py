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


def test_make_assign():
    source = "make x = 10"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, Assign)
    assert stmt.target == "x"


def test_if_stmt():
    source = "if x > 5\nprint 'ok'\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, IfStmt)
    assert isinstance(stmt.cond, BinOp)
    assert stmt.cond.op == '>'


def test_if_else():
    source = "if x > 5\nprint 'yes'\nelse\nprint 'no'\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, IfStmt)
    assert stmt.else_body is not None
    assert len(stmt.else_body) == 1


def test_for_loop():
    source = "for i in 1..5\nprint i\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, ForStmt)
    assert stmt.var == 'i'
    assert isinstance(stmt.iterable, Range)


def test_while_loop():
    source = "while x > 0\nx = x - 1\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, WhileStmt)


def test_func_def():
    source = "func greet(name)\nprint name\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, FuncDef)
    assert stmt.name == 'greet'
    assert stmt.params == ['name']


def test_class_def():
    source = "class Dog\nconstructor(name)\nthis.name = name\nend\nfunc bark()\nprint this.name\nend\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, ClassDef)
    assert stmt.name == 'Dog'
    assert len(stmt.body) == 2  # constructor + bark method


def test_member_access():
    source = "this.name"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, ExprStmt)
    assert isinstance(stmt.expr, MemberAccess)


def test_function_call():
    source = "greet(\"world\")"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    stmt = ast.statements[0]
    assert isinstance(stmt, ExprStmt)
    assert isinstance(stmt.expr, Call)
    assert isinstance(stmt.expr.func, Var)
    assert stmt.expr.func.name == 'greet'


def test_return_stmt():
    source = "func add(a, b)\nreturn a + b\nend"
    tokens = tokenize(source)
    parser = Parser(tokens)
    ast = parser.parse()
    func = ast.statements[0]
    assert isinstance(func, FuncDef)
    ret = func.body[0]
    assert isinstance(ret, Return)
    assert isinstance(ret.value, BinOp)
