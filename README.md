# Pyro – A friendlier Python

Pyro is a programming language that feels like Python but removes the rough edges: no indentation errors, no `self`, no mandatory `print()` parentheses, and blocks end with `end`.

It **compiles to standard Python** – so you can use any Python library (NumPy, Django, TensorFlow) without change.

## Why Pyro?

| Feature | Python | Pyro |
|---------|--------|------|
| Blocks | Indentation sensitive | `if ... end` (no indentation errors) |
| Function definition | `def` | `func` (standard) or `fn` (Mojo-style Fast execution path!) |
| Method first argument | `self` | `this` (shorter) |
| `print` | `print("hello")` | `print "hello"` (or with parens) |
| Colons after headers | Required | Optional |
| Variable assignment | `x = 1` | `make x: int = 1` or `x = 1` (MyPy typing supported) |
| Ranges | `range(1,6)` | `1..5` (inclusive) |
| Functional Pipelines | `print(add(x, 10))` | `x |> add(10) |> print` (Coconut syntax!) |

🔥 **NEW in v1.0.0** 🔥
* **Beginner Tracebacks:** Pyret-inspired visually pinpointed (`^`) error handlers.
* **Typing out-the-box:** MyPy support for `.pyro` definitions.
* **Mojo Speeds:** `fn` explicitly caches and wraps using `numba.njit` implicitly.
* **Browser Sandbox:** Comes with an interactive HTML `examples/browser_playground.html` inspired by Brython/Skulpt.
* **MCU & Web Compilation:** Use `--target mcu` or `--target js` (RapydScript) for direct integrations.

## Example

```pyro
print "Hello from Pyro!"

make x = 10
y = 20
print "Sum: " + str(x + y)

if x > 5
    print "x is large"
else
    print "x is small"
end

func greet(name)
    print "Hello, " + name
end

greet("world")

for i in 1..5
    print i
end

class Person
    constructor(name)
        this.name = name
    end
    func say_hello()
        print "My name is " + this.name
    end
end

p = Person("Pyro")
p.say_hello()
```
## Installation
-  To install Pyro globally
```bash
pip install the-pyro-lang
```
-  To update to the latest `vx.x.x` release:
```bash
pip install --upgrade the-pyro-lang==x.x.x
```
## Usage

Compile a .pyro file to Python:

```
pyro compile input.pyro -o output.py
```

Run directly:

```
pyro run input.pyro
```

Or use as a Python module:

```
from pyro import compile_pyro
py_code = compile_pyro(source)
exec(py_code)
```

# Roadmap

## Why I created Pyro
One time I was with my friend talking, and my friend told that it was hard learning Python, but I finished learning under 2 month but he/she stopped because it was hard and I stared teaching him but for him/her it was complex and i got inspired by how he/she makes mistakes and I turned those mistakes to correct syntax that's why I created Pyro. 
## My/Our Goals in ihis Project

- To make easier to learn
  
- Make it a true language
  
- Use it for every thing that python does 

- MVP (variables, arithmetic, if/else, loops, functions, classes)

- Compile to Python source

- Import system

- Exception handling (try/catch)

- List/dict comprehensions

- Standalone bytecode compiler (direct .pyc output)

- Self‑hosting (compiler written in Pyro itself)

# Contributing

See CONTRIBUTING.md. Open issues or PRs on GitHub.

# License

MIT – use it anywhere, even in commercial projects.



---

