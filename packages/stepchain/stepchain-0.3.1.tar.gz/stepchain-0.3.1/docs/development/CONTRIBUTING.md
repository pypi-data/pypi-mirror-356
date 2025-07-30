# Contributing to StepChain

Thank you for your interest in contributing to StepChain! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Add the upstream repository as a remote
4. Create a new branch for your feature or bugfix

```bash
git clone https://github.com/YOUR_USERNAME/taskcrew-segmenter.git
cd taskcrew-segmenter
git remote add upstream https://github.com/closedloop-technologies/taskcrew-segmenter.git
git checkout -b feature/your-feature-name
```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- pip and virtualenv
- OpenAI API key for testing

### Setting Up the Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=taskcrew_segmenter

# Run specific test file
pytest tests/test_decomposer.py

# Run with verbose output
pytest -v
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-retry-logic`
- `bugfix/fix-dependency-validation`
- `docs/update-api-reference`
- `refactor/improve-error-handling`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `perf`: Performance improvements
- `style`: Code style changes
- `build`: Build system changes
- `ci`: CI configuration changes

Examples:
```
feat(decomposer): add support for custom strategies
fix(executor): handle rate limit errors gracefully
docs(api): update executor documentation
test(storage): add tests for JSONLStore
```

### Pull Request Process

1. Update your branch with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Ensure all tests pass and code is properly formatted:
   ```bash
   pytest
   black .
   ruff check .
   mypy .
   ```

3. Update documentation if needed

4. Push your branch and create a pull request

5. Fill out the pull request template completely

6. Wait for code review and address feedback

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the source code structure
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies

Example test:
```python
def test_decomposer_validates_empty_task():
    """Test that decomposer rejects empty task descriptions."""
    decomposer = TaskDecomposer()
    
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        decomposer.decompose("")
```

### Test Coverage

We aim for at least 80% test coverage. Check coverage with:
```bash
pytest --cov=taskcrew_segmenter --cov-report=html
open htmlcov/index.html
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with these additions:
- Maximum line length: 100 characters
- Use type hints for all public functions
- Document all public APIs with docstrings

### Type Hints

Use type hints for better code clarity:
```python
from typing import Optional, List, Dict, Any

def decompose_task(
    task: str,
    tools: Optional[List[str]] = None,
    context: Optional[Dict[str, Any]] = None
) -> Plan:
    """Decompose a task into steps."""
    ...
```

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Handle edge cases gracefully

### Code Organization

- Keep modules focused and cohesive
- Limit module size to ~500 lines
- Use clear, descriptive names
- Group related functionality

## Documentation

### Docstrings

Use Google-style docstrings:
```python
def execute_step(self, step: Step, run_id: str) -> StepResult:
    """Execute a single step with retry logic.
    
    Args:
        step: The step to execute
        run_id: Unique identifier for this run
        
    Returns:
        StepResult with execution details
        
    Raises:
        ExecutionError: If execution fails after retries
    """
```

### API Documentation

- Update API docs when changing public interfaces
- Include code examples
- Document all parameters and return values
- Explain common use cases

### README Updates

Update the README when:
- Adding new features
- Changing installation requirements
- Modifying CLI commands
- Updating examples

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a release PR
4. After merge, tag the release
5. Build and publish to PyPI

## Getting Help

- Open an issue for bugs or feature requests
- Join discussions in GitHub Discussions
- Check existing issues before creating new ones
- Provide minimal reproducible examples for bugs

## Recognition

Contributors will be recognized in:
- The CONTRIBUTORS file
- Release notes
- Project documentation

Thank you for contributing to StepChain!