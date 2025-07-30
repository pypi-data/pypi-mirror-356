"""
Core plotting functions for ggpubpy.

This module contains the main plotting functions that create publication-ready
plots with statistical annotations.
"""

import itertools
from typing import Dict, List, Optional, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, f_oneway, ttest_ind


# Default color palette - updated with new colors
DEFAULT_PALETTE = [
    "#00AFBB", "#E7B800", "#FC4E07",
    "#4E79A7", "#E15759", "#59A14F", "#EDC948",
    "#B07AA1", "#FF9DA7", "#9C755F"
]


def _validate_inputs(df: pd.DataFrame, x: str, y: str, order: Optional[List] = None) -> None:
    """
    Validate input parameters for plotting functions.
    
    Parameters
    ----------
    df : pd.DataFrame
        The input dataframe.
    x : str
        Column name for categories.
    y : str
        Column name for numeric values.
    order : list, optional
        Order of categories.
        
    Raises
    ------
    AssertionError
        If inputs are invalid.
    """
    assert isinstance(df, pd.DataFrame), "df must be a pandas DataFrame"
    assert not df.empty, "DataFrame cannot be empty"
    assert x in df.columns, f"Column '{x}' not found in DataFrame"
    assert y in df.columns, f"Column '{y}' not found in DataFrame"
    assert pd.api.types.is_numeric_dtype(df[y]), f"Column '{y}' must be numeric"
    
    # Check if we have valid data after dropping NaN
    valid_data = df[[x, y]].dropna()
    assert not valid_data.empty, "No valid data remaining after removing NaN values"
    
    unique_groups = valid_data[x].unique()
    assert len(unique_groups) >= 1, f"Column '{x}' must have at least 1 unique value"
    
    if order is not None:
        assert isinstance(order, (list, tuple)), "order must be a list or tuple"
        assert all(item in unique_groups for item in order), "All items in order must exist in the data"


def _perform_statistical_tests(
    groups: List[np.ndarray], 
    parametric: bool = False
) -> Tuple[float, float, List[Tuple[int, int, float]]]:
    """
    Perform statistical tests on groups.
    
    Parameters
    ----------
    groups : list of arrays
        List of numeric arrays for each group.
    parametric : bool
        If True, use parametric tests (ANOVA, t-test).
        If False, use non-parametric tests (Kruskal-Wallis, Mann-Whitney U).
        
    Returns
    -------
    tuple
        (global_stat, global_p, pairwise_results)
        where pairwise_results is list of (i, j, p_value) tuples.
    """
    assert len(groups) >= 1, "At least one group is required"
    
    # Filter out empty groups
    valid_groups = [g for g in groups if len(g) > 0]
    assert len(valid_groups) >= 1, "At least one non-empty group is required"
    
    if len(valid_groups) == 1:
        return np.nan, np.nan, []
    
    # Global test
    if parametric:
        # One-way ANOVA for parametric case
        global_stat, global_p = f_oneway(*valid_groups)
    else:
        # Kruskal-Wallis for non-parametric case
        global_stat, global_p = kruskal(*valid_groups)
    
    # Pairwise tests
    pairwise_results = []
    valid_indices = [i for i, g in enumerate(groups) if len(g) > 0]
    
    for i, j in itertools.combinations(range(len(valid_indices)), 2):
        idx_i, idx_j = valid_indices[i], valid_indices[j]
        
        if parametric:
            # Independent t-test for parametric case
            _, p_val = ttest_ind(groups[idx_i], groups[idx_j])
        else:
            # Mann-Whitney U test for non-parametric case
            _, p_val = mannwhitneyu(groups[idx_i], groups[idx_j], alternative="two-sided")
        
        pairwise_results.append((idx_i, idx_j, p_val))
    
    return global_stat, global_p, pairwise_results


def significance_stars(p: float) -> str:
    """
    Convert a p-value into star notation.

    Parameters
    ----------
    p : float
        The p-value to convert.

    Returns
    -------
    str
        Star notation: "****" for p < 1e-4, "***" for p < 1e-3,
        "**" for p < 0.01, "*" for p < 0.05, "ns" for p >= 0.05.
    """
    if p < 1e-4:
        return "****"
    if p < 1e-3:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


def format_p_value(p: float) -> str:
    """
    Format p-value for display in statistical annotations.
    
    Parameters
    ----------
    p : float
        The p-value to format.
        
    Returns
    -------
    str
        Formatted p-value string. Shows "<0.001" for very small values.
    """
    if p <= 0.001:
        return "<0.001"
    elif p < 0.01:
        return f"{p:.3f}"
    else:
        return f"{p:.2f}"


def _get_palette_for_data(
    levels: List, 
    palette: Optional[Dict] = None
) -> Dict:
    """
    Generate a color palette for the given data levels.
    
    Parameters
    ----------
    levels : list
        List of unique category levels.
    palette : dict, optional
        User-provided palette mapping levels to colors.
        
    Returns
    -------
    dict
        Dictionary mapping each level to a color.
    """
    if palette is not None:
        # Use provided palette, fill missing levels with defaults
        result_palette = {}
        for i, level in enumerate(levels):
            if level in palette:
                result_palette[level] = palette[level]
            else:
                result_palette[level] = DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)]
        return result_palette
    else:
        # Use default palette
        return {level: DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)] 
                for i, level in enumerate(levels)}


def plot_violin_with_stats(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    order: Optional[List] = None,
    palette: Optional[Dict] = None,
    figsize: Tuple[int, int] = (6, 6),
    figsize_scale: float = 1.0,
    add_jitter: bool = True,
    jitter_std: float = 0.04,
    violin_width: float = 0.6,
    box_width: float = 0.15,
    global_test: bool = True,
    pairwise_test: bool = True,
    parametric: bool = False,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Draw a violin + boxplot + jitter + stats.

    Parameters
    ----------
    df : pd.DataFrame
        Your data.
    x : str
        Categorical column name.
    y : str
        Numeric column name.
    x_label : str, optional
        Custom label for the x-axis.
    y_label : str, optional
        Custom label for the y-axis.
    order : list, optional
        Order of x categories. Defaults to sorted unique values.
    palette : dict, optional
        Mapping from category -> color.
    figsize : tuple
        Figure size.
    figsize_scale : float
        Scale factor for figure size.
    add_jitter : bool
        Whether to add jittered points.
    jitter_std : float
        Standard deviation for horizontal jitter.
    violin_width : float
        Width of violin plots.
    box_width : float
        Width of boxplots inside violins.
    global_test : bool
        Whether to perform global statistical test.
    pairwise_test : bool
        Whether to perform pairwise statistical tests.
    parametric : bool
        If True, use parametric tests (ANOVA + t-test).
        If False, use non-parametric tests (Kruskal-Wallis + Mann-Whitney U).

    Returns
    -------
    tuple
        (figure, axes) matplotlib objects.
    """
    # Validate inputs
    _validate_inputs(df, x, y, order)
    assert isinstance(figsize, (tuple, list)) and len(figsize) == 2, "figsize must be a tuple/list of length 2"
    assert figsize_scale > 0, "figsize_scale must be positive"
    assert jitter_std >= 0, "jitter_std must be non-negative"
    assert violin_width > 0, "violin_width must be positive"
    assert box_width > 0, "box_width must be positive"
    assert isinstance(parametric, bool), "parametric must be a boolean"    # Prepare category levels and corresponding data
    levels = order if order is not None else sorted(df[x].unique())
    groups = [df[df[x] == lvl][y].dropna().values for lvl in levels]
    positions = np.arange(len(levels)) + 1
    
    # Generate color palette
    color_palette = _get_palette_for_data(levels, palette)

    # Statistical tests
    global_stat, global_p, pairwise = _perform_statistical_tests(groups, parametric)
    
    # Filter pairwise results if pairwise_test is False
    if not pairwise_test:
        pairwise = []

    # Create figure
    scaled_figsize = (figsize[0] * figsize_scale, figsize[1] * figsize_scale)
    fig, ax = plt.subplots(figsize=scaled_figsize)    # Violin plots
    violin_parts = ax.violinplot(groups, positions=positions, 
                                widths=violin_width, showextrema=True, 
                                showmedians=False, showmeans=False)    # Color the violins with palette
    for idx, body in enumerate(violin_parts['bodies']):
        level = levels[idx]
        color = color_palette[level]
        body.set_facecolor(color)
        body.set_edgecolor("black")
        body.set_alpha(1.0)  # Fully filled violin
    
    # Color the violin extrema lines if they exist (these are LineCollection objects)
    if 'cmins' in violin_parts and violin_parts['cmins'] is not None:
        violin_parts['cmins'].set_color("black")
        violin_parts['cmins'].set_linewidth(1)
    if 'cmaxes' in violin_parts and violin_parts['cmaxes'] is not None:
        violin_parts['cmaxes'].set_color("black")
        violin_parts['cmaxes'].set_linewidth(1)
    if 'cbars' in violin_parts and violin_parts['cbars'] is not None:
        violin_parts['cbars'].set_color("black")
        violin_parts['cbars'].set_linewidth(1)

    # Boxplots - white background
    ax.boxplot(groups, positions=positions, widths=box_width,
               patch_artist=True, showfliers=False,
               boxprops=dict(facecolor="white", color="black"),
               whiskerprops=dict(color="black"),
               capprops=dict(color="black"),               medianprops=dict(color="black"))

    # Add jittered points
    if add_jitter:
        rng = np.random.default_rng(0)
        for pos, values in zip(positions, groups):
            xs = rng.normal(pos, jitter_std, size=len(values))
            ax.scatter(xs, values, s=15, color="k", alpha=0.6, zorder=3)

    # Statistical annotations
    data_min = np.min([np.min(g) for g in groups if len(g) > 0])
    data_max = np.max([np.max(g) for g in groups if len(g) > 0])
    span = data_max - data_min
    base = data_max + 0.1 * span
    step = 0.1 * span    # Pairwise annotations
    for idx, (i, j, pval) in enumerate(pairwise):
        i_pos, j_pos = positions[i], positions[j]
        y0 = base + step * idx
        p_text = significance_stars(pval)
        ax.plot(
            [i_pos, i_pos, j_pos, j_pos],
            [y0, y0 + 0.02 * span, y0 + 0.02 * span, y0],
            color="black",        )
        ax.text((i_pos + j_pos) / 2, y0 + 0.03 * span, p_text, ha="center", va="bottom")

    # Global test annotation
    if global_test and not np.isnan(global_p):
        test_name = "One-way ANOVA" if parametric else "Kruskal-Wallis"
        p_formatted = format_p_value(global_p)
        ax.text(
            positions[0],
            base + step * (len(pairwise) + 0.4),
            f"{test_name} p = {p_formatted}",
            fontsize=10,
            va="bottom",
        )    # Axis labels
    ax.set_xticks(positions)
    ax.set_xticklabels(levels)
    ax.set_xlabel(x_label or x)
    ax.set_ylabel(y_label or y)
    
    # Legend
    handles = [mpatches.Patch(color=color_palette[l], label=l) for l in levels]
    ax.legend(handles=handles, title=(x_label or x))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(data_min - 0.05 * span, base + step * (len(pairwise) + 0.6))
    plt.tight_layout()
    return fig, ax


def plot_boxplot_with_stats(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    order: Optional[List] = None,
    palette: Optional[Dict] = None,
    figsize: Tuple[int, int] = (6, 6),
    add_jitter: bool = True,
    jitter_std: float = 0.04,
    box_width: float = 0.6,
    global_test: bool = True,
    pairwise_test: bool = True,
    parametric: bool = False,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Draw a colored boxplot with jittered points and statistical annotations.

    Parameters
    ----------
    df : pd.DataFrame
        Your data.
    x : str
        Column name for categories (must be categorical).
    y : str
        Column name for numeric values.
    x_label, y_label : str, optional        Axis labels. Defaults to column names.
    order : list, optional
        Order of x categories. Defaults to sorted unique values.
    palette : dict, optional
        Mapping from category -> color.
    figsize : tuple
        Figure size.
    add_jitter : bool
        Whether to add jittered points.
    jitter_std : float
        Standard deviation for horizontal jitter.    box_width : float
        Width of each box in the plot.
    global_test : bool
        Whether to perform and display global statistical test.
    pairwise_test : bool  
        Whether to perform and display pairwise comparisons.
    parametric : bool
        If True, use parametric tests (ANOVA + t-test).
        If False, use non-parametric tests (Kruskal-Wallis + Mann-Whitney U).

    Returns
    -------
    tuple        (figure, axes) matplotlib objects.
    """    # Validate inputs
    _validate_inputs(df, x, y, order)
    assert isinstance(figsize, (tuple, list)) and len(figsize) == 2, "figsize must be a tuple/list of length 2"
    assert isinstance(add_jitter, bool), "add_jitter must be a boolean"
    assert jitter_std >= 0, "jitter_std must be non-negative"
    assert box_width > 0, "box_width must be positive"
    assert isinstance(parametric, bool), "parametric must be a boolean"
    
    # Prepare category levels and corresponding data
    levels = order if order is not None else sorted(df[x].unique())
    groups = [df[df[x] == lvl][y].dropna().values for lvl in levels]
    positions = np.arange(len(levels)) + 1
    
    # Generate color palette
    color_palette = _get_palette_for_data(levels, palette)    # Statistical tests
    global_stat, global_p, pairwise_p = _perform_statistical_tests(groups, parametric)
    
    # Filter pairwise results if pairwise_test is False
    if not pairwise_test:
        pairwise_p = []

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)    # Create boxplots
    bp = ax.boxplot(
        groups,
        positions=positions,
        widths=box_width,
        patch_artist=True,
        notch=False,
        showfliers=False,
    )
      # Define different marker shapes for each group
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
    
    # Color all box elements with palette colors
    for idx, level in enumerate(levels):
        color = color_palette[level]
        
        # Box outline
        bp["boxes"][idx].set_facecolor('none')  # Boş iç
        bp["boxes"][idx].set_edgecolor(color)   # Colored edge
        bp["boxes"][idx].set_linewidth(2)       # Kalın kenar
        
        # Whiskers (her box için 2 whisker var)
        bp["whiskers"][idx*2].set_color(color)
        bp["whiskers"][idx*2].set_linewidth(2)
        bp["whiskers"][idx*2+1].set_color(color)
        bp["whiskers"][idx*2+1].set_linewidth(2)
        
        # Caps (her box için 2 cap var)
        bp["caps"][idx*2].set_color(color)
        bp["caps"][idx*2].set_linewidth(2)
        bp["caps"][idx*2+1].set_color(color)
        bp["caps"][idx*2+1].set_linewidth(2)
          # Median line
        bp["medians"][idx].set_color(color)
        bp["medians"][idx].set_linewidth(2)
        
    # Add jittered points with different markers for each group
    if add_jitter:
        rng = np.random.default_rng(0)
        for idx, (pos, values) in enumerate(zip(positions, groups)):
            level = levels[idx]
            color = color_palette[level]
            marker = markers[idx % len(markers)]  # Different marker shapes
            xs = rng.normal(pos, jitter_std, size=len(values))
            ax.scatter(xs, values, s=20, color=color, alpha=0.7, marker=marker, zorder=3)

    # Statistical annotations
    y_min = np.min([np.min(g) for g in groups if len(g) > 0])
    y_max = np.max([np.max(g) for g in groups if len(g) > 0])
    span = y_max - y_min
    base = y_max + 0.1 * span
    step = 0.1 * span    # Pairwise annotations
    for idx, (i, j, pval) in enumerate(pairwise_p):
        i_pos, j_pos = positions[i], positions[j]
        y0 = base + step * idx
        p_text = significance_stars(pval)
        ax.plot(
            [i_pos, i_pos, j_pos, j_pos],
            [y0, y0 + 0.02 * span, y0 + 0.02 * span, y0],
            color="black",
        )
        ax.text((i_pos + j_pos) / 2, y0 + 0.03 * span, p_text, ha="center", va="bottom")# Global test annotation
    if global_test and not np.isnan(global_p):
        test_name = "One-way ANOVA" if parametric else "Kruskal-Wallis"
        p_formatted = format_p_value(global_p)
        ax.text(
            positions[0],
            base + step * (len(pairwise_p) + 0.4),
            f"{test_name} p = {p_formatted}",
            fontsize=10,
            va="bottom",
        )# Axis labels
    ax.set_xticks(positions)
    ax.set_xticklabels(levels)
    ax.set_xlabel(x_label or x)
    ax.set_ylabel(y_label or y)
    
    # Legend
    handles = [mpatches.Patch(color=color_palette[l], label=l) for l in levels]
    ax.legend(handles=handles, title=x_label or x)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(y_min - 0.05 * span, base + step * (len(pairwise_p) + 0.8))
    plt.tight_layout()
    return fig, ax
