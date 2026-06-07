import io
import sys
from pyro.compiler import compile_pyro


def _capture_exec(py_code):
    """Execute Python code and capture its stdout."""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        exec(py_code, {})
    finally:
        sys.stdout = old_stdout
    return captured.getvalue()


def test_hello_world():
    source = 'print "Hello"'
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "Hello" in output


def test_variables():
    source = '''make x = 10
y = 20
print x + y'''
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "30" in output


def test_if_else():
    source = '''x = 10
if x > 5
    print "big"
else
    print "small"
end'''
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "big" in output


def test_fibonacci():
    source = """
func fib(n)
    if n <= 1
        return n
    else
        return fib(n - 1) + fib(n - 2)
    end
end
print fib(5)
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert output.strip() == "5"


def test_class():
    source = """
class Dog
    constructor(name)
        this.name = name
    end
    func bark()
        print this.name + " says woof"
    end
end
d = Dog("Rex")
d.bark()
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "Rex says woof" in output


def test_for_loop_range():
    source = """
make total = 0
for i in 1..5
    total = total + i
end
print total
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert output.strip() == "15"


def test_while_loop():
    source = """
x = 3
while x > 0
    print x
    x = x - 1
end
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    lines = output.strip().split('\n')
    assert lines == ['3', '2', '1']


def test_nested_function_calls():
    source = '''print str(42)'''
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "42" in output


def test_compile_hello_example():
    """Test compiling the hello.pyro example file."""
    with open('examples/hello.pyro', 'r') as f:
        source = f.read()
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "Hello from Pyro!" in output
    assert "My name is Pyro" in output


def test_compile_fibonacci_example():
    """Test compiling the fibonacci.pyro example file."""
    with open('examples/fibonacci.pyro', 'r') as f:
        source = f.read()
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    lines = output.strip().split('\n')
    assert "Fibonacci sequence:" in lines[0]


def test_compile_class_example():
    """Test compiling the class.pyro example file."""
    with open('examples/class.pyro', 'r') as f:
        source = f.read()
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    assert "Pyro" in output


def test_booleans_and_none():
    source = """
x = True
y = False
z = None
print x
print y
print z
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    lines = output.strip().split('\n')
    assert lines == ['True', 'False', 'None']


def test_logical_operators():
    source = """
print True and False
print True or False
print not True
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    lines = output.strip().split('\n')
    assert lines == ['False', 'True', 'False']


def test_advanced_math_operators():
    source = """
print 2 ** 3
print 10 // 3
"""
    py_code = compile_pyro(source)
    output = _capture_exec(py_code)
    lines = output.strip().split('\n')
    assert lines == ['8', '3']
