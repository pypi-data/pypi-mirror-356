# ggpubpy Documentation

Welcome to the **ggpubpy** documentation! 

ggpubpy is a Python library that provides easy-to-use functions for creating publication-ready plots with built-in statistical tests and automatic p-value annotations. Inspired by R's ggpubr package.

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
quickstart
api
examples
contributing
changelog
```

## Features

- 🎻 **Violin plots** with boxplots and jitter points
- 📊 **Box plots** with statistical annotations  
- 🎨 **Automatic color palettes** with ColorBrewer-inspired defaults
- 📈 **Built-in statistical tests** (parametric and non-parametric)
- ⭐ **Smart p-value formatting** (stars for pairwise, formatted values for global tests)
- 📦 **Built-in datasets** for quick testing and examples
- 🔧 **Clean, intuitive API** designed for researchers

## Quick Example

```python
import ggpubpy
from ggpubpy.datasets import load_iris

# Load data
iris = load_iris()

# Create violin plot with statistical tests
fig, ax = ggpubpy.violinggplot(
    df=iris, 
    x="species", 
    y="sepal_length",
    x_label="Species", 
    y_label="Sepal Length (cm)"
)
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
