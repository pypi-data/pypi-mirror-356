# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-20

### Added
- Initial release of ggpubpy 🎉
- Core plotting functions: `violinggplot()` and `boxggplot()`
- Built-in iris dataset with `load_iris()`
- Automatic color palette system with ColorBrewer-inspired defaults
- Statistical testing support (parametric and non-parametric)
- Smart p-value formatting (stars for pairwise, formatted values for global tests)
- Comprehensive documentation and examples
- Modern Python packaging with pyproject.toml
- Full test suite with integration tests
- CI/CD pipeline with GitHub Actions
- Contribution guidelines and development setup

### Features
- **Violin plots** with fully filled violins, white boxplots, and jittered points
- **Box plots** with colored edges, white interiors, and statistical annotations
- **Statistical tests**: 
  - Non-parametric: Kruskal-Wallis + Mann-Whitney U (default)
  - Parametric: One-way ANOVA + t-test
- **Smart annotations**:
  - Pairwise comparisons: `*` (p<0.05), `**` (p<0.01), `ns` (p≥0.05)
  - Global tests: `<0.001`, `0.023`, `0.15` (formatted p-values)
- **Flexible API** with custom colors, labels, ordering, and figure sizing
- **Built-in datasets** for quick testing and reproducible examples
- **Marker shapes** - each group gets unique markers in jittered points
- **Color consistency** - same colors used across all plot elements

### Technical
- Python 3.8+ support
- Dependencies: NumPy, Pandas, Matplotlib, SciPy
- Comprehensive test coverage
- Type hints and documentation
- Black code formatting
- Pre-commit hooks for code quality

## [Unreleased]

### Planned Features
- Additional plot types (bar plots, scatter plots)
- More statistical tests and effect size calculations
- Interactive plotting support
- Additional built-in datasets
- Performance optimizations
- Plotly backend support

---

## Contributing

See [CONTRIBUTING.md](contributing.rst) for guidelines on how to contribute to this project.

## Support

- GitHub Issues: Report bugs and request features
- Documentation: Complete API reference and examples  
- Community: Active development and maintenance
