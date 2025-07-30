# Installation

## Requirements

- Python 3.8+
- NumPy
- Pandas  
- Matplotlib
- SciPy

## Install from PyPI

```bash
pip install ggpubpy
```

## Install from Source

### Development Installation

```bash
# Clone the repository
git clone https://github.com/turkalpmd/ggpubpy.git
cd ggpubpy

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Dependencies

The core dependencies are automatically installed:

```
numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.5.0
scipy>=1.7.0
```

## Verify Installation

```python
import ggpubpy
print(ggpubpy.__version__)

# Test with built-in data
from ggpubpy.datasets import load_iris
iris = load_iris()
print(f"Loaded {len(iris)} rows of iris data")
```
