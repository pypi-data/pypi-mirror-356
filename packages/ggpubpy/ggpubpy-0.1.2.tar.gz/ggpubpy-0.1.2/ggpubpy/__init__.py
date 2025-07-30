"""
ggpubpy: matplotlib Based Publication-Ready Plots

A Python library that provides easy-to-use functions for creating and customizing 
matplotlib-based, publication-ready plots with built-in statistical tests and 
automatic p-value or significance star annotations.

This project is directly inspired by R's ggpubr package.
"""

__version__ = "0.1.2"
__author__ = "Izzet Turkalp Akbasli"
__email__ = "izzetakbasli@gmail.com"

# Import dataset functions (these don't require scipy)
from . import datasets
from .datasets import load_iris, get_iris_palette, list_datasets

# Lazy imports to avoid scipy import issues during package import
def _import_plots():
    """Lazy import of plots module."""
    try:
        from .plots import (
            plot_violin_with_stats,
            plot_boxplot_with_stats,
            significance_stars,
            DEFAULT_PALETTE,
        )
        return plot_violin_with_stats, plot_boxplot_with_stats, significance_stars, DEFAULT_PALETTE
    except ImportError as e:
        raise ImportError(f"Could not import plotting functions. Please ensure scipy is properly installed: {e}")

# Create lazy loading functions
def violinggplot(*args, **kwargs):
    """Create violin plot with statistical annotations."""
    plot_violin_with_stats, _, _, _ = _import_plots()
    return plot_violin_with_stats(*args, **kwargs)

def boxggplot(*args, **kwargs):
    """Create box plot with statistical annotations."""
    _, plot_boxplot_with_stats, _, _ = _import_plots()
    return plot_boxplot_with_stats(*args, **kwargs)

def plot_violin_with_stats(*args, **kwargs):
    """Create violin plot with statistical annotations.""" 
    func, _, _, _ = _import_plots()
    return func(*args, **kwargs)

def plot_boxplot_with_stats(*args, **kwargs):
    """Create box plot with statistical annotations."""
    _, func, _, _ = _import_plots()
    return func(*args, **kwargs)

def significance_stars(*args, **kwargs):
    """Convert p-values to significance stars."""
    _, _, func, _ = _import_plots()
    return func(*args, **kwargs)

# Lazy DEFAULT_PALETTE access
def get_default_palette():
    """Get default color palette."""
    _, _, _, palette = _import_plots()
    return palette

# Simple DEFAULT_PALETTE for basic access without scipy dependency
DEFAULT_PALETTE = [
    "#00AFBB", "#E7B800", "#FC4E07",
    "#4E79A7", "#E15759", "#59A14F", "#EDC948",
    "#B07AA1", "#FF9DA7", "#9C755F"
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
]
