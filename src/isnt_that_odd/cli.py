"""Command-line interface for the isn't that odd library."""
import sys
from typing import Union

import click

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


@click.command(
    name="isnt-that-odd",
    help="Check if numbers are even using LLM APIs",
    epilog="""
Examples:
  %(prog)s 42                    # Check if 42 is even
  %(prog)s 43                    # Check if 43 is odd
  %(prog)s 0                     # Check if 0 is even
  %(prog)s -4                    # Check if -4 is even
  %(prog)s 10.5                  # Check if 10.5 is even (integer part)
  %(prog)s "17"                  # Check if string "17" is even
  %(prog)s --model claude-3 42   # Use specific model
  %(prog)s --api-key KEY 42      # Use custom API key
    """,
)
@click.argument("number")
@click.option(
    "--model",
    "-m",
    default="gpt-3.5-turbo",
    help="LLM model to use (default: gpt-3.5-turbo, supports any LiteLLM model)",
    show_default=True,
)
@click.option(
    "--api-key",
    "-k",
    help="API key for the LLM service (can also be set via LITELLM_API_KEY env var)",
    envvar="LITELLM_API_KEY",
)
@click.option(
    "--base-url",
    "-u",
    help="Base URL for the LLM service (for open-source models, can also be set via LITELLM_API_BASE env var)",
    envvar="LITELLM_API_BASE",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
@click.version_option(version="0.1.0", prog_name="isnt-that-odd")
def main(
    number: str,
    model: str,
    api_key: str,
    base_url: str,
    verbose: bool,
) -> None:
    """Check if a number is even using LLM APIs."""
    try:
        # Parse the input number
        parsed_number = parse_number(number)

        if verbose:
            click.echo(f"🔍 Checking if {parsed_number} is even...")
            click.echo(f"🤖 Using model: {model}")

        # Check if the number is even
        result = is_even(
            number=parsed_number,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )

        # Display result
        if result:
            click.echo(f"✅ {parsed_number} is EVEN")
        else:
            click.echo(f"❌ {parsed_number} is ODD")

    except KeyboardInterrupt:
        click.echo("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
