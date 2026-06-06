from .ast_nodes import *

class PyTransformer:
    def __init__(self):
        self.indent = 0

    def indent_str(self):
        return "    " * self.indent

    def _indent_lines(self, text):
        """Add current indentation to every line of a multi-line string."""
        if not text:
            return ""
        lines = text.splitlines()
        indented = "\n".join(self.indent_str() + line if line.strip() else self.indent_str() for line in lines)
        return indented

    def transform(self, node):
        if isinstance(node, Program):
            return "\n".join(self.transform(stmt) for stmt in node.statements)

        elif isinstance(node, FuncDef):
            params = ", ".join(node.params)
            self.indent += 1
            body_lines = []
            for stmt in node.body:
                body_lines.append(self.transform(stmt))
            body = "\n".join(body_lines)
            body = self._indent_lines(body)
            self.indent -= 1
            return f"def {node.name}({params}):\n{body}"

        elif isinstance(node, ClassDef):
            self.indent += 1
            members = []
            for stmt in node.body:
                if isinstance(stmt, Constructor):
                    # Transform constructor to __init__
                    params = stmt.params[:]
                    if not params or params[0] != 'self':
                        params.insert(0, 'self')
                    self.indent += 1
                    body_lines = []
                    for s in stmt.body:
                        body_lines.append(self.transform(s))
                    body = "\n".join(body_lines)
                    body = self._indent_lines(body)
                    self.indent -= 1
                    members.append(f"def __init__({', '.join(params)}):\n{body}")
                elif isinstance(stmt, FuncDef):
                    # Method: ensure 'self' is first parameter
                    if not stmt.params or stmt.params[0] != 'self':
                        stmt.params.insert(0, 'self')
                    members.append(self.transform(stmt))
                else:
                    members.append(self.transform(stmt))
            self.indent -= 1
            if members:
                class_body = "\n".join(members)
            else:
                class_body = self.indent_str() + "    pass"
            return f"class {node.name}:\n{class_body}"

        elif isinstance(node, Constructor):
            # Normally handled inside ClassDef, but keep for completeness
            params = node.params[:]
            if not params or params[0] != 'self':
                params.insert(0, 'self')
            self.indent += 1
            body_lines = []
            for stmt in node.body:
                body_lines.append(self.transform(stmt))
            body = "\n".join(body_lines)
            body = self._indent_lines(body)
            self.indent -= 1
            return f"def __init__({', '.join(params)}):\n{body}"

        elif isinstance(node, IfStmt):
            cond = self.transform(node.cond)
            self.indent += 1
            then_lines = []
            for stmt in node.then_body:
                then_lines.append(self.transform(stmt))
            then_body = "\n".join(then_lines)
            then_body = self._indent_lines(then_body)
            self.indent -= 1
            result = f"if {cond}:\n{then_body}"
            if node.else_body:
                self.indent += 1
                else_lines = []
                for stmt in node.else_body:
                    else_lines.append(self.transform(stmt))
                else_body = "\n".join(else_lines)
                else_body = self._indent_lines(else_body)
                self.indent -= 1
                result += f"\nelse:\n{else_body}"
            return result

        elif isinstance(node, ForStmt):
            var = node.var
            # Transform range literal 1..5 -> range(1,6)
            if isinstance(node.iterable, Range):
                start = self.transform(node.iterable.start)
                end = self.transform(node.iterable.end)
                iterable = f"range({start}, {end}+1)"
            else:
                iterable = self.transform(node.iterable)
            self.indent += 1
            body_lines = []
            for stmt in node.body:
                body_lines.append(self.transform(stmt))
            body = "\n".join(body_lines)
            body = self._indent_lines(body)
            self.indent -= 1
            return f"for {var} in {iterable}:\n{body}"

        elif isinstance(node, WhileStmt):
            cond = self.transform(node.cond)
            self.indent += 1
            body_lines = []
            for stmt in node.body:
                body_lines.append(self.transform(stmt))
            body = "\n".join(body_lines)
            body = self._indent_lines(body)
            self.indent -= 1
            return f"while {cond}:\n{body}"

        elif isinstance(node, Assign):
            value = self.transform(node.value)
            return f"{node.target} = {value}"

        elif isinstance(node, ExprStmt):
            expr = self.transform(node.expr)
            return f"{expr}"

        elif isinstance(node, Return):
            if node.value:
                val = self.transform(node.value)
                return f"return {val}"
            return "return"

        elif isinstance(node, BinOp):
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
            return f"range({start}, {end}+1)"

        elif isinstance(node, Call):
            func = self.transform(node.func)
            args = ", ".join(self.transform(a) for a in node.args)
            return f"{func}({args})"

        else:
            raise TypeError(f"Unknown AST node: {type(node)}")
