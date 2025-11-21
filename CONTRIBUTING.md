# Contributing to OmniForge

Thank you for your interest in contributing to OmniForge! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/MASSIVEMAGNETICS/build_me/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear use case description
   - Expected functionality
   - Potential implementation approach
   - Examples if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass (`pytest`)
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/build_me.git
cd build_me

# Install dependencies
./scripts/install.sh

# Activate virtual environment
source venv/bin/activate

# Run tests
pytest

# Run linter
pylint src/
```

### Coding Standards

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write comprehensive docstrings
- Add comments for complex logic
- Keep functions focused and small
- Write unit tests for new features

### Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage (>80%)
- Test edge cases and error conditions

### Documentation

- Update README.md if needed
- Add docstrings to all functions/classes
- Include examples for new features
- Update API documentation

## Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Questions?

Open a [Discussion](https://github.com/MASSIVEMAGNETICS/build_me/discussions) or reach out to maintainers.

Thank you for contributing! 🚀
