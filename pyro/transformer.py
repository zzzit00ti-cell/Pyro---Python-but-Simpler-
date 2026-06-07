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
            param_strs = []
            for p in node.params:
                name, typ = p
                param_strs.append(f"{name}: {typ}" if typ else name)
            params = ", ".join(param_strs)
            
            decorators = ""
            if getattr(node, 'is_fast', False):
                decorators = f"{self.indent_str()}@__pyro_fast__\n"
            
            return_str = f" -> {node.return_type}" if getattr(node, 'return_type', None) else ""
            
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            return f"{decorators}{self.indent_str()}def {node.name}({params}){return_str}:\n{body}"

        elif isinstance(node, ClassDef):
            header = f"{self.indent_str()}class {node.name}:"
            self.indent += 1
            members = []
            for stmt in node.body:
                if isinstance(stmt, Constructor):
                    params = stmt.params[:]
                    if not params or params[0][0] != 'self':
                        params.insert(0, ('self', None))
                    self.indent += 1
                    ctor_body = self._transform_body(stmt.body)
                    self.indent -= 1
                    param_strs = [p[0] + (f": {p[1]}" if p[1] else "") for p in params]
                    members.append(f"{self.indent_str()}def __init__({', '.join(param_strs)}):\n{ctor_body}")
                elif isinstance(stmt, FuncDef):
                    # Make a copy of params to avoid mutating the AST
                    original_params = stmt.params[:]
                    if not stmt.params or stmt.params[0][0] != 'self':
                        stmt.params.insert(0, ('self', None))
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
            if not params or params[0][0] != 'self':
                params.insert(0, ('self', None))
            self.indent += 1
            body = self._transform_body(node.body)
            self.indent -= 1
            param_strs = [p[0] + (f": {p[1]}" if p[1] else "") for p in params]
            return f"{self.indent_str()}def __init__({', '.join(param_strs)}):\n{body}"

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
            type_str = f": {node.type_hint}" if getattr(node, 'type_hint', None) else ""
            return f"{self.indent_str()}{node.target}{type_str} = {value}"

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
            
        elif isinstance(node, Pipeline):
            left_val = self.transform(node.left)
            if isinstance(node.right, Call):
                func = self.transform(node.right.func)
                args = [self.transform(a) for a in node.right.args]
                args.insert(0, left_val)
                return f"{func}({', '.join(args)})"
            else:
                func = self.transform(node.right)
                return f"{func}({left_val})"

        else:
            raise TypeError(f"Unknown AST node: {type(node)}")

    def _transform_body(self, stmts):
        """Transform a list of body statements, each already indented by current level."""
        if not stmts:
            return f"{self.indent_str()}pass"
        return "\n".join(self.transform(stmt) for stmt in stmts)
