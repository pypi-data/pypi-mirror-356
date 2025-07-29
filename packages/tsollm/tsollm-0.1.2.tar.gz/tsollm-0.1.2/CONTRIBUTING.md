# Contributing to TSO-LLM

Thank you for your interest in contributing to TSO-LLM! This document provides guidelines and instructions for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- Git
- OpenAI API key for testing

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/tsollm.git
   cd tsollm
   ```

2. **Install UV** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync --all-extras --dev
   ```

4. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

5. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/tsollm --cov-report=html

# Run specific test file
uv run pytest tests/test_core.py

# Run tests for specific function
uv run pytest tests/test_core.py::test_extract_note_info
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_should_extract_note_when_given_valid_text`
- Include both positive and negative test cases
- Mock external API calls using `unittest.mock`
- Aim for high test coverage (95%+)

## 🎨 Code Style

We use several tools to maintain code quality:

### Formatting
```bash
# Format code with Black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/
```

### Linting
```bash
# Check code style with flake8
uv run flake8 src/ tests/

# Type checking with mypy
uv run mypy src/
```

### Pre-commit Hooks
Pre-commit hooks automatically run these checks before each commit:
```bash
uv run pre-commit run --all-files
```

## 📋 Contributing Guidelines

### Types of Contributions

1. **Bug Reports**: Use GitHub issues with the bug template
2. **Feature Requests**: Use GitHub issues with the feature template
3. **Code Contributions**: Follow the pull request process
4. **Documentation**: Improve README, docstrings, or guides
5. **Tests**: Add or improve test coverage

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**
   ```bash
   uv run black src/ tests/
   uv run isort src/ tests/
   uv run flake8 src/ tests/
   uv run mypy src/
   uv run pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new schema for email classification"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Adding or modifying tests
- `refactor:` Code refactoring
- `chore:` Build process or auxiliary tool changes

Examples:
```
feat: add email classification schema
fix: handle empty OpenAI responses gracefully
docs: update installation instructions
test: add integration tests for bookmark extraction
```

## 🏗️ Architecture

### Project Structure
```
tsollm/
├── src/tsollm/          # Main package code
│   ├── __init__.py      # Package exports
│   ├── core.py          # Main TSO class
│   ├── schemas.py       # Pydantic schemas
│   └── exceptions.py    # Custom exceptions
├── tests/               # Test suite
├── examples/            # Usage examples
├── docs/                # Documentation
└── .github/workflows/   # CI/CD pipelines
```

### Adding New Schemas

1. **Define the schema** in `src/tsollm/schemas.py`:
   ```python
   class EmailClassification(BaseModel):
       """Schema for classifying emails."""
       subject: str = Field(description="Email subject line")
       # ... other fields
   ```

2. **Register the schema** in `src/tsollm/core.py`:
   ```python
   SUPPORTED_SCHEMAS = {
       "note": NoteClassification,
       "bookmark": BookmarkClassification,
       "email": EmailClassification,  # Add your schema
   }
   ```

3. **Add system prompt** in the `_get_system_prompt` method
4. **Export the schema** in `src/tsollm/__init__.py`
5. **Write comprehensive tests** in `tests/test_schemas.py`
6. **Update documentation** and examples

## 📖 Documentation

### Docstring Style
We use Google-style docstrings:

```python
def extract(self, text: str, schema_type: str) -> Dict[str, Any]:
    """Extract structured information from text.
    
    Args:
        text: The input text to process
        schema_type: Type of schema to use ('note' or 'bookmark')
        
    Returns:
        Dictionary containing the extracted structured data
        
    Raises:
        ExtractionError: If extraction fails
        ValueError: If schema_type is not supported
    """
```

### README Updates
When adding new features:
- Update the feature list
- Add usage examples
- Update the schema documentation
- Include any new configuration options

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment information**:
   - Python version
   - Package version
   - Operating system
5. **Code snippet** that reproduces the issue
6. **Error messages** or logs

## 💡 Feature Requests

For new features, please provide:

1. **Clear description** of the proposed feature
2. **Use case** or problem it solves
3. **Proposed API** or interface
4. **Example usage** code
5. **Alternatives considered**

## 📄 License

By contributing to TSO-LLM, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and considerate
- Focus on constructive feedback
- Help others learn and grow
- Report unacceptable behavior

## 📞 Getting Help

- **Questions**: Open a GitHub discussion
- **Bugs**: Open a GitHub issue
- **Security issues**: Email the maintainers directly

## 🎉 Recognition

Contributors will be recognized in:
- The README contributors section
- Release notes for their contributions
- Special thanks for significant contributions

Thank you for contributing to TSO-LLM! 🚀 