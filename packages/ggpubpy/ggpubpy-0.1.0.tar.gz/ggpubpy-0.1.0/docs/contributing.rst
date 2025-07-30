# Contributing to ggpubpy

**🎉 Welcome Contributors!** We're excited that you're interested in contributing to ggpubpy! This project is designed to be **contribution-friendly** and we welcome contributions of all kinds.

## 🚀 Project Status

✅ **Ready for Contributions!** This project is actively maintained and ready for community contributions.

## Ways to Contribute

### 🐛 Bug Reports
- Found a bug? Please open an issue on GitHub
- Include a minimal reproducible example
- Describe your environment (Python version, OS, package versions)

### 💡 Feature Requests  
- Have an idea for a new feature? We'd love to hear it!
- Open an issue with the "enhancement" label
- Describe your use case and proposed solution

### 📖 Documentation
- Improve existing documentation
- Add more examples
- Fix typos or unclear explanations
- Translate documentation (future)

### 🔧 Code Contributions
- Fix bugs
- Implement new features
- Improve performance
- Add new statistical tests
- Enhance plotting options

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/ggpubpy.git
cd ggpubpy
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Verify Setup

```bash
# Run the comprehensive test suite
python final_check.py

# Generate example plots
cd examples/
python generate_examples.py
```

## 🧪 Running Tests

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=ggpubpy --cov-report=html
```

### Integration Tests
```bash
# Run comprehensive integration test
python final_check.py
```

### Code Quality
```bash
# Format code
black ggpubpy/ tests/

# Sort imports  
isort ggpubpy/ tests/

# Lint code
flake8 ggpubpy/ tests/

# Type checking
mypy ggpubpy/
```

## 📝 Coding Standards

### Code Style
- Follow **PEP 8** style guidelines
- Use **Black** for code formatting
- Use **isort** for import sorting
- Maximum line length: 88 characters

### Documentation
- All public functions must have **docstrings**
- Use **NumPy-style docstrings**
- Include examples in docstrings when helpful
- Update documentation for new features

### Testing
- Write tests for new functionality
- Maintain test coverage above 80%
- Include integration tests for major features
- Test edge cases and error conditions

## 🔄 Contribution Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write your code
- Add/update tests
- Update documentation
- Run tests locally

### 3. Commit Changes
```bash
git add .
git commit -m "feat: add new plotting feature"
```

**Commit Message Format:**
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` test additions/changes
- `refactor:` code refactoring
- `style:` formatting changes

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots for visual changes
- Test results

## 🎯 Priority Areas

We're especially looking for contributions in these areas:

### 🔬 New Statistical Tests
- Additional parametric/non-parametric tests
- Effect size calculations
- Multiple comparison corrections
- Bayesian statistics integration

### 🎨 Visualization Features
- New plot types (bar plots, scatter plots, etc.)
- Additional color palettes
- Theme system
- Interactive plotting support

### 📊 Data Support
- More built-in datasets
- Data validation improvements
- Support for different data formats
- Missing data handling

### 🚀 Performance
- Optimize plotting performance
- Memory usage improvements
- Parallel processing support

### 📱 Ecosystem Integration
- Jupyter notebook widgets
- Streamlit components
- Plotly backend support
- Integration with other viz libraries

## 💬 Community

### Getting Help
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: akbaslint@gmail.com for private inquiries

### Code of Conduct
We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and inclusive in all interactions.

## 🏆 Recognition

Contributors will be:
- Listed in the AUTHORS file
- Mentioned in release notes
- Acknowledged in documentation
- Invited to join the core team for significant contributions

## 📚 Resources

- [GitHub Repository](https://github.com/turkalpmd/ggpubpy)
- [Documentation](https://ggpubpy.readthedocs.io/) (when available)
- [PyPI Package](https://pypi.org/project/ggpubpy/)
- [Example Gallery](examples/)

## ❓ Questions?

Don't hesitate to reach out! We're here to help and excited to work with you.

**Thank you for contributing to ggpubpy!** 🙏
