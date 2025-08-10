"""Tests for the core functionality of isnt_that_odd."""
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.isnt_that_odd.core import EvenChecker
from src.isnt_that_odd.core import EvenResponse
from src.isnt_that_odd.core import is_even


class TestEvenResponse:
    """Test the EvenResponse Pydantic model."""

    def test_valid_response(self):
        """Test that valid responses are parsed correctly."""
        response = EvenResponse(is_even=True)
        assert response.is_even is True

        response = EvenResponse(is_even=False)
        assert response.is_even is False

    def test_model_validation(self):
        """Test that the model validates input correctly."""
        # This should work
        EvenResponse(is_even=True)

        # This should raise an error
        with pytest.raises(ValueError):
            EvenResponse(is_even="not a boolean")


class TestEvenChecker:
    """Test the EvenChecker class."""

    def test_init_defaults(self):
        """Test initialization with default values."""
        checker = EvenChecker()
        assert checker.model == "gpt-3.5-turbo"
        assert checker.api_key is None
        assert checker.base_url is None

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        checker = EvenChecker(
            model="gpt-4", api_key="test-key", base_url="https://api.example.com"
        )
        assert checker.model == "gpt-4"
        assert checker.api_key == "test-key"
        assert checker.base_url == "https://api.example.com"

    def test_create_prompt(self):
        """Test prompt creation."""
        checker = EvenChecker()
        prompt = checker._create_prompt(42)

        assert "42" in prompt
        assert "even" in prompt.lower()
        assert "odd" in prompt.lower()
        assert "json" in prompt.lower()
        assert "is_even" in prompt

    @patch("src.isnt_that_odd.core.completion")
    def test_check_even_number_success(self, mock_completion):
        """Test successful check for even number."""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": true}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(42)

        assert result is True
        mock_completion.assert_called_once()

    @patch("src.isnt_that_odd.core.completion")
    def test_check_odd_number_success(self, mock_completion):
        """Test successful check for odd number."""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": false}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(43)

        assert result is False
        mock_completion.assert_called_once()

    @patch("src.isnt_that_odd.core.completion")
    def test_check_with_fallback_parsing(self, mock_completion):
        """Test fallback parsing when JSON parsing fails."""
        # Mock the LLM response with text instead of JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "The number 42 is even"
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(42)

        assert result is True

    @patch("src.isnt_that_odd.core.completion")
    def test_check_with_odd_fallback_parsing(self, mock_completion):
        """Test fallback parsing for odd numbers."""
        # Mock the LLM response with text instead of JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "The number 43 is odd"
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(43)

        assert result is False

    @patch("src.isnt_that_odd.core.completion")
    def test_check_api_error(self, mock_completion):
        """Test handling of API errors."""
        mock_completion.side_effect = Exception("API Error")

        checker = EvenChecker()
        with pytest.raises(Exception, match="Error calling LLM API"):
            checker.check(42)

    @patch("src.isnt_that_odd.core.completion")
    def test_check_unparseable_response(self, mock_completion):
        """Test handling of unparseable responses."""
        # Mock the LLM response with gibberish
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Random text content"
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        with pytest.raises(ValueError, match="Could not parse LLM response"):
            checker.check(42)

    @patch("src.isnt_that_odd.core.completion")
    def test_check_ambiguous_response(self, mock_completion):
        """Test handling of ambiguous responses containing both true/false or even/odd."""
        # Mock the LLM response with ambiguous content
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[
            0
        ].message.content = "The number 42 is both even and odd, true and false"
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        with pytest.raises(
            ValueError, match="Ambiguous response with both true and false"
        ):
            checker.check(42)

    @patch("src.isnt_that_odd.core.completion")
    def test_check_ambiguous_response_odd_even(self, mock_completion):
        """Test handling of ambiguous responses containing both odd and even indicators."""
        # Mock the LLM response with ambiguous content
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This number is odd but also even"
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        with pytest.raises(
            ValueError, match="Ambiguous response with both true and false"
        ):
            checker.check(42)

    @patch("src.isnt_that_odd.core.completion")
    def test_check_calls_completion_correctly(self, mock_completion):
        """Test that completion is called with correct parameters."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": true}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        checker.check(42)

        # Verify completion was called with correct parameters
        mock_completion.assert_called_once()
        call_args = mock_completion.call_args

        assert call_args[1]["model"] == "gpt-3.5-turbo"
        assert call_args[1]["temperature"] == 0.0
        assert call_args[1]["max_tokens"] == 50
        assert call_args[1]["response_format"] == {"type": "json_object"}

        # Check the prompt content
        messages = call_args[1]["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert "42" in messages[0]["content"]


class TestIsEvenFunction:
    """Test the convenience is_even function."""

    @patch("src.isnt_that_odd.core.EvenChecker")
    def test_is_even_calls_checker(self, mock_checker_class):
        """Test that is_even function creates checker and calls check method."""
        mock_checker = Mock()
        mock_checker.check.return_value = True
        mock_checker_class.return_value = mock_checker

        result = is_even(42, model="gpt-4", api_key="test-key")

        # Verify EvenChecker was created with correct parameters
        mock_checker_class.assert_called_once_with(
            model="gpt-4", api_key="test-key", base_url=None
        )

        # Verify check method was called
        mock_checker.check.assert_called_once_with(42)

        # Verify result
        assert result is True


class TestEdgeCases:
    """Test edge cases and special numbers."""

    @patch("src.isnt_that_odd.core.completion")
    def test_zero_is_even(self, mock_completion):
        """Test that zero is correctly identified as even."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": true}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(0)

        assert result is True

    @patch("src.isnt_that_odd.core.completion")
    def test_negative_numbers(self, mock_completion):
        """Test negative numbers."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": false}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(-3)

        assert result is False

    @patch("src.isnt_that_odd.core.completion")
    def test_decimal_numbers(self, mock_completion):
        """Test decimal numbers."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": true}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check(4.7)

        assert result is True

    @patch("src.isnt_that_odd.core.completion")
    def test_string_numbers(self, mock_completion):
        """Test string representations of numbers."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"is_even": false}'
        mock_completion.return_value = mock_response

        checker = EvenChecker()
        result = checker.check("17")

        assert result is False
