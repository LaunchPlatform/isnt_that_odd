#!/usr/bin/env python3
"""Basic usage example for the isn't that odd library."""
import os

from isnt_that_odd import EvenChecker
from isnt_that_odd import is_even


def main():
    """Demonstrate basic usage of the library."""
    print("🤖 isn't that odd - LLM-Powered Even/Odd Detection")
    print("=" * 50)

    # Check if you have an API key set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OPENAI_API_KEY found in environment variables.")
        print("   Set OPENAI_API_KEY to test with real LLM API calls.")
        print("   For demonstration, we'll show the structure without API calls.\n")

    # Test numbers
    test_numbers = [2, 3, 0, -4, -7, 10.5, 15.8, 100, 999, "42", "17"]

    print("Testing numbers for even/odd detection:")
    print("-" * 40)

    for number in test_numbers:
        if api_key:
            try:
                result = is_even(number)
                status = "✅ EVEN" if result else "❌ ODD"
                print(f"{number:>6} → {status}")
            except Exception as e:
                print(f"{number:>6} → ❌ ERROR: {e}")
        else:
            # Show expected results without API calls
            expected = (
                number == 0
                or (isinstance(number, (int, float)) and int(number) % 2 == 0)
                or (isinstance(number, str) and int(number) % 2 == 0)
            )
            status = "✅ EVEN" if expected else "❌ ODD"
            print(f"{number:>6} → {status} (expected)")

    print("\n" + "=" * 50)

    if api_key:
        print("🚀 Using real LLM API calls!")
        print("Try different models:")

        # Example with different models
        models = ["gpt-3.5-turbo", "gpt-4"]
        for model in models:
            try:
                checker = EvenChecker(model=model)
                result = checker.check(42)
                print(f"   {model}: 42 is {'even' if result else 'odd'}")
            except Exception as e:
                print(f"   {model}: Error - {e}")
    else:
        print("🔑 Set OPENAI_API_KEY to test with real LLM API calls!")
        print("   export OPENAI_API_KEY='your-api-key-here'")

    print("\n📚 For more examples, check the README.md file!")


if __name__ == "__main__":
    main()
