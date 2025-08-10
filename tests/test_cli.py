"""Tests for the CLI functionality."""

from unittest.mock import patch

from click.testing import CliRunner

from isnt_that_odd.cli import cli
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
    """Test the CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("isnt_that_odd.cli.is_even")
    def test_check_success_even(self, mock_is_even):
        """Test successful CLI execution for even number."""
        mock_is_even.return_value = True

        result = self.runner.invoke(cli, ["check", "42"])

        assert result.exit_code == 0
        assert "✅ 42 is EVEN" in result.output
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_check_success_odd(self, mock_is_even):
        """Test successful CLI execution for odd number."""
        mock_is_even.return_value = False

        result = self.runner.invoke(cli, ["check", "43"])

        assert result.exit_code == 0
        assert "❌ 43 is ODD" in result.output
        mock_is_even.assert_called_once()

    @patch("isnt_that_odd.cli.is_even")
    def test_check_with_custom_model(self, mock_is_even):
        """Test CLI with custom model."""
        mock_is_even.return_value = True

        result = self.runner.invoke(cli, ["check", "--model", "gpt-4", "42"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-4", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_check_with_api_key(self, mock_is_even):
        """Test CLI with custom API key."""
        mock_is_even.return_value = True

        result = self.runner.invoke(cli, ["check", "--api-key", "test-key", "42"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42, model="gpt-3.5-turbo", api_key="test-key", base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_check_with_base_url(self, mock_is_even):
        """Test CLI with custom base URL."""
        mock_is_even.return_value = True

        result = self.runner.invoke(
            cli, ["check", "--base-url", "http://localhost:8000", "42"]
        )

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=42,
            model="gpt-3.5-turbo",
            api_key=None,
            base_url="http://localhost:8000",
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_check_with_verbose(self, mock_is_even):
        """Test CLI with verbose flag."""
        mock_is_even.return_value = True

        result = self.runner.invoke(cli, ["check", "--verbose", "42"])

        assert result.exit_code == 0
        assert "🔍 Checking if 42 is even..." in result.output
        assert "🤖 Using model: gpt-3.5-turbo" in result.output
        mock_is_even.assert_called_once()

    @patch("isnt_that_odd.cli.is_even")
    def test_check_error_handling(self, mock_is_even):
        """Test CLI error handling."""
        mock_is_even.side_effect = Exception("API Error")

        result = self.runner.invoke(cli, ["check", "42"])

        assert result.exit_code == 1
        assert "❌ Error: API Error" in result.output

    @patch("isnt_that_odd.cli.is_even")
    def test_check_float_number(self, mock_is_even):
        """Test CLI with float number."""
        mock_is_even.return_value = True

        result = self.runner.invoke(cli, ["check", "10.5"])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number=10.5, model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    @patch("isnt_that_odd.cli.is_even")
    def test_check_string_number(self, mock_is_even):
        """Test CLI with string number."""
        mock_is_even.return_value = False

        result = self.runner.invoke(cli, ["check", '"17"'])

        assert result.exit_code == 0
        mock_is_even.assert_called_once_with(
            number='"17"', model="gpt-3.5-turbo", api_key=None, base_url=None
        )

    def test_check_help(self):
        """Test CLI help output."""
        result = self.runner.invoke(cli, ["check", "--help"])

        assert result.exit_code == 0
        assert "Check if a single number is even using LLM APIs" in result.output
        assert "--model" in result.output
        assert "--api-key" in result.output

    def test_cli_help(self):
        """Test main CLI help output."""
        result = self.runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Check if numbers are even using LLM APIs" in result.output
        assert "check" in result.output
        assert "benchmark" in result.output

    def test_cli_version(self):
        """Test CLI version output."""
        result = self.runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "isnt-that-odd, version 0.1.0" in result.output

    def test_benchmark_help(self):
        """Test benchmark command help output."""
        result = self.runner.invoke(cli, ["benchmark", "--help"])

        assert result.exit_code == 0
        assert "Run benchmark mode with random numbers" in result.output
        assert "--count" in result.output
        assert "--min" in result.output
        assert "--max" in result.output

    @patch("isnt_that_odd.cli.run_benchmark")
    def test_benchmark_command(self, mock_run_benchmark):
        """Test benchmark command execution."""
        result = self.runner.invoke(cli, ["benchmark", "--count", "5"])

        assert result.exit_code == 0
        mock_run_benchmark.assert_called_once()

    def test_benchmark_invalid_count(self):
        """Test benchmark with invalid count."""
        result = self.runner.invoke(cli, ["benchmark", "--count", "0"])

        assert result.exit_code == 1
        assert "Count must be a positive number" in result.output

    def test_benchmark_invalid_range(self):
        """Test benchmark with invalid range."""
        result = self.runner.invoke(cli, ["benchmark", "--min", "10", "--max", "5"])

        assert result.exit_code == 1
        assert "Min value must be less than max value" in result.output


class TestLegacyMain:
    """Test the legacy main function for backward compatibility."""

    @patch("isnt_that_odd.core.is_even")
    def test_legacy_main_success(self, mock_is_even):
        """Test legacy main function still works."""
        from isnt_that_odd.cli import main

        mock_is_even.return_value = True

        # Test that the main function calls is_even correctly
        main("42")
        mock_is_even.assert_called_once_with(
            number=42,
            model="gpt-3.5-turbo",
            api_key=None,
            base_url=None,
        )

    @patch("isnt_that_odd.core.is_even")
    def test_legacy_main_with_options(self, mock_is_even):
        """Test legacy main function with custom options."""
        from isnt_that_odd.cli import main

        mock_is_even.return_value = True

        main("42", model="gpt-4", api_key="test-key", verbose=True)
        mock_is_even.assert_called_once_with(
            number=42,
            model="gpt-4",
            api_key="test-key",
            base_url=None,
        )
