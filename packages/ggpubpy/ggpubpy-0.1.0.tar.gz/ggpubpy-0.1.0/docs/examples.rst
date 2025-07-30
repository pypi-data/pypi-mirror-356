# Examples

## Gallery of Examples

### Basic Plots

#### Three-Group Violin Plot
```python
import ggpubpy
from ggpubpy.datasets import load_iris

iris = load_iris()

fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    x_label='Species',
    y_label='Sepal Length (cm)'
)
```

#### Three-Group Box Plot
```python
fig, ax = ggpubpy.boxggplot(
    df=iris,
    x='species',
    y='sepal_length',
    x_label='Species',
    y_label='Sepal Length (cm)'
)
```

### Two-Group Comparisons

```python
# Filter for two groups
iris_2groups = iris[iris['species'].isin(['setosa', 'versicolor'])]

# Violin plot comparison
fig, ax = ggpubpy.violinggplot(
    df=iris_2groups,
    x='species',
    y='sepal_length',
    parametric=True  # Use t-test for 2 groups
)
```

### Custom Styling

#### Custom Colors
```python
custom_palette = {
    'setosa': '#E74C3C',     # Red
    'versicolor': '#3498DB', # Blue  
    'virginica': '#2ECC71'   # Green
}

fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='petal_length',
    palette=custom_palette,
    x_label='Species',
    y_label='Petal Length (cm)'
)
```

#### Custom Ordering
```python
fig, ax = ggpubpy.boxggplot(
    df=iris,
    x='species',
    y='petal_width',
    order=['virginica', 'versicolor', 'setosa'],
    x_label='Species (Custom Order)',
    y_label='Petal Width (cm)'
)
```

### Statistical Test Options

#### Parametric vs Non-parametric
```python
import matplotlib.pyplot as plt

# Non-parametric (default)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ggpubpy.violinggplot(
    df=iris, x='species', y='sepal_length',
    parametric=False, ax=ax1
)
ax1.set_title('Non-parametric (Kruskal-Wallis)')

ggpubpy.violinggplot(
    df=iris, x='species', y='sepal_length', 
    parametric=True, ax=ax2
)
ax2.set_title('Parametric (ANOVA)')

plt.tight_layout()
```

#### Global Test Only
```python
# Show only global test, no pairwise comparisons
fig, ax = ggpubpy.boxggplot(
    df=iris,
    x='species',
    y='sepal_length',
    global_test=True,
    pairwise_test=False
)
```

### Advanced Usage

#### Multiple Plots
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Sepal length
ggpubpy.violinggplot(iris, 'species', 'sepal_length', ax=axes[0,0])
axes[0,0].set_title('Sepal Length')

# Sepal width  
ggpubpy.violinggplot(iris, 'species', 'sepal_width', ax=axes[0,1])
axes[0,1].set_title('Sepal Width')

# Petal length
ggpubpy.violinggplot(iris, 'species', 'petal_length', ax=axes[1,0])
axes[1,0].set_title('Petal Length')

# Petal width
ggpubpy.violinggplot(iris, 'species', 'petal_width', ax=axes[1,1])
axes[1,1].set_title('Petal Width')

plt.tight_layout()
```

#### Publication-Ready Styling
```python
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid')

fig, ax = ggpubpy.violinggplot(
    df=iris,
    x='species',
    y='sepal_length',
    x_label='Species',
    y_label='Sepal Length (cm)',
    figsize=(8, 6)
)

# Additional styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.title('Iris Sepal Length by Species', fontsize=14, fontweight='bold')
plt.tight_layout()
```

## Generate Examples

To generate all the example plots shown in the README:

```bash
cd examples/
python generate_examples.py
```

This will create PNG files for all the examples in the `examples/` directory.
