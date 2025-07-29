"""Enables running the validator as a module.

This file allows the package to be executed directly from the command line
using `python -m code_validator`. It serves as the main entry point
that invokes the command-line interface logic.
"""

from .cli import run_from_cli

if __name__ == "__main__":
    run_from_cli()
