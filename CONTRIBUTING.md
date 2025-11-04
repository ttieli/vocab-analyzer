# Contributing to Vocab Analyzer

Thank you for your interest in contributing to vocab-analyzer! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Please be respectful and constructive in all interactions. We want to maintain a welcoming and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of NLP concepts (helpful but not required)

### Areas for Contribution

We welcome contributions in several areas:

1. **Code Improvements**
   - Bug fixes
   - Performance optimizations
   - New features
   - Refactoring

2. **Documentation**
   - User guide improvements
   - API documentation
   - Examples and tutorials
   - Translations

3. **Testing**
   - Unit tests
   - Integration tests
   - Performance benchmarks

4. **Data**
   - Phrasal verb additions
   - CEFR level corrections
   - Sample texts

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/vocab-analyzer.git
cd vocab-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install package in development mode
pip install -e ".[dev]"

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

### 5. Verify Setup

```bash
# Run tests
pytest

# Check code quality
black --check src/
isort --check src/
flake8 src/
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions/fixes
- `refactor/` - Code refactoring

### 2. Make Changes

- Write clean, readable code
- Follow existing patterns
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_word.py

# Run with coverage
pytest --cov=vocab_analyzer

# Test CLI manually
vocab-analyzer analyze tests/fixtures/sample_text.txt
```

### 4. Format Code

```bash
# Auto-format with black
black src/ tests/

# Sort imports
isort src/ tests/

# Check style
flake8 src/ tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add phrasal verb detection"
```

See [Commit Guidelines](#commit-guidelines) below.

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (enforced by Black)
- **Imports**: Sorted with isort
- **Type hints**: Required for public APIs
- **Docstrings**: Google style for all public functions/classes

### Code Organization

```python
"""
Module docstring describing purpose.
"""
# Standard library imports
import json
from pathlib import Path
from typing import List, Optional

# Third-party imports
import pandas as pd
import spacy

# Local imports
from ..models import Word
from ..utils import clean_text


class MyClass:
    """
    Class docstring.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """
    
    def public_method(self, arg: str) -> Optional[str]:
        """
        Method docstring.
        
        Args:
            arg: Description
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something goes wrong
        """
        pass
    
    def _private_method(self):
        """Private methods use single underscore."""
        pass
```

### Type Hints

Always use type hints for function signatures:

```python
from typing import Dict, List, Optional, Union

def analyze_text(
    text: str,
    min_level: Optional[str] = None,
    max_level: Optional[str] = None
) -> Dict[str, List[Word]]:
    """Type hints make code self-documenting."""
    pass
```

### Error Handling

```python
# Good: Specific exceptions
try:
    result = process_file(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    return None

# Bad: Catching everything
try:
    result = process_file(path)
except Exception:
    pass  # Don't do this!
```

## Testing Guidelines

### Writing Tests

```python
import pytest
from vocab_analyzer.models import Word


class TestWord:
    """Test Word dataclass."""
    
    def test_creation(self):
        """Test word creation with valid data."""
        word = Word(word="test", level="B1", word_type="noun")
        assert word.word == "test"
        assert word.level == "B1"
    
    def test_invalid_level(self):
        """Test validation of invalid CEFR level."""
        with pytest.raises(ValueError, match="Invalid CEFR level"):
            Word(word="test", level="X1", word_type="noun")
    
    @pytest.mark.parametrize("level", ["A1", "A2", "B1", "B2", "C1", "C2"])
    def test_all_levels(self, level):
        """Test all valid CEFR levels."""
        word = Word(word="test", level=level, word_type="noun")
        assert word.level == level
```

### Test Organization

```
tests/
├── unit/           # Unit tests (fast, isolated)
│   ├── test_word.py
│   ├── test_phrase.py
│   └── test_analysis.py
├── integration/    # Integration tests (slower, full pipeline)
│   ├── test_analyzer.py
│   └── test_cli.py
└── fixtures/       # Test data
    ├── sample_text.txt
    └── expected_output.json
```

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/unit/test_word.py

# Specific test
pytest tests/unit/test_word.py::TestWord::test_creation

# With coverage
pytest --cov=vocab_analyzer --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
git commit -m "feat(analyzer): add phrasal verb detection"

# Bug fix
git commit -m "fix(exporter): handle empty analysis results"

# Documentation
git commit -m "docs(readme): add installation instructions"

# Multiple lines
git commit -m "feat(cli): add --quiet option

Add quiet mode to suppress progress output.
Useful for scripting and automation.

Closes #123"
```

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run all checks**
   ```bash
   pytest
   black --check src/
   isort --check src/
   flake8 src/
   mypy src/
   ```

3. **Update documentation**
   - README.md if adding features
   - Docstrings for new code
   - CHANGELOG.md (if exists)

### Submitting PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Use descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots if UI changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

- At least one approval required
- All CI checks must pass
- Address reviewer feedback
- Keep PR scope focused

## Additional Resources

### Project Documentation

- [User Guide](docs/USER_GUIDE.md)
- [Examples](docs/EXAMPLES.md)
- [Quick Reference](docs/QUICK_REFERENCE.md)
- [API Documentation](docs/API.md) (if available)

### External Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [spaCy Documentation](https://spacy.io/)

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues/PRs first

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

---

Thank you for contributing to vocab-analyzer! 🎉
