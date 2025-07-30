"""
Built-in datasets for ggpubpy examples and testing.

This module provides easy access to commonly used datasets for demonstration
and testing purposes.
"""

import os
from typing import Dict, Any

import pandas as pd


def _get_data_path() -> str:
    """Get the path to the data directory."""
    return os.path.join(os.path.dirname(__file__), "data")


def load_iris() -> pd.DataFrame:
    """
    Load the famous iris dataset.

    The iris dataset contains measurements of sepal and petal dimensions
    for three species of iris flowers (setosa, versicolor, virginica).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: sepal_length, sepal_width, petal_length,
        petal_width, species.

    Examples
    --------
    >>> from ggpubpy.datasets import load_iris
    >>> iris = load_iris()
    >>> iris.head()
    """
    data_path = _get_data_path()
    iris_path = os.path.join(data_path, "iris.csv")
    return pd.read_csv(iris_path)


def get_iris_palette() -> Dict[str, str]:
    """
    Get the default color palette for iris species.

    Returns
    -------
    dict
        Dictionary mapping species names to hex colors.
          Examples
    --------
    >>> from ggpubpy.datasets import get_iris_palette
    >>> palette = get_iris_palette()
    >>> print(palette)
    {'setosa': '#00AFBB', 'versicolor': '#E7B800', 'virginica': '#FC4E07'}
    """
    return {"setosa": "#00AFBB", "versicolor": "#E7B800", "virginica": "#FC4E07"}


def list_datasets() -> Dict[str, Any]:
    """
    List all available datasets with descriptions.

    Returns
    -------
    dict
        Dictionary with dataset names as keys and descriptions as values.
    """
    return {
        "iris": {
            "description": "The famous iris flower dataset with sepal/petal measurements",
            "shape": (150, 5),
            "columns": [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width",
                "species",
            ],
            "loader": load_iris,
        }
    }
