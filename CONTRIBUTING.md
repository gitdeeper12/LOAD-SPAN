# Contributing to LOAD-SPAN

Thank you for your interest in contributing to LOAD-SPAN!

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Install development dependencies: `make install-dev`
4. Create a branch for your changes

## Development Workflow

### Running Tests

```bash
make test
```

Code Quality

```bash
make lint    # Run linters
make format  # Format code automatically
```

Building Documentation

```bash
make docs
```

Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass locally
4. Update CHANGELOG.md with your changes
5. Submit a pull request to the main branch

Code Style

· Follow PEP 8 guidelines
· Use Black for formatting (line length: 100)
· Use isort for import sorting
· Add type hints for all functions

Commit Messages

Use conventional commit format:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style changes
· refactor: Code refactoring
· test: Test additions or corrections
· chore: Maintenance tasks

Questions?

Open an issue on GitHub or contact the maintainers.
