class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FuncDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ClassDef(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class Constructor(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class IfStmt(ASTNode):
    def __init__(self, cond, then_body, else_body=None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class ForStmt(ASTNode):
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body

class WhileStmt(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class Assign(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class MemberAssign(ASTNode):
    def __init__(self, obj, attr, value):
        self.obj = obj    # e.g., Var('this')
        self.attr = attr  # string, e.g., 'name'
        self.value = value

class ExprStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class Return(ASTNode):
    def __init__(self, value):
        self.value = value

class BinOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class This(ASTNode):
    pass

class Range(ASTNode):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Call(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args
        
class MemberAccess(ASTNode):
    def __init__(self, obj, attr):
        self.obj = obj   # e.g., Var('this') or Var('x')
        self.attr = attr # string attribute name
