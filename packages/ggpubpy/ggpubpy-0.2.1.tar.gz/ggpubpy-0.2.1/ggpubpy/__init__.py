"""
ggpubpy: matplotlib Based Publication-Ready Plots

A Python library that provides easy-to-use functions for creating and customizing
matplotlib-based, publication-ready plots with built-in statistical tests and
automatic p-value or significance star annotations.

This project is directly inspired by R's ggpubr package.
"""

from typing import Any, List, Tuple

__version__ = "0.2.1"
__author__ = "Izzet Turkalp Akbasli"
__email__ = "izzetakbasli@gmail.com"

# Import dataset functions (these don't require scipy)
from . import datasets
from .datasets import get_iris_palette, list_datasets, load_iris


# Lazy imports to avoid scipy import issues during package import
def _import_plots() -> Tuple[Any, Any, Any, List[str]]:
    """Lazy import of plots module."""
    try:
        from .plots import (
            DEFAULT_PALETTE,
            plot_boxplot_with_stats,
            plot_violin_with_stats,
            significance_stars,
        )

        return (
            plot_violin_with_stats,
            plot_boxplot_with_stats,
            significance_stars,
            DEFAULT_PALETTE,
        )
    except ImportError as e:
        raise ImportError(
            f"Could not import plotting functions. Please ensure scipy is properly installed: {e}"
        )


# Create lazy loading functions
def violinggplot(*args: Any, **kwargs: Any) -> Any:
    """Create violin plot with statistical annotations."""
    plot_violin_with_stats, _, _, _ = _import_plots()
    return plot_violin_with_stats(*args, **kwargs)


def boxggplot(*args: Any, **kwargs: Any) -> Any:
    """Create box plot with statistical annotations."""
    _, plot_boxplot_with_stats, _, _ = _import_plots()
    return plot_boxplot_with_stats(*args, **kwargs)


def plot_violin_with_stats(*args: Any, **kwargs: Any) -> Any:
    """Create violin plot with statistical annotations."""
    func, _, _, _ = _import_plots()
    return func(*args, **kwargs)


def plot_boxplot_with_stats(*args: Any, **kwargs: Any) -> Any:
    """Create box plot with statistical annotations."""
    _, func, _, _ = _import_plots()
    return func(*args, **kwargs)


def significance_stars(*args: Any, **kwargs: Any) -> Any:
    """Convert p-values to significance stars."""
    _, _, func, _ = _import_plots()
    return func(*args, **kwargs)


# Lazy DEFAULT_PALETTE access
def get_default_palette() -> List[str]:
    """Get default color palette."""
    _, _, _, palette = _import_plots()
    return palette


# Lazy loader for shift plot
def plot_shift(x: Any, y: Any, *args: Any, **kwargs: Any) -> Any:
    """Shift plot comparing two distributions."""
    try:
        from .plots import plot_shift as _shift
    except ImportError as e:
        raise ImportError(
            f"Could not import shift plot function. Please ensure dependencies are installed: {e}"
        )
    return _shift(x, y, *args, **kwargs)


# Simple DEFAULT_PALETTE for basic access without scipy dependency
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

__all__ = [
    "plot_violin_with_stats",
    "plot_boxplot_with_stats",
    "violinggplot",
    "boxggplot",
    "significance_stars",
    "DEFAULT_PALETTE",
    "datasets",
    "load_iris",
    "get_iris_palette",
    "list_datasets",
    "plot_shift",
]
