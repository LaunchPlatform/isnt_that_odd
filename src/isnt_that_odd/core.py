"""Core functionality for determining if numbers are even using LLM APIs."""

from typing import Optional
from typing import Union

from jinja2.sandbox import SandboxedEnvironment
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

        Raises:
            FileNotFoundError: If the prompt template file cannot be found
        """
        from pathlib import Path

        # Get the directory where this module is located
        current_dir = Path(__file__).parent
        prompt_file = current_dir / "prompts" / "even_odd.txt"

        try:
            with open(prompt_file, encoding="utf-8") as f:
                prompt_template = f.read()

            # Use sandboxed Jinja2 environment for security
            sandbox_env = SandboxedEnvironment()
            template = sandbox_env.from_string(prompt_template)
            return template.render(number=number)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Prompt template file not found at {prompt_file}. "
                "This file is required for the EvenChecker to function properly."
            ) from None

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
