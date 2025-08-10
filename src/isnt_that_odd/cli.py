"""Command-line interface for the isn't that odd library."""
import argparse
import sys
from typing import List
from typing import Optional
from typing import Union

from .core import is_even


def parse_number(value: str) -> Union[int, float, str]:
    """Parse a string input to determine if it's a number or should remain a string."""
    try:
        # Try to convert to float first
        float_val = float(value)
        # If it's a whole number, convert to int
        if float_val.is_integer():
            return int(float_val)
        return float_val
    except ValueError:
        # If it's not a number, return as string
        return value


def main(args: Optional[List[str]] = None) -> int:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Check if numbers are even using LLM APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 42                    # Check if 42 is even
  %(prog)s 43                    # Check if 43 is odd
  %(prog)s 0                     # Check if 0 is even
  %(prog)s -4                    # Check if -4 is even
  %(prog)s 10.5                  # Check if 10.5 is even (integer part)
  %(prog)s "17"                  # Check if string "17" is even
  %(prog)s --model gpt-4 42      # Use specific model
  %(prog)s --api-key KEY 42      # Use custom API key
        """,
    )

    parser.add_argument(
        "number", help="The number to check (can be integer, float, or string)"
    )

    parser.add_argument(
        "--model",
        "-m",
        default="gpt-3.5-turbo",
        help="LLM model to use (default: gpt-3.5-turbo)",
    )

    parser.add_argument("--api-key", "-k", help="API key for the LLM service")

    parser.add_argument(
        "--base-url", "-u", help="Base URL for the LLM service (for open-source models)"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    parsed_args = parser.parse_args(args)

    try:
        # Parse the input number
        number = parse_number(parsed_args.number)

        if parsed_args.verbose:
            print(f"🔍 Checking if {number} is even...")
            print(f"🤖 Using model: {parsed_args.model}")

        # Check if the number is even
        result = is_even(
            number=number,
            model=parsed_args.model,
            api_key=parsed_args.api_key,
            base_url=parsed_args.base_url,
        )

        # Display result
        if result:
            print(f"✅ {number} is EVEN")
        else:
            print(f"❌ {number} is ODD")

        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
