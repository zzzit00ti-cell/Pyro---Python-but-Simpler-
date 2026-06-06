# Contributing to Pyro

Thank you for your interest in Pyro! We welcome contributions of all kinds: bug reports, feature requests, documentation improvements, and code changes.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork:

```

   git clone https://github.com/your-username/pyro.git
   cd pyro
   
```

3. Create a virtual environment:
    
```

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
```


4. Install the package in editable mode with test dependencies:

```
    pip install -e .
    pip install pytest pytest-cov
```

5. Running Tests

```

pytest tests/ -v --cov=pyro

```

## Code Style

    Follow PEP 8 for Python code.

    Use meaningful variable names.

    Add docstrings to public functions and classes.

    Keep the compiler modular: lexer → parser → transformer.

## How to Add a New Feature

    1. Lexer: Add new token types in pyro/lexer.py (update KEYWORDS, TOKEN_REGEX if needed).

    2. Parser: Add new grammar rules in pyro/parser.py and new AST node classes in pyro/ast_nodes.py.

    3. Transformer: Implement code generation for the new AST node in pyro/transformer.py.

    4. Tests: Write tests in tests/ for the new feature.

## Submitting a Pull Request

    1. Create a new branch from main:
    
```

    git checkout -b feature/your-feature-name
    
```

    2. Make your changes, add tests, and ensure all tests pass.

    3. Commit with a clear message:
    
```

    git commit -m "Add support for ..."
    
```

    4. Push to your fork and open a Pull Request against main.

## Reporting Issues

Use the GitHub issue tracker. Please include:

    A minimal example of Pyro code that reproduces the issue.

    Expected behavior vs. actual behavior.

    Pyro version (pyro --version).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
