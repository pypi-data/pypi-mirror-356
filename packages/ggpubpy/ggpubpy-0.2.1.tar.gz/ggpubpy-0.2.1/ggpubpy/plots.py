"""
Core plotting functions for ggpubpy.

This module contains the main plotting functions that create publication-ready
plots with statistical annotations.
"""

import itertools
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import PolyCollection
from scipy.stats import (
    beta,
    f_oneway,
    gaussian_kde,
    kruskal,
    mannwhitneyu,
    norm,
    ttest_ind,
)

# Default color palette - updated with new colors
DEFAULT_PALETTE = [
    "#00AFBB",
    "#E7B800",
    "#FC4E07",
    "#4E79A7",
    "#E15759",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
]


def _validate_inputs(
    df: pd.DataFrame, x: str, y: str, order: Optional[List] = None
) -> None:
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
        assert all(
            item in unique_groups for item in order
        ), "All items in order must exist in the data"


def _perform_statistical_tests(
    groups: List[np.ndarray], parametric: bool = False
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
            _, p_val = mannwhitneyu(
                groups[idx_i], groups[idx_j], alternative="two-sided"
            )

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


def _get_palette_for_data(levels: List, palette: Optional[Dict] = None) -> Dict:
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
        return {
            level: DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)]
            for i, level in enumerate(levels)
        }


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
    assert (
        isinstance(figsize, (tuple, list)) and len(figsize) == 2
    ), "figsize must be a tuple/list of length 2"
    assert figsize_scale > 0, "figsize_scale must be positive"
    assert jitter_std >= 0, "jitter_std must be non-negative"
    assert violin_width > 0, "violin_width must be positive"
    assert box_width > 0, "box_width must be positive"
    assert isinstance(
        parametric, bool
    ), "parametric must be a boolean"  # Prepare category levels and corresponding data
    levels = order if order is not None else sorted(df[x].unique())
    groups = [df[df[x] == lvl][y].dropna().values for lvl in levels]
    positions = np.arange(len(levels)) + 1

    # Generate color palette
    color_palette = _get_palette_for_data(levels, palette)

    # Statistical tests
    global_stat, global_p, pairwise = _perform_statistical_tests(groups, parametric)

    # Filter pairwise results if pairwise_test is False
    if not pairwise_test:
        pairwise = []  # Create figure
    scaled_figsize = (figsize[0] * figsize_scale, figsize[1] * figsize_scale)
    fig, ax = plt.subplots(figsize=scaled_figsize)

    # Violin plots
    violin_parts = ax.violinplot(
        groups,
        positions=positions,
        widths=violin_width,
        showextrema=True,
        showmedians=False,
        showmeans=False,
    )  # Color the violins with palette
    bodies = cast(List[PolyCollection], violin_parts["bodies"])
    for idx, body in enumerate(bodies):
        level = levels[idx]
        color = color_palette[level]
        body.set_facecolor(color)
        body.set_edgecolor("black")
        body.set_alpha(1.0)  # Fully filled violin

    # Color the violin extrema lines if they exist (these are LineCollection objects)
    if "cmins" in violin_parts and violin_parts["cmins"] is not None:
        violin_parts["cmins"].set_color("black")
        violin_parts["cmins"].set_linewidth(1)
    if "cmaxes" in violin_parts and violin_parts["cmaxes"] is not None:
        violin_parts["cmaxes"].set_color("black")
        violin_parts["cmaxes"].set_linewidth(1)
    if "cbars" in violin_parts and violin_parts["cbars"] is not None:
        violin_parts["cbars"].set_color("black")
        violin_parts["cbars"].set_linewidth(1)

    # Boxplots - white background
    ax.boxplot(
        groups,
        positions=positions,
        widths=box_width,
        patch_artist=True,
        showfliers=False,
        boxprops=dict(facecolor="white", color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        medianprops=dict(color="black"),
    )

    # Add jittered points
    if add_jitter:
        rng = np.random.default_rng(0)
        for pos, values in zip(positions, groups):
            xs = rng.normal(pos, jitter_std, size=len(values))
            ax.scatter(
                xs, values, s=15, color="k", alpha=0.6, zorder=3
            )  # Statistical annotations
    data_min: float = np.min([np.min(g) for g in groups if len(g) > 0])
    data_max: float = np.max([np.max(g) for g in groups if len(g) > 0])
    span = data_max - data_min
    base = data_max + 0.1 * span
    step = 0.1 * span  # Pairwise annotations
    for idx, (i, j, pval) in enumerate(pairwise):
        i_pos, j_pos = positions[i], positions[j]
        y0 = base + step * idx
        p_text = significance_stars(pval)
        ax.plot(
            [i_pos, i_pos, j_pos, j_pos],
            [y0, y0 + 0.02 * span, y0 + 0.02 * span, y0],
            color="black",
        )
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
        )  # Axis labels
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
    """  # Validate inputs
    _validate_inputs(df, x, y, order)
    assert (
        isinstance(figsize, (tuple, list)) and len(figsize) == 2
    ), "figsize must be a tuple/list of length 2"
    assert isinstance(add_jitter, bool), "add_jitter must be a boolean"
    assert jitter_std >= 0, "jitter_std must be non-negative"
    assert box_width > 0, "box_width must be positive"
    assert isinstance(parametric, bool), "parametric must be a boolean"

    # Prepare category levels and corresponding data
    levels = order if order is not None else sorted(df[x].unique())
    groups = [df[df[x] == lvl][y].dropna().values for lvl in levels]
    positions = np.arange(len(levels)) + 1

    # Generate color palette
    color_palette = _get_palette_for_data(levels, palette)  # Statistical tests
    global_stat, global_p, pairwise_p = _perform_statistical_tests(groups, parametric)

    # Filter pairwise results if pairwise_test is False
    if not pairwise_test:
        pairwise_p = []

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)  # Create boxplots
    bp = ax.boxplot(
        groups,
        positions=positions,
        widths=box_width,
        patch_artist=True,
        notch=False,
        showfliers=False,
    )
    # Define different marker shapes for each group
    markers = ["o", "s", "^", "D", "v", "<", ">", "p", "*", "h"]

    # Color all box elements with palette colors
    for idx, level in enumerate(levels):
        color = color_palette[level]

        # Box outline
        bp["boxes"][idx].set_facecolor("none")  # Boş iç
        bp["boxes"][idx].set_edgecolor(color)  # Colored edge
        bp["boxes"][idx].set_linewidth(2)  # Kalın kenar

        # Whiskers (her box için 2 whisker var)
        bp["whiskers"][idx * 2].set_color(color)
        bp["whiskers"][idx * 2].set_linewidth(2)
        bp["whiskers"][idx * 2 + 1].set_color(color)
        bp["whiskers"][idx * 2 + 1].set_linewidth(2)

        # Caps (her box için 2 cap var)
        bp["caps"][idx * 2].set_color(color)
        bp["caps"][idx * 2].set_linewidth(2)
        bp["caps"][idx * 2 + 1].set_color(color)
        bp["caps"][idx * 2 + 1].set_linewidth(2)
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
            ax.scatter(
                xs, values, s=20, color=color, alpha=0.7, marker=marker, zorder=3
            )  # Statistical annotations
    y_min: float = np.min([np.min(g) for g in groups if len(g) > 0])
    y_max: float = np.max([np.max(g) for g in groups if len(g) > 0])
    span = y_max - y_min
    base = y_max + 0.1 * span
    step = 0.1 * span  # Pairwise annotations
    for idx, (i, j, pval) in enumerate(pairwise_p):
        i_pos, j_pos = positions[i], positions[j]
        y0 = base + step * idx
        p_text = significance_stars(pval)
        ax.plot(
            [i_pos, i_pos, j_pos, j_pos],
            [y0, y0 + 0.02 * span, y0 + 0.02 * span, y0],
            color="black",
        )
        ax.text(
            (i_pos + j_pos) / 2, y0 + 0.03 * span, p_text, ha="center", va="bottom"
        )  # Global test annotation
    if global_test and not np.isnan(global_p):
        test_name = "One-way ANOVA" if parametric else "Kruskal-Wallis"
        p_formatted = format_p_value(global_p)
        ax.text(
            positions[0],
            base + step * (len(pairwise_p) + 0.4),
            f"{test_name} p = {p_formatted}",
            fontsize=10,
            va="bottom",
        )  # Axis labels
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


def _bias_corrected_ci(
    bootdist: np.ndarray, sample_point: float, alpha: float = 0.05
) -> np.ndarray:
    """Bias-corrected confidence intervals."""
    z0 = norm.ppf(np.mean(bootdist < sample_point))
    ll = norm.cdf(2 * z0 + norm.ppf(alpha / 2)) * 100
    ul = norm.cdf(2 * z0 + norm.ppf(1 - alpha / 2)) * 100
    return cast(np.ndarray, np.percentile(bootdist, [ll, ul]))


def harrelldavis(
    x: np.ndarray, quantile: Union[float, List[float], np.ndarray] = 0.5, axis: int = -1
) -> np.ndarray:
    """Harrell-Davis robust quantile estimator."""
    x = np.asarray(x)
    assert x.ndim <= 2, "Only 1D or 2D arrays supported."
    assert axis in [0, 1, -1], "Axis must be 0, 1, or -1."
    x = np.sort(x, axis=axis)
    n = x.shape[axis]
    vec = np.arange(n)
    qs = np.atleast_1d(quantile)
    res = []
    for q in qs:
        m1, m2 = (n + 1) * q, (n + 1) * (1 - q)
        w = cast(
            np.ndarray,
            beta.cdf((vec + 1) / n, m1, m2) - beta.cdf(vec / n, m1, m2),
        )
        if x.ndim > 1 and axis == 0:
            w = w[:, np.newaxis]  # Broadcast weights for column-wise operations
        val = (w * x).sum(axis=axis)
        res.append(val)
    result: np.ndarray = np.squeeze(np.array(res, dtype=np.float64))
    # Always return as array for consistent typing
    return cast(np.ndarray, np.atleast_1d(result))


def plot_shift(
    x: np.ndarray,
    y: np.ndarray,
    *,
    paired: bool = False,
    n_boot: int = 1000,
    percentiles: np.ndarray = np.arange(10, 100, 10),
    confidence: float = 0.95,
    seed: Optional[int] = None,
    show_median: bool = True,
    violin: bool = True,
    show_quantiles: bool = False,
    show_quantile_diff: bool = False,
    parametric: bool = False,
    x_name: str = "X",
    y_name: str = "Y",
) -> plt.Figure:
    """Shift plot.

    Parameters
    ----------
    x, y : array_like
        First and second set of observations.
    paired : bool
        If True, x and y are paired samples.
    n_boot : int
        Number of bootstrap iterations.
    percentiles : array_like
        Sequence of percentiles (0-100) to compute.
    confidence : float
        Confidence level for intervals.
    seed : int or None
        Random seed.
    show_median : bool
        If True, show median lines.    violin : bool
        If True, plot half-violin densities.
    show_quantiles : bool
        If True, show quantile connection lines between distributions.
    show_quantile_diff : bool
        If True, show bottom subplot with quantile differences.
    parametric : bool
        If True, use t-test; else Mann-Whitney U test.

    Returns
    -------
    fig : matplotlib Figure instance
    """
    # Safety checks
    x = np.asarray(x)
    y = np.asarray(y)
    pct = np.asarray(percentiles) / 100
    assert x.ndim == 1 and y.ndim == 1, "x and y must be 1D."
    assert (
        not np.isnan(x).any() and not np.isnan(y).any()
    ), "Missing values not allowed."
    nx, ny = x.size, y.size
    assert nx >= 10 and ny >= 10, "Each sample must have at least 10 observations."
    assert 0 < confidence < 1, "confidence must be between 0 and 1."
    if paired:
        assert (
            nx == ny
        ), "x and y must have same size when paired=True."  # Harrell-Davis quantiles
    x_per: np.ndarray = harrelldavis(x, pct)
    y_per: np.ndarray = harrelldavis(y, pct)
    delta: np.ndarray = y_per - x_per

    # Statistical test for comparison
    if parametric:
        if paired:
            from scipy.stats import ttest_rel

            stat, p_val = ttest_rel(x, y)
            test_name = "Paired t-test"
        else:
            stat, p_val = ttest_ind(x, y)
            test_name = "Independent t-test"
    else:
        if paired:
            from scipy.stats import wilcoxon

            stat, p_val = wilcoxon(x, y)
            test_name = "Wilcoxon signed-rank"
        else:
            stat, p_val = mannwhitneyu(x, y, alternative="two-sided")
            test_name = "Mann-Whitney U"

    # Bootstrap differences
    rng = np.random.default_rng(seed)
    if paired:
        bootsam = rng.choice(nx, size=(nx, n_boot), replace=True)
        x_boot_q = np.array(
            [harrelldavis(x[bootsam[:, i]], pct) for i in range(n_boot)]
        ).T
        y_boot_q = np.array(
            [harrelldavis(y[bootsam[:, i]], pct) for i in range(n_boot)]
        ).T
        bootstat = y_boot_q - x_boot_q
    else:
        x_boot_q = np.array(
            [harrelldavis(rng.choice(x, nx), pct) for _ in range(n_boot)]
        ).T
        y_boot_q = np.array(
            [harrelldavis(rng.choice(y, ny), pct) for _ in range(n_boot)]
        ).T
        bootstat = y_boot_q - x_boot_q

    # Confidence intervals
    lowers_list: List[float] = []
    medians_list: List[float] = []
    uppers_list: List[float] = []
    for i, d in enumerate(delta):
        ci = _bias_corrected_ci(bootstat[i], d, alpha=1 - confidence)
        ci_low, ci_high = ci[0], ci[1]
        med_val_ci = _bias_corrected_ci(bootstat[i], d, alpha=1)
        med_val = med_val_ci[0]
        lowers_list.append(float(ci_low))
        uppers_list.append(float(ci_high))
        medians_list.append(float(med_val))
    lowers = np.array(lowers_list)
    medians = np.array(medians_list)
    uppers = np.array(uppers_list)  # Prepare data for stripplot
    data = pd.DataFrame(
        {"value": np.concatenate([x, y]), "variable": ["X"] * nx + ["Y"] * ny}
    )  # Plot distributions
    if show_quantile_diff:
        fig = plt.figure(figsize=(10, 6))
        ax1 = plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=3)
    else:
        fig, ax1 = plt.subplots(figsize=(10, 4))  # Custom boxplots

    def adj_vals(vals: np.ndarray) -> Tuple[float, float, float, float, float]:
        percentiles_arr = cast(np.ndarray, np.percentile(vals, [25, 50, 75]))
        q1, med, q3 = percentiles_arr[0], percentiles_arr[1], percentiles_arr[2]
        iqr = q3 - q1
        lower = np.clip(q1 - 1.5 * iqr, vals.min(), q1)
        upper = np.clip(q3 + 1.5 * iqr, q3, vals.max())
        return float(q1), float(med), float(q3), float(lower), float(upper)

    for arr, y0 in zip([x, y], [1.2, -0.2]):
        q1, med, q3, lo, hi = adj_vals(np.sort(arr))
        ax1.plot(med, y0, "o", color="white", zorder=10)
        ax1.hlines(y0, q1, q3, color="k", lw=7, zorder=9)
        ax1.hlines(y0, lo, hi, color="k", lw=2, zorder=9)

    # Scatter raw data points without jitter
    ax1.scatter(x, np.full_like(x, 1.2), color="#cfcfcf", s=10, alpha=0.6, zorder=3)
    ax1.scatter(y, np.full_like(y, -0.2), color="#88bedc", s=10, alpha=0.6, zorder=3)

    if violin:
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", PendingDeprecationWarning)
            vl = ax1.violinplot([y, x], showextrema=False, vert=False, widths=1)
        bodies = cast(List[PolyCollection], vl["bodies"])
        for idx, color, offset in zip([0, 1], ["#88bedc", "#cfcfcf"], [-1.2, -0.8]):
            path = bodies[idx].get_paths()[0]
            verts: np.ndarray = cast(np.ndarray, path.vertices)
            if idx == 0:
                verts[:, 1][verts[:, 1] >= 1] = 1
            else:
                verts[:, 1][verts[:, 1] <= 2] = 2
            verts[:, 1] += offset
            bodies[idx].set_edgecolor("k")
            bodies[idx].set_facecolor(color)
            bodies[idx].set_alpha(0.8)
        if show_quantile_diff:
            ax1.set_ylim(2.2, -1.2)
        else:
            ax1.set_ylim(1.8, -0.8)  # Connect quantiles (optional)
    if show_quantiles:
        for i in range(len(pct)):
            col = (
                "#4c72b0"
                if uppers[i] < 0
                else ("#c34e52" if lowers[i] > 0 else "darkgray")
            )
            plt.plot([y_per[i], x_per[i]], [0.2, 0.8], "o-", color=col, zorder=10)
            plt.plot([x_per[i]] * 2, [0.8, 1.2], "k--", zorder=9)
            plt.plot([y_per[i]] * 2, [-0.2, 0.2], "k--", zorder=9)

    if show_median:
        m_x, m_y = np.median(x), np.median(y)
        plt.plot([m_x] * 2, [0.8, 1.2], "k-")
        plt.plot([m_y] * 2, [-0.2, 0.2], "k-")

    plt.xlabel("Scores (a.u.)", size=15)
    ax1.set_yticks([1.2, -0.2])
    ax1.set_yticklabels([x_name, y_name], size=15)
    ax1.set_ylabel("")

    # Add statistical test result to title
    p_formatted = format_p_value(p_val)
    plt.title(f"{test_name}: p = {p_formatted}", fontsize=12, pad=10)

    # Quantile shift plot (optional)
    if show_quantile_diff:
        ax2 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        for i, per in enumerate(x_per):
            col = (
                "#4c72b0"
                if uppers[i] < 0
                else ("#c34e52" if lowers[i] > 0 else "darkgray")
            )
            ax2.plot([per] * 2, [uppers[i], lowers[i]], lw=3, color=col, zorder=10)
            ax2.plot(per, medians[i], "o", ms=10, color=col, zorder=10)
        ax2.axhline(0, ls="--", lw=2, color="gray")
        ax2.set_xlabel(f"{x_name} quantiles", size=15)
        ax2.set_ylabel(f"{y_name} - {x_name} quantiles\ndifferences (a.u.)", size=10)

    plt.tight_layout()
    return fig
