# API Reference

## Core Functions

### Plot Functions

```{eval-rst}
.. autofunction:: ggpubpy.violinggplot
```

```{eval-rst}
.. autofunction:: ggpubpy.boxggplot
```

### Low-level Functions

```{eval-rst}
.. autofunction:: ggpubpy.plot_violin_with_stats
```

```{eval-rst}
.. autofunction:: ggpubpy.plot_boxplot_with_stats
```

## Dataset Functions

```{eval-rst}
.. automodule:: ggpubpy.datasets
   :members:
```

## Utility Functions

```{eval-rst}
.. autofunction:: ggpubpy.significance_stars
```

## Constants

```{eval-rst}
.. autodata:: ggpubpy.DEFAULT_PALETTE
```

## Function Parameters

### Common Parameters

- **df** (*pandas.DataFrame*): Your input data
- **x** (*str*): Column name for categories (groups)
- **y** (*str*): Column name for numeric values
- **x_label, y_label** (*str, optional*): Custom axis labels
- **order** (*list, optional*): Custom ordering of categories
- **palette** (*dict, optional*): Custom color mapping {category: color}
- **figsize** (*tuple*): Figure size (width, height) in inches
- **parametric** (*bool*): Use parametric (True) or non-parametric (False) tests
- **global_test** (*bool*): Whether to show global statistical test
- **pairwise_test** (*bool*): Whether to show pairwise comparisons

### Plot-specific Parameters

#### Violin Plots
- **violin_width** (*float*): Width of violin plots (default: 0.6)
- **box_width** (*float*): Width of inner box plots (default: 0.3)
- **add_jitter** (*bool*): Whether to add jittered points (default: True)
- **jitter_std** (*float*): Standard deviation for jitter (default: 0.04)

#### Box Plots  
- **box_width** (*float*): Width of box plots (default: 0.6)
- **add_jitter** (*bool*): Whether to add jittered points (default: True)
- **jitter_std** (*float*): Standard deviation for jitter (default: 0.04)

## Statistical Tests

### Non-parametric (default)
- **Global test**: Kruskal-Wallis H-test
- **Pairwise tests**: Mann-Whitney U test

### Parametric (parametric=True)
- **Global test**: One-way ANOVA
- **Pairwise tests**: Independent t-test

### Output Format
- **Pairwise**: Significance stars (*, **, ns)
- **Global**: Formatted p-values (<0.001, 0.023, 0.15, etc.)
