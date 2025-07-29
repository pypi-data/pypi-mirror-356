# Auto Commenter

Auto Commenter is a Python package that automatically generates docstrings for your Python functions and classes based on their arguments and return types. It uses **abstract syntax tree (AST)** analysis to inspect the code and generate informative comments.

## Features

- Automatically generates docstrings for functions and classes.
- Infers argument types based on common patterns (e.g., `num`, `data`, `arr`).
- Supports return type detection, including for `int`, `str`, `list`, `dict`, `pd.DataFrame`, and `np.ndarray`.
- Easily integrate into your workflow to improve code documentation.

## Installation

You can install Auto Commenter from **PyPI** using pip:

```bash
pip install auto-commenter
