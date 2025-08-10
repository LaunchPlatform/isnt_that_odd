"""Command-line interface for the isn't that odd library."""
import random
import sys
import time
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


def generate_random_numbers(
    count: int, min_val: int = -1000, max_val: int = 1000
) -> list[int]:
    """Generate a list of random integers for benchmarking."""
    return [random.randint(min_val, max_val) for _ in range(count)]


def run_benchmark(
    count: int,
    model: str,
    api_key: str,
    base_url: str,
    verbose: bool,
    min_val: int,
    max_val: int,
) -> None:
    """Run benchmark mode with random numbers."""
    click.echo(f"🚀 Starting benchmark with {count} random numbers...")
    click.echo(f"🤖 Using model: {model}")
    click.echo(f"📊 Range: {min_val} to {max_val}")
    click.echo("-" * 50)

    # Generate random numbers
    numbers = generate_random_numbers(count, min_val, max_val)

    # Track results
    correct_count = 0
    total_time = 0
    results = []

    for i, number in enumerate(numbers, 1):
        start_time = time.time()

        try:
            if verbose:
                click.echo(f"🔍 [{i}/{count}] Checking if {number} is even...")

            # Check if the number is even
            result = is_even(
                number=number,
                model=model,
                api_key=api_key,
                base_url=base_url,
            )

            end_time = time.time()
            elapsed = end_time - start_time
            total_time += elapsed

            # Determine if the result is correct
            actual_even = number % 2 == 0
            is_correct = result == actual_even

            if is_correct:
                correct_count += 1

            results.append(
                {
                    "number": number,
                    "predicted": result,
                    "actual": actual_even,
                    "correct": is_correct,
                    "time": elapsed,
                }
            )

            if verbose:
                status = "✅" if is_correct else "❌"
                click.echo(
                    f"   {status} Predicted: {'EVEN' if result else 'ODD'}, "
                    f"Actual: {'EVEN' if actual_even else 'ODD'}, "
                    f"Time: {elapsed:.3f}s"
                )

        except Exception as e:
            if verbose:
                click.echo(f"   ❌ Error: {e}")
            results.append(
                {
                    "number": number,
                    "predicted": None,
                    "actual": number % 2 == 0,
                    "correct": False,
                    "time": 0,
                    "error": str(e),
                }
            )

    # Generate statistics report
    click.echo("\n" + "=" * 50)
    click.echo("📊 BENCHMARK RESULTS")
    click.echo("=" * 50)

    accuracy = (correct_count / count) * 100
    avg_time = total_time / count if count > 0 else 0

    click.echo(f"Total numbers tested: {count}")
    click.echo(f"Correct predictions: {correct_count}")
    click.echo(f"Accuracy: {accuracy:.2f}%")
    click.echo(f"Total time: {total_time:.3f}s")
    click.echo(f"Average time per prediction: {avg_time:.3f}s")

    # Detailed breakdown
    even_numbers = [r for r in results if r["actual"]]
    odd_numbers = [r for r in results if not r["actual"]]

    if even_numbers:
        even_correct = sum(1 for r in even_numbers if r["correct"])
        even_accuracy = (even_correct / len(even_numbers)) * 100
        click.echo(
            f"\nEven numbers: {len(even_numbers)} (Accuracy: {even_accuracy:.2f}%)"
        )

    if odd_numbers:
        odd_correct = sum(1 for r in odd_numbers if r["correct"])
        odd_accuracy = (odd_correct / len(odd_numbers)) * 100
        click.echo(f"Odd numbers: {len(odd_numbers)} (Accuracy: {odd_accuracy:.2f}%)")

    # Show some examples of incorrect predictions
    incorrect_results = [
        r for r in results if not r["correct"] and r["predicted"] is not None
    ]
    if incorrect_results and verbose:
        click.echo(f"\n❌ Examples of incorrect predictions:")
        for r in incorrect_results[:5]:  # Show first 5
            click.echo(
                f"   {r['number']}: Predicted {'EVEN' if r['predicted'] else 'ODD'}, "
                f"Actual {'EVEN' if r['actual'] else 'ODD'}"
            )


@click.group()
@click.version_option(version="0.1.0", prog_name="isnt-that-odd")
def cli():
    """Check if numbers are even using LLM APIs."""
    pass


@cli.command()
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
def check(
    number: str,
    model: str,
    api_key: str,
    base_url: str,
    verbose: bool,
) -> None:
    """Check if a single number is even using LLM APIs."""
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


@cli.command()
@click.option(
    "--count",
    "-c",
    default=10,
    help="Number of random numbers to test (default: 10)",
    show_default=True,
)
@click.option(
    "--min",
    default=-1000,
    help="Minimum value for random numbers (default: -1000)",
    show_default=True,
)
@click.option(
    "--max",
    default=1000,
    help="Maximum value for random numbers (default: 1000)",
    show_default=True,
)
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
def benchmark(
    count: int,
    min: int,
    max: int,
    model: str,
    api_key: str,
    base_url: str,
    verbose: bool,
) -> None:
    """Run benchmark mode with random numbers to test even/odd detection accuracy."""
    try:
        if count <= 0:
            click.echo("❌ Count must be a positive number", err=True)
            sys.exit(1)

        if min >= max:
            click.echo("❌ Min value must be less than max value", err=True)
            sys.exit(1)

        run_benchmark(
            count=count,
            model=model,
            api_key=api_key,
            base_url=base_url,
            verbose=verbose,
            min_val=min,
            max_val=max,
        )

    except KeyboardInterrupt:
        click.echo("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


# Backward compatibility - keep the old main function
def main(
    number: str,
    model: str = "gpt-3.5-turbo",
    api_key: str = None,
    base_url: str = None,
    verbose: bool = False,
) -> None:
    """Check if a number is even using LLM APIs (legacy function)."""
    check.callback(
        number=number,
        model=model,
        api_key=api_key,
        base_url=base_url,
        verbose=verbose,
    )


if __name__ == "__main__":
    cli()
