"""Tests for the CLI functionality."""
from unittest.mock import patch

from click.testing import CliRunner
from isnt_that_odd.cli import main
from isnt_that_odd.cli import parse_number


class TestParseNumber:
    """Test the parse_number function."""

    def test_parse_integer(self):
        """Test parsing integer strings."""
        assert parse_number("42") == 42
        assert parse_number("-17") == -17
        assert parse_number("0") == 0

    def test_parse_float(self):
        """Test parsing float strings."""
        assert parse_number("3.14") == 3.14
        assert parse_number("-2.5") == -2.5
        assert parse_number("10.0") == 10

    def test_parse_string(self):
        """Test parsing non-numeric strings."""
        assert parse_number("hello") == "hello"
        assert parse_number("42abc") == "42abc"
        assert parse_number("") == ""


class TestCLI:
    """Test the CLI main function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("isnt_that_odd.cli.is_even")
    def test_main_success_even(self, mock_is_even):
        """Test successful CLI execution for even number."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["42"])

        assert result.exit_code == 0
        assert "✅ 42 is EVEN" in result.output
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_main_success_odd(self, mock_is_even):
        """Test successful CLI execution for odd number."""
        mock_is_even.return_value = False

        result = self.runner.invoke(main, ["43"])

        assert result.exit_code == 0
        assert "❌ 43 is ODD" in result.output
        mock_is_even.assert_called_once()

    @patch("isnt_that_odd.cli.is_even")
    def test_main_with_custom_model(self, mock_is_even):
        """Test CLI with custom model."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["--model", "gpt-4", "42"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-4", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_main_with_api_key(self, mock_is_even):
        """Test CLI with custom API key."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["--api-key", "test-key", "42"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-3.5-turbo", api_key="test-key", base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_main_with_base_url(self, mock_is_even):
        """Test CLI with custom base URL."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["--base-url", "http://localhost:8000", "42"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42,
            model="gpt-3.5-turbo",
            api_key=None,
            base_url="http://localhost:8000",
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_main_with_verbose(self, mock_is_even):
        """Test CLI with verbose flag."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["--verbose", "42"])

        assert result.exit_code == 0
        assert "🔍 Checking if 42 is even..." in result.output
        assert "🤖 Using model: gpt-3.5-turbo" in result.output
        mock_is_even.assert_called_once()

    @patch("isnt_that_odd.cli.is_even")
    def test_main_error_handling(self, mock_is_even):
        """Test CLI error handling."""
        mock_is_even.side_effect = Exception("API Error")

        result = self.runner.invoke(main, ["42"])

        assert result.exit_code == 1
        assert "❌ Error: API Error" in result.output

    @patch("isnt_that_odd.cli.is_even")
    def test_main_float_number(self, mock_is_even):
        """Test CLI with float number."""
        mock_is_even.return_value = True

        result = self.runner.invoke(main, ["10.5"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=10.5, model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_main_string_number(self, mock_is_even):
        """Test CLI with string number."""
        mock_is_even.return_value = False

        result = self.runner.invoke(main, ['"17"'])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number='"17"', model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    def test_main_help(self):
        """Test CLI help output."""
        result = self.runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Check if numbers are even using LLM APIs" in result.output
        assert "--model" in result.output
        assert "--api-key" in result.output

    def test_main_version(self):
        """Test CLI version output."""
        result = self.runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "isnt-that-odd, version 0.1.0" in result.output
