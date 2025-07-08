# Contributing to Freepik AI Orchestrator

Thank you for your interest in contributing to the Freepik AI Orchestrator! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16+ (for frontend development)
- Docker (optional, for containerized development)
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/freepik-ai-orchestrator.git
cd freepik-ai-orchestrator
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/freepik/freepik-ai-orchestrator.git
```

## Development Setup

### Local Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the development server:

```bash
streamlit run app.py
```

### Docker Development

1. Build the development container:

```bash
docker-compose -f docker-compose.dev.yml build
```

2. Start the development environment:

```bash
docker-compose -f docker-compose.dev.yml up
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues and improve stability
- **Features**: Add new functionality or enhance existing features
- **Documentation**: Improve docs, tutorials, and examples
- **Tests**: Add or improve test coverage
- **Performance**: Optimize code and improve efficiency
- **Refactoring**: Clean up code structure and organization

### Before You Start

1. Check existing issues and pull requests
2. Create an issue to discuss major changes
3. Ensure your idea aligns with project goals
4. Follow the development workflow

## Pull Request Process

### 1. Create a Branch

Create a feature branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test improvements
- `refactor/description` - Code refactoring

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Commit Guidelines

Write clear, descriptive commit messages:

```bash
git commit -m "feat: add support for new AI model integration

- Add MidJourney API integration
- Update model selection interface
- Add comprehensive error handling
- Include unit tests for new functionality"
```

**Commit Message Format:**

```
type(scope): brief description

Detailed explanation of changes (optional)

- Key change 1
- Key change 2
- Key change 3
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### 4. Test Your Changes

Run the full test suite:

```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Code quality checks
flake8 .
black --check .
mypy .

# Frontend tests (if applicable)
npm test
```

### 5. Update Documentation

- Update relevant documentation
- Add docstrings for new functions/classes
- Update API documentation if needed
- Add examples for new features

### 6. Submit Pull Request

1. Push your branch:

```bash
git push origin feature/your-feature-name
```

2. Create a pull request on GitHub
3. Fill out the PR template completely
4. Link any related issues
5. Request review from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] New tests added

## Documentation
- [ ] Code comments updated
- [ ] API documentation updated
- [ ] User documentation updated
- [ ] Changelog updated

## Related Issues
Closes #123
Related to #456
```

## Issue Reporting

### Bug Reports

Include the following information:

- **Environment**: OS, Python version, dependencies
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

### Feature Requests

Include the following information:

- **Problem**: What problem does this solve?
- **Proposed solution**: Detailed description
- **Alternatives**: Other solutions considered
- **Use cases**: How would this be used?
- **Priority**: How important is this feature?

## Development Workflow

### Setting Up Development Environment

1. **Install pre-commit hooks:**

```bash
pip install pre-commit
pre-commit install
```

2. **Configure IDE settings:**
   - Enable auto-formatting with Black
   - Set up linting with flake8
   - Configure type checking with mypy

### Code Review Process

1. **Self-review**: Review your own code first
2. **Automated checks**: Ensure CI passes
3. **Peer review**: Address reviewer feedback
4. **Maintainer review**: Final review by maintainers
5. **Merge**: Approved PRs are merged

## Code Standards

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Formatting**: Use Black for consistent formatting
- **Imports**: Use isort for import organization
- **Type hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings

### Example Code Style

```python
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """Main orchestrator for AI model management.
    
    This class handles coordination between different AI models
    and provides a unified interface for content generation.
    
    Args:
        config: Configuration dictionary
        debug: Enable debug logging
        
    Attributes:
        models: Available AI models
        analytics: Analytics tracker
    """
    
    def __init__(
        self, 
        config: Dict[str, str], 
        debug: bool = False
    ) -> None:
        self.config = config
        self.debug = debug
        self.models: List[str] = []
        
    def generate_content(
        self, 
        prompt: str, 
        model: str,
        **kwargs
    ) -> Optional[Dict[str, Union[str, float]]]:
        """Generate content using specified AI model.
        
        Args:
            prompt: Text prompt for generation
            model: AI model to use
            **kwargs: Additional model-specific parameters
            
        Returns:
            Generated content metadata or None if failed
            
        Raises:
            ModelNotFoundError: If model is not available
            GenerationError: If generation fails
        """
        try:
            result = self._process_generation(prompt, model, **kwargs)
            logger.info(f"Generated content using {model}")
            return result
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
```

### JavaScript/TypeScript Style

- Use TypeScript for type safety
- Follow Prettier formatting
- Use ESLint for code quality
- Prefer functional components
- Use modern ES6+ features

## Testing

### Test Structure

```
tests/
├── unit/                 # Unit tests
│   ├── test_orchestrator.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/          # Integration tests
│   ├── test_api.py
│   └── test_workflows.py
├── e2e/                 # End-to-end tests
│   └── test_app.py
└── fixtures/            # Test data
    ├── sample_responses.json
    └── test_images/
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from freepik_ai_orchestrator import AIOrchestrator


class TestAIOrchestrator:
    """Test cases for AIOrchestrator class."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for testing."""
        config = {"api_key": "test-key"}
        return AIOrchestrator(config)
    
    def test_generate_content_success(self, orchestrator):
        """Test successful content generation."""
        with patch('freepik_ai_orchestrator.models.DallE3') as mock_model:
            mock_model.generate.return_value = {"url": "test.jpg"}
            
            result = orchestrator.generate_content(
                prompt="test prompt",
                model="dall-e-3"
            )
            
            assert result is not None
            assert "url" in result
            mock_model.generate.assert_called_once()
    
    def test_generate_content_invalid_model(self, orchestrator):
        """Test generation with invalid model."""
        with pytest.raises(ModelNotFoundError):
            orchestrator.generate_content(
                prompt="test prompt",
                model="invalid-model"
            )
```

### Test Coverage

Maintain test coverage above 90%:

```bash
# Generate coverage report
python -m pytest --cov=freepik_ai_orchestrator --cov-report=html

# View coverage
open htmlcov/index.html
```

## Documentation

### Code Documentation

- **Docstrings**: All public functions and classes
- **Type hints**: All function parameters and returns
- **Comments**: Complex logic and algorithms
- **Examples**: Usage examples in docstrings

### User Documentation

- **API docs**: Keep API reference up to date
- **Tutorials**: Add examples for new features
- **Guides**: Update deployment and usage guides
- **Changelog**: Document all changes

### Building Documentation

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Release Process

### Version Management

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release tag
- [ ] Deploy to staging
- [ ] Deploy to production

## Getting Help

### Resources

- **Documentation**: [Full documentation](https://freepik-ai-orchestrator.readthedocs.io)
- **API Reference**: [API docs](../API.md)
- **Examples**: [Usage examples](../usage.md)
- **Troubleshooting**: [Common issues](../troubleshooting.md)

### Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Discord**: Real-time chat with community
- **Stack Overflow**: Tag questions with `freepik-ai-orchestrator`

### Contact

- **Maintainers**: @maintainer1, @maintainer2
- **Email**: ai-orchestrator@freepik.com
- **Security**: security@freepik.com

Thank you for contributing to Freepik AI Orchestrator! 🚀
