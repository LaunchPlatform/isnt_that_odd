"""isnt_that_odd - A library to determine if numbers are even using LLM APIs."""
from .cli import main as cli_main
from .core import EvenChecker
from .core import is_even

__version__ = "0.1.0"
__all__ = ["is_even", "EvenChecker", "cli_main"]
