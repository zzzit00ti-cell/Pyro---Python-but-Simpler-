from .lexer import tokenize
from .parser import Parser, ParserError
from .transformer import PyTransformer

def compile_pyro(source, fast_mode=False):
    try:
        tokens = tokenize(source)
        parser = Parser(tokens, source_lines=source.splitlines())
        ast = parser.parse()
        transformer = PyTransformer()
        py_code = transformer.transform(ast)
        if "@__pyro_fast__" in py_code:
            if fast_mode:
                inject = "try:\n    from numba import njit as __pyro_fast__\nexcept ImportError:\n    from functools import cache as __pyro_fast__\n"
            else:
                inject = "def __pyro_fast__(f): return f\n"
            py_code = inject + py_code
        return py_code
    except ParserError as e:
        # Already has suggestions embedded
        raise e
    except Exception as e:
        # Wrap unexpected errors
        raise SyntaxError(f"Compilation error: {str(e)}") from e

def compile_file(input_path, output_path=None, fast_mode=False):
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    py_code = compile_pyro(source, fast_mode=fast_mode)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(py_code)
    return py_code
