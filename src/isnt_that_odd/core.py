"""Core functionality for determining if numbers are even using LLM APIs."""

from typing import Optional
from typing import Union

from litellm import completion
from pydantic import BaseModel
from pydantic import Field


class EvenResponse(BaseModel):
    """Structured response from LLM for even/odd determination."""

    is_even: bool = Field(description="True if the number is even, False if odd")


class EvenChecker:
    """A class to check if numbers are even using LLM APIs."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",  # Default model, can be any LiteLLM supported model
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """Initialize the EvenChecker.

        Args:
            model: The LLM model to use (default: gpt-3.5-turbo)
            api_key: API key for the LLM service
            base_url: Base URL for the LLM service (for open-source models)
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def _create_prompt(self, number: Union[int, float, str]) -> str:
        """Create a prompt for the LLM to determine if a number is even.

        Args:
            number: The number to check

        Returns:
            A formatted prompt string
        """
        import os
        from pathlib import Path

        # Get the directory where this module is located
        current_dir = Path(__file__).parent
        prompt_file = current_dir / "prompts" / "even_odd.txt"

        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt_template = f.read()
            return prompt_template.format(number=number)
        except FileNotFoundError:
            # Fallback to hardcoded prompt if file not found
            return f"""You are a mathematical assistant. Your task is to determine if the given number is even or odd.

Number: {number}

Instructions:
1. A number is even if it is divisible by 2 with no remainder
2. A number is odd if it is not divisible by 2
3. For decimal numbers, only the integer part matters
4. For negative numbers, the same rules apply
5. Zero (0) is considered even

Please respond with ONLY a JSON object containing a boolean field "is_even":
- Set "is_even" to true if the number is even
- Set "is_even" to false if the number is odd

Example response format:
{{"is_even": true}}

Your response:"""

    def check(self, number: Union[int, float, str]) -> bool:
        """Check if a number is even using the LLM.

        Args:
            number: The number to check (can be int, float, or string)

        Returns:
            True if the number is even, False if odd

        Raises:
            Exception: If the LLM response cannot be parsed or is invalid
        """
        prompt = self._create_prompt(number)

        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0,  # Deterministic output
                max_tokens=50,
                api_key=self.api_key,
                base_url=self.base_url,
            )
        except Exception as e:
            raise Exception(f"Error calling LLM API: {str(e)}") from e

        # Extract the content from the response
        content = response.choices[0].message.content

        # Parse the JSON response
        try:
            result = EvenResponse.model_validate_json(content)
            return result.is_even
        except Exception as e:
            # Fallback: try to extract boolean from text if JSON parsing fails
            content_lower = content.lower().strip()
            if ("true" in content_lower and "false" in content_lower) or (
                "odd" in content_lower and "even" in content_lower
            ):
                raise ValueError(
                    "Ambiguous response with both true and false, content: " + content
                ) from e
            if "true" in content_lower or "even" in content_lower:
                return True
            elif "false" in content_lower or "odd" in content_lower:
                return False
            else:
                raise ValueError(f"Could not parse LLM response: {content}") from e


def is_even(
    number: Union[int, float, str],
    model: str = "gpt-3.5-turbo",  # Default model, can be any LiteLLM supported model
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> bool:
    """Convenience function to check if a number is even.

    Args:
        number: The number to check
        model: The LLM model to use
        api_key: API key for the LLM service
        base_url: Base URL for the LLM service

    Returns:
        True if the number is even, False if odd
    """
    checker = EvenChecker(model=model, api_key=api_key, base_url=base_url)
    return checker.check(number)
