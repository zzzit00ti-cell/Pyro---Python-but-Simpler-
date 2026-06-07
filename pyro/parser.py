from .ast_nodes import (
    Program, FuncDef, ClassDef, Constructor, IfStmt, ForStmt, WhileStmt,
    Assign, MemberAssign, ExprStmt, Return, BinOp, Number, String, Var, This, Range, Call, MemberAccess
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.in_class = False

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        tok = self.peek()
        if not tok:
            raise SyntaxError("Unexpected end of input")
        if expected_type and tok[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {tok[0]} '{tok[1]}'")
        if expected_value and tok[1] != expected_value:
            raise SyntaxError(f"Expected '{expected_value}', got '{tok[1]}'")
        self.pos += 1
        return tok

    def match(self, typ, val=None):
        tok = self.peek()
        if not tok:
            return False
        if tok[0] != typ:
            return False
        if val is not None and tok[1] != val:
            return False
        return True

    def parse(self):
        stmts = []
        while self.peek():
            stmts.append(self.parse_statement())
        return Program(stmts)

    def parse_statement(self):
        # Constructor only inside class
        if self.in_class and self.match('KEYWORD', 'constructor'):
            return self.parse_constructor()

        if self.match('KEYWORD', 'func'):
            return self.parse_func()
        if self.match('KEYWORD', 'class'):
            return self.parse_class()
        if self.match('KEYWORD', 'if'):
            return self.parse_if()
        if self.match('KEYWORD', 'for'):
            return self.parse_for()
        if self.match('KEYWORD', 'while'):
            return self.parse_while()
        if self.match('KEYWORD', 'return'):
            self.consume('KEYWORD', 'return')
            val = self.parse_expr() if not self.match('KEYWORD', 'end') else None
            return Return(val)
        if self.match('KEYWORD', 'print'):
            self.consume('KEYWORD', 'print')
            expr = self.parse_expr()
            return ExprStmt(Call(Var('print'), [expr]))
        if self.match('KEYWORD', 'make'):
            self.consume('KEYWORD', 'make')
            target = self.consume('IDENT')[1]
            self.consume('OPERATOR', '=')
            value = self.parse_expr()
            return Assign(target, value)

        # Assignment or expression (including chained member access/call)
        lhs = self.parse_expr()
        if self.match('OPERATOR', '='):
            self.consume('OPERATOR', '=')
            rhs = self.parse_expr()
            if isinstance(lhs, Var):
                return Assign(lhs.name, rhs)
            elif isinstance(lhs, MemberAccess):
                return MemberAssign(lhs.obj, lhs.attr, rhs)
            else:
                raise SyntaxError("Invalid left-hand side in assignment")
        else:
            return ExprStmt(lhs)

    def parse_constructor(self):
        self.consume('KEYWORD', 'constructor')
        self.consume('PUNCT', '(')
        params = []
        if not self.match('PUNCT', ')'):
            while True:
                params.append(self.consume('IDENT')[1])
                if self.match('PUNCT', ')'):
                    break
                self.consume('PUNCT', ',')
        self.consume('PUNCT', ')')
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return Constructor(params, body)

    def parse_func(self):
        self.consume('KEYWORD', 'func')
        name = self.consume('IDENT')[1]
        self.consume('PUNCT', '(')
        params = []
        if not self.match('PUNCT', ')'):
            while True:
                params.append(self.consume('IDENT')[1])
                if self.match('PUNCT', ')'):
                    break
                self.consume('PUNCT', ',')
        self.consume('PUNCT', ')')
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return FuncDef(name, params, body)

    def parse_class(self):
        self.consume('KEYWORD', 'class')
        name = self.consume('IDENT')[1]
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        old = self.in_class
        self.in_class = True
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        self.in_class = old
        return ClassDef(name, body)

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        cond = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        then_body = self.parse_block()
        else_body = None
        if self.match('KEYWORD', 'else'):
            self.consume('KEYWORD', 'else')
            if self.match('PUNCT', ':'):
                self.consume('PUNCT', ':')
            else_body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return IfStmt(cond, then_body, else_body)

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        var = self.consume('IDENT')[1]
        self.consume('KEYWORD', 'in')
        iterable = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return ForStmt(var, iterable, body)

    def parse_while(self):
        self.consume('KEYWORD', 'while')
        cond = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return WhileStmt(cond, body)

    def parse_block(self):
        """Parse statements until 'end' or 'else' (do NOT consume them)."""
        stmts = []
        while self.peek() and not (self.match('KEYWORD') and self.peek()[1] in ('end', 'else')):
            stmts.append(self.parse_statement())
        return stmts

    # Expression parsing with precedence
    def parse_expr(self):
        return self.parse_conditional()

    def parse_conditional(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.match('OPERATOR', 'or'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_logical_and()
            left = BinOp(op, left, right)
        return left

    def parse_logical_and(self):
        left = self.parse_comparison()
        while self.match('OPERATOR', 'and'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_comparison()
            left = BinOp(op, left, right)
        return left

    def parse_comparison(self):
        left = self.parse_addition()
        while self.match('OPERATOR') and self.peek()[1] in ('==', '!=', '<', '>', '<=', '>='):
            op = self.consume('OPERATOR')[1]
            right = self.parse_addition()
            left = BinOp(op, left, right)
        return left

    def parse_addition(self):
        left = self.parse_multiplication()
        while self.match('OPERATOR') and self.peek()[1] in ('+', '-'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_multiplication()
            left = BinOp(op, left, right)
        return left

    def parse_multiplication(self):
        left = self.parse_primary()
        while self.match('OPERATOR') and self.peek()[1] in ('*', '/', '%', '//'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_primary()
            left = BinOp(op, left, right)
        return left

    def parse_primary(self):
        # Parse an atom, then allow chained .identifier and (args)
        node = self.parse_atom()
        while True:
            # Member access: .identifier
            if self.match('PUNCT', '.'):
                self.consume('PUNCT', '.')
                attr = self.consume('IDENT')[1]
                node = MemberAccess(node, attr)
            # Function call: ( args )
            elif self.match('PUNCT', '('):
                self.consume('PUNCT', '(')
                args = []
                if not self.match('PUNCT', ')'):
                    while True:
                        args.append(self.parse_expr())
                        if self.match('PUNCT', ')'):
                            break
                        self.consume('PUNCT', ',')
                self.consume('PUNCT', ')')
                node = Call(node, args)
            else:
                break
        return node

    def parse_atom(self):
        # Parenthesized expression
        if self.match('PUNCT', '('):
            self.consume('PUNCT', '(')
            expr = self.parse_expr()
            self.consume('PUNCT', ')')
            return expr

        # Number literal (with optional range)
        if self.match('NUMBER'):
            val = self.consume('NUMBER')[1]
            if self.match('RANGE'):
                self.consume('RANGE')
                right = self.parse_atom()
                if isinstance(right, Number):
                    return Range(Number(val), right)
                else:
                    raise SyntaxError("Expected number after '..'")
            return Number(val)

        # String literal
        if self.match('STRING'):
            val = self.consume('STRING')[1]
            return String(val)

        # 'this' keyword
        if self.match('THIS'):
            self.consume('THIS')
            return This()

        # Identifier
        if self.match('IDENT'):
            name = self.consume('IDENT')[1]
            return Var(name)

        raise SyntaxError(f"Unexpected token: {self.peek()}")
