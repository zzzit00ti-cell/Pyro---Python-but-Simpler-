import subprocess
import tempfile
from pathlib import Path
from pyro.compiler import compile_pyro

def test_hello_world():
    source = 'print "Hello"'
    py_code = compile_pyro(source)
    # Execute the generated Python code
    exec_globals = {}
    exec(py_code, exec_globals)  # no output captured, but runs without error
    # We can also capture stdout, but for simplicity just test no crash
    assert True

def test_fibonacci():
    source = """
func fib(n)
    if n <= 1
        return n
    else
        return fib(n-1) + fib(n-2)
    end
end
print fib(5)
"""
    py_code = compile_pyro(source)
    import io
    import sys
    captured = io.StringIO()
    sys.stdout = captured
    exec(py_code)
    sys.stdout = sys.__stdout__
    assert captured.getvalue().strip() == "5"

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
    import io
    import sys
    captured = io.StringIO()
    sys.stdout = captured
    exec(py_code)
    sys.stdout = sys.__stdout__
    assert "Rex says woof" in captured.getvalue()
