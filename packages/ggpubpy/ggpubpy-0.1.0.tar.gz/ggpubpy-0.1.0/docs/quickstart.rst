# Quick Start Guide

This guide will get you up and running with ggpubpy in minutes.

## Basic Usage

### Import the Library

```python
import ggpubpy
from ggpubpy.datasets import load_iris
```

### Load Sample Data

```python
# Load the built-in iris dataset
iris = load_iris()
print(iris.head())
```

### Create Your First Plot

#### Violin Plot

```python
# Basic violin plot with statistical tests
fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length'
)
```

#### Box Plot

```python
# Basic box plot with statistical tests  
fig, ax = ggpubpy.boxggplot(
    df=iris,
    x='species', 
    y='sepal_length'
)
```

## Customization Options

### Custom Labels

```python
fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    x_label='Species',
    y_label='Sepal Length (cm)'
)
```

### Custom Colors

```python
custom_palette = {
    'setosa': '#FF6B6B',
    'versicolor': '#4ECDC4', 
    'virginica': '#45B7D1'
}

fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    palette=custom_palette
)
```

### Statistical Test Options

```python
# Parametric tests (ANOVA + t-test)
fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    parametric=True
)

# Global test only (no pairwise comparisons)
fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    global_test=True,
    pairwise_test=False
)
```

### Two-Group Comparisons

```python
# Filter for two groups
iris_2groups = iris[iris['species'].isin(['setosa', 'versicolor'])]

fig, ax = ggpubpy.boxggplot(
    df=iris_2groups,
    x='species',
    y='sepal_length'
)
```

## Understanding the Output

- **Violin plots**: Show distribution shape + box plot + jittered points
- **Box plots**: Show quartiles with jittered points and colored edges
- **Statistical annotations**: 
  - Pairwise comparisons show significance stars (*, **, ns)
  - Global tests show formatted p-values (<0.001, 0.023, etc.)
- **Colors**: Each group gets a unique color and marker shape

## Next Steps

- Check out the [API Reference](api.rst) for complete function documentation
- Browse [Examples](examples.rst) for more advanced use cases
- Learn about [Contributing](contributing.rst) to the project
