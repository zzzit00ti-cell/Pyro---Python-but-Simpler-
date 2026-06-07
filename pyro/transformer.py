from .ast_nodes import *


class PyTransformer:
    def __init__(self):
        self.indent = 0

    def indent_str(self):
        return "    " * self.indent

    def transform(self, node):
        if isinstance(node, Program):
            return "\n".join(self.transform(stmt) for stmt in node.statements)

        elif isinstance(node, FuncDef):
            params = ", ".join(node.params)
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            return f"{self.indent_str()}def {node.name}({params}):\n{body}"

        elif isinstance(node, ClassDef):
            header = f"{self.indent_str()}class {node.name}:"
            self.indent += 1
            members = []
            for stmt in node.body:
                if isinstance(stmt, Constructor):
                    params = stmt.params[:]
                    if not params or params[0] != 'self':
                        params.insert(0, 'self')
                    self.indent += 1
                    ctor_body = self._transform_body(stmt.body)
                    self.indent -= 1
                    members.append(f"{self.indent_str()}def __init__({', '.join(params)}):\n{ctor_body}")
                elif isinstance(stmt, FuncDef):
                    # Make a copy of params to avoid mutating the AST
                    original_params = stmt.params[:]
                    if not stmt.params or stmt.params[0] != 'self':
                        stmt.params.insert(0, 'self')
                    members.append(self.transform(stmt))
                    # Restore original params
                    stmt.params = original_params
                else:
                    members.append(self.transform(stmt))
            self.indent -= 1
            if not members:
                members.append(f"{self.indent_str()}    pass")
            class_body = "\n".join(members)
            return f"{header}\n{class_body}"

        elif isinstance(node, Constructor):
            params = node.params[:]
            if not params or params[0] != 'self':
                params.insert(0, 'self')
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            return f"{self.indent_str()}def __init__({', '.join(params)}):\n{body}"

        elif isinstance(node, IfStmt):
            cond = self.transform(node.cond)
            self.indent += 1
            then_body = self._transform_body(node.then_body)
            self.indent -= 1
            result = f"{self.indent_str()}if {cond}:\n{then_body}"
            if node.else_body:
                self.indent += 1
                else_body = self._transform_body(node.else_body)
                self.indent -= 1
                result += f"\n{self.indent_str()}else:\n{else_body}"
            return result

        elif isinstance(node, ForStmt):
            var = node.var
            if isinstance(node.iterable, Range):
                start = self.transform(node.iterable.start)
                end = self.transform(node.iterable.end)
                iterable = f"range({start}, {end} + 1)"
            else:
                iterable = self.transform(node.iterable)
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            return f"{self.indent_str()}for {var} in {iterable}:\n{body}"

        elif isinstance(node, WhileStmt):
            cond = self.transform(node.cond)
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            return f"{self.indent_str()}while {cond}:\n{body}"

        elif isinstance(node, Assign):
            value = self.transform(node.value)
            return f"{self.indent_str()}{node.target} = {value}"

        elif isinstance(node, MemberAssign):
            obj = self.transform(node.obj)
            value = self.transform(node.value)
            return f"{self.indent_str()}{obj}.{node.attr} = {value}"

        elif isinstance(node, MemberAccess):
            obj = self.transform(node.obj)
            return f"{obj}.{node.attr}"

        elif isinstance(node, ExprStmt):
            expr = self.transform(node.expr)
            return f"{self.indent_str()}{expr}"

        elif isinstance(node, Return):
            if node.value:
                val = self.transform(node.value)
                return f"{self.indent_str()}return {val}"
            return f"{self.indent_str()}return"

        elif isinstance(node, BinOp):
            if node.op == 'not':
                right = self.transform(node.right)
                return f"(not {right})"
            left = self.transform(node.left)
            right = self.transform(node.right)
            return f"({left} {node.op} {right})"

        elif isinstance(node, Number):
            return str(node.value)

        elif isinstance(node, String):
            return repr(node.value)

        elif isinstance(node, Var):
            return node.name

        elif isinstance(node, This):
            return "self"

        elif isinstance(node, Range):
            start = self.transform(node.start)
            end = self.transform(node.end)
            return f"range({start}, {end} + 1)"

        elif isinstance(node, Call):
            func = self.transform(node.func)
            args = ", ".join(self.transform(a) for a in node.args)
            return f"{func}({args})"

        else:
            raise TypeError(f"Unknown AST node: {type(node)}")

    def _transform_body(self, stmts):
        """Transform a list of body statements, each already indented by current level."""
        if not stmts:
            return f"{self.indent_str()}pass"
        return "\n".join(self.transform(stmt) for stmt in stmts)
