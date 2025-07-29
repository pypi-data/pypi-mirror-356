"""
Entry point for RunLy when executed as a module.

This file enables running RunLy with:
    python -m runly

It simply imports and calls the main CLI function.
"""

import sys

from runly.cli import main

if __name__ == "__main__":
    sys.exit(main())
