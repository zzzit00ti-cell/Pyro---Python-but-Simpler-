import sys
from .compiler import compile_pyro, compile_file
from .cli import main

if sys.version_info < (3, 10):
    raise ImportError("Pyro requires Python 3.10 or higher")
__version__ = "0.1.3"
__all__ = ["compile_pyro", "compile_file", "main"]
