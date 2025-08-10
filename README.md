# isn't that odd

A Python library that determines if a given number is even or not by sending prompts to LLM APIs. Built with LiteLLM for universal LLM support and structured output for reliable responses.

## Features

- 🤖 **LLM-Powered**: Uses Large Language Models to determine if numbers are even or odd
- 🔌 **Universal Support**: Built on LiteLLM to support any LLM provider (OpenAI, Anthropic, local models, etc.)
- 📊 **Structured Output**: Forces LLM responses to be structured JSON for reliability
- 🧪 **Comprehensive Testing**: Full test suite with pytest and promptfoo integration
- 🚀 **Modern Python**: Type hints, Pydantic models, and modern Python practices
- 📦 **Easy Installation**: Simple setup with uv package manager

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
pip install uv

# Clone the repository
git clone https://github.com/yourusername/isnt_that_odd.git
cd isnt_that_odd

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from isnt_that_odd import is_even

# Check if a number is even
result = is_even(42)
print(result)  # True

result = is_even(43)
print(result)  # False
```

## Usage

### Basic Usage

```python
from isnt_that_odd import is_even, EvenChecker

# Simple function call
is_even(10)      # True
is_even(11)      # False
is_even(0)       # True
is_even(-4)      # True
is_even(-7)      # False
is_even(10.5)    # True (integer part 10 is even)
```

### Advanced Usage

```python
from isnt_that_odd import EvenChecker

# Create a custom checker
checker = EvenChecker(
    model="gpt-4",
    api_key="your-api-key-here"
)

# Check multiple numbers
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]
results = [checker.check(num) for num in numbers]
print(results)  # [True, False, True, False, True, False, True, False, True]
```

### Using Different LLM Providers

```python
from isnt_that_odd import EvenChecker

# OpenAI
checker = EvenChecker(
    model="gpt-4",
    api_key="your-openai-key"
)

# Anthropic
checker = EvenChecker(
    model="claude-3-sonnet-20240229",
    api_key="your-anthropic-key"
)

# Local models (e.g., Ollama)
checker = EvenChecker(
    model="llama2",
    base_url="http://localhost:11434/v1"
)

# Azure OpenAI
checker = EvenChecker(
    model="gpt-4",
    api_key="your-azure-key",
    base_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment"
)
```

## API Reference

### `is_even(number, model="gpt-3.5-turbo", api_key=None, base_url=None)`

Convenience function to check if a number is even.

**Parameters:**
- `number`: The number to check (int, float, or string)
- `model`: LLM model to use (default: "gpt-3.5-turbo")
- `api_key`: API key for the LLM service
- `base_url`: Base URL for the LLM service (for open-source models)

**Returns:**
- `bool`: True if the number is even, False if odd

### `EvenChecker(model="gpt-3.5-turbo", api_key=None, base_url=None)`

Main class for checking if numbers are even.

**Methods:**
- `check(number)`: Check if a number is even
- `_create_prompt(number)`: Create the prompt for the LLM

## How It Works

1. **Prompt Engineering**: The library creates a carefully crafted prompt that instructs the LLM to determine if a number is even or odd
2. **Structured Output**: Uses JSON response format to ensure the LLM returns structured data
3. **Fallback Parsing**: If JSON parsing fails, falls back to text analysis
4. **Error Handling**: Comprehensive error handling for API failures and parsing issues

### Example Prompt

```
You are a mathematical assistant. Your task is to determine if the given number is even or odd.

Number: 42

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
{"is_even": true}

Your response:
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/isnt_that_odd

# Run specific test file
pytest tests/test_core.py
```

### Prompt Testing with promptfoo

```bash
# Install promptfoo
npm install -g promptfoo

# Run prompt tests
promptfoo eval -c promptfoo.yaml
```

## Development

### Setting up Development Environment

```bash
# Install development dependencies
uv sync --group dev

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/ tests/
isort src/ tests/

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/
```

### Project Structure

```
isnt_that_odd/
├── src/
│   └── isnt_that_odd/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── promptfoo.yaml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LiteLLM](https://github.com/BerriAI/litellm) for universal LLM support
- Uses [Pydantic](https://github.com/pydantic/pydantic) for data validation
- Tested with [pytest](https://github.com/pytest-dev/pytest) and [promptfoo](https://github.com/promptfoo/promptfoo)

## Why "isn't that odd"?

The name is a playful reference to the library's purpose of determining whether numbers are even or odd. It's also a bit of a pun - when you ask if something "isn't that odd," you're questioning whether it's unusual, just like the library questions whether a number is odd!
