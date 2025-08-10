#!/usr/bin/env python3
"""Example of using the benchmark functionality programmatically."""
from isnt_that_odd.cli import generate_random_numbers
from isnt_that_odd.cli import run_benchmark


def main():
    """Run a simple benchmark example."""
    print("🧪 Running benchmark example...")

    # Generate some test numbers
    test_numbers = generate_random_numbers(5, -100, 100)
    print(f"Generated numbers: {test_numbers}")

    # Note: This would require actual API credentials to run
    # For demonstration purposes, we'll just show the structure
    print("\nTo run actual benchmark:")
    print("isnt-that-odd benchmark --count 20 --verbose")
    print("isnt-that-odd benchmark --count 50 --min -5000 --max 5000")


if __name__ == "__main__":
    main()
