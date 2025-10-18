# Contributing to RFM Insight Engine

Thank you for your interest in contributing to RFM Insight Engine! 🚀

This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 🐛 Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** to see if your question is already answered
3. **Use the issue template** when creating new issues

#### Issue Types

- 🐛 **Bug Report**: Something isn't working as expected
- 💡 **Feature Request**: Suggest a new feature or enhancement
- 📚 **Documentation**: Improve or add documentation
- ❓ **Question**: Ask a question about usage

### 💻 Code Contributions

#### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/rfm-insight-engine.git
cd rfm-insight-engine

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # Coming soon
```

#### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Run linting
   flake8 src/
   
   # Run the demo to ensure everything works
   python run_analysis.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description of your changes"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### 📝 Pull Request Guidelines

#### Before Submitting

- [ ] **Code follows style guidelines** (PEP 8)
- [ ] **Tests pass** and new tests are added
- [ ] **Documentation is updated** if needed
- [ ] **README is updated** if adding new features
- [ ] **No merge conflicts** with main branch

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] Demo script runs successfully

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors
```

## 🎨 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Good example
class RFMCalculator:
    """RFM calculation and scoring module."""
    
    def __init__(self):
        self.rfm_data = None
        self.segments = None
    
    def calculate_rfm_scores(self, rfm_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate RFM scores based on quantiles.
        
        Args:
            rfm_data: DataFrame with Recency, Frequency, Monetary columns
            
        Returns:
            DataFrame with RFM scores
        """
        # Implementation here
        pass
```

### File Organization

```
src/
├── __init__.py
├── engine.py                    # Main engine
├── core/                        # Core functionality
│   ├── __init__.py
│   ├── data_processor.py
│   └── rfm_calculator.py
├── visualization/               # Plotting and charts
│   ├── __init__.py
│   └── plotter.py
└── strategy/                    # Marketing strategies
    ├── __init__.py
    └── marketing_strategies.py
```

### Documentation Standards

- **Docstrings**: Use Google style docstrings
- **Comments**: Explain complex logic, not obvious code
- **README**: Update when adding new features
- **Type Hints**: Use type hints for function parameters and returns

## 🧪 Testing

### Writing Tests

```python
import pytest
import pandas as pd
from src.core.rfm_calculator import RFMCalculator

def test_rfm_calculation():
    """Test RFM score calculation."""
    # Create sample data
    data = pd.DataFrame({
        'Recency': [10, 20, 30],
        'Frequency': [5, 10, 15],
        'Monetary': [100, 200, 300]
    })
    
    # Test calculation
    calculator = RFMCalculator()
    result = calculator.calculate_rfm_scores(data)
    
    # Assertions
    assert 'R_Score' in result.columns
    assert 'F_Score' in result.columns
    assert 'M_Score' in result.columns
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_rfm_calculator.py
```

## 📚 Documentation Contributions

### Types of Documentation

1. **Code Documentation**
   - Docstrings for functions and classes
   - Inline comments for complex logic
   - Type hints

2. **User Documentation**
   - README updates
   - Tutorial notebooks
   - API documentation

3. **Developer Documentation**
   - Architecture decisions
   - Contributing guidelines
   - Development setup

### Documentation Style

- Use **clear, concise language**
- Include **examples** where helpful
- Use **markdown formatting** consistently
- Add **screenshots** for UI changes

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] CHANGELOG updated
- [ ] Release notes prepared

## 🎯 Areas for Contribution

### High Priority

- 🐛 **Bug fixes** in existing functionality
- 📚 **Documentation improvements**
- 🧪 **Test coverage** improvements
- 🚀 **Performance optimizations**

### Medium Priority

- 🎨 **UI/UX improvements** for notebooks
- 🌐 **Multi-language support**
- 📊 **Additional visualization types**
- 🔧 **Configuration options**

### Low Priority

- 🐳 **Docker support**
- ☁️ **Cloud deployment guides**
- 📱 **Mobile-friendly documentation**
- 🎯 **Integration examples**

## 💬 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

- **Be respectful** and constructive
- **Be patient** with newcomers
- **Be open** to feedback and suggestions
- **Be collaborative** and helpful

### Communication Channels

- 💬 **GitHub Issues**: Bug reports and feature requests
- 💬 **GitHub Discussions**: General questions and ideas
- 📧 **Email**: massoud@example.com for sensitive issues

## 🏆 Recognition

Contributors will be recognized in:

- 📄 **README.md** contributors section
- 📋 **CHANGELOG.md** for significant contributions
- 🏆 **GitHub contributor stats**
- 📢 **Release notes** for major features

## ❓ Questions?

If you have questions about contributing:

1. **Check existing issues** and discussions
2. **Read the documentation**
3. **Create a new issue** with the "question" label
4. **Email us** at massoud@example.com

---

**Thank you for contributing to RFM Insight Engine! 🙏**

*Your contributions help make customer analytics accessible to everyone.*
