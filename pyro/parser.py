from .ast_nodes import (
    Program, FuncDef, ClassDef, Constructor, IfStmt, ForStmt, WhileStmt,
    Assign, MemberAssign, ExprStmt, Return, BinOp, Number, String, Var, This, Range, Call
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.in_class = False   # flag to allow 'constructor' keyword

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

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
        # Constructor is only allowed inside a class
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
        if self.match('IDENT'):
            target_name = self.consume('IDENT')[1]
            # Check for member access: this.attr
            if self.match('PUNCT', '.'):
                self.consume('PUNCT', '.')
                attr = self.consume('IDENT')[1]
                if self.match('OPERATOR', '='):
                    self.consume('OPERATOR', '=')
                    value = self.parse_expr()
                    obj = Var(target_name)
                    return MemberAssign(obj, attr, value)
                else:
                    self.pos -= 3
                    expr = self.parse_expr()
                    return ExprStmt(expr)
            elif self.match('OPERATOR', '='):
                self.consume('OPERATOR', '=')
                value = self.parse_expr()
                return Assign(target_name, value)
            else:
                self.pos -= 1
                expr = self.parse_expr()
                return ExprStmt(expr)
        expr = self.parse_expr()
        return ExprStmt(expr)

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
        body = self.parse_block(stop_on=['end'])
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
        body = self.parse_block(stop_on=['end'])
        return FuncDef(name, params, body)

    def parse_class(self):
        self.consume('KEYWORD', 'class')
        name = self.consume('IDENT')[1]
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        # Enter class context
        old_in_class = self.in_class
        self.in_class = True
        body = self.parse_block(stop_on=['end'])
        self.in_class = old_in_class
        return ClassDef(name, body)

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        cond = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        then_body = self.parse_block(stop_on=['end', 'else'])
        else_body = None
        if self.match('KEYWORD', 'else'):
            self.consume('KEYWORD', 'else')
            if self.match('PUNCT', ':'):
                self.consume('PUNCT', ':')
            else_body = self.parse_block(stop_on=['end'])
        # Consume the final 'end' (already consumed by parse_block)
        return IfStmt(cond, then_body, else_body)

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        var = self.consume('IDENT')[1]
        self.consume('KEYWORD', 'in')
        iterable = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block(stop_on=['end'])
        return ForStmt(var, iterable, body)

    def parse_while(self):
        self.consume('KEYWORD', 'while')
        cond = self.parse_expr()
        if self.match('PUNCT', ':'):
            self.consume('PUNCT', ':')
        body = self.parse_block(stop_on=['end'])
        return WhileStmt(cond, body)

    def parse_block(self, stop_on=None):
        """Parse a block of statements until a keyword in stop_on is encountered."""
        if stop_on is None:
            stop_on = ['end']
        stmts = []
        while self.peek():
            if self.match('KEYWORD') and self.peek()[1] in stop_on:
                # Stop before the terminating keyword (consume it outside)
                break
            stmts.append(self.parse_statement())
        # Consume the terminating keyword (end, else, etc.)
        if self.match('KEYWORD') and self.peek()[1] in stop_on:
            self.consume('KEYWORD', self.peek()[1])
        return stmts

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
        if self.match('NUMBER'):
            val = self.consume('NUMBER')[1]
            return Number(val)
        if self.match('STRING'):
            val = self.consume('STRING')[1]
            return String(val)
        if self.match('IDENT'):
            name = self.consume('IDENT')[1]
            if self.match('PUNCT', '('):
                self.consume('PUNCT', '(')
                args = []
                if not self.match('PUNCT', ')'):
                    while True:
                        args.append(self.parse_expr())
                        if self.match('PUNCT', ')'):
                            break
                        self.consume('PUNCT', ',')
                self.consume('PUNCT', ')')
                return Call(Var(name), args)
            return Var(name)
        if self.match('THIS'):
            self.consume('THIS')
            return This()
        if self.match('PUNCT', '('):
            self.consume('PUNCT', '(')
            expr = self.parse_expr()
            self.consume('PUNCT', ')')
            return expr
        # Range literal: number .. number
        if self.match('NUMBER'):
            left = self.parse_primary()
            if self.match('RANGE'):
                self.consume('RANGE')
                right = self.parse_primary()
                return Range(left, right)
            return left
        raise SyntaxError(f"Unexpected token: {self.peek()}")
