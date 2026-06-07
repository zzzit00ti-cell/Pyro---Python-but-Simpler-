from .lexer import tokenize
from .parser import Parser, ParserError
from .transformer import PyTransformer

def compile_pyro(source):
    try:
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        transformer = PyTransformer()
        py_code = transformer.transform(ast)
        return py_code
    except ParserError as e:
        # Already has suggestions embedded
        raise e
    except Exception as e:
        # Wrap unexpected errors
        raise SyntaxError(f"Compilation error: {str(e)}") from e

def compile_file(input_path, output_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()
    py_code = compile_pyro(source)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(py_code)
    return py_code
