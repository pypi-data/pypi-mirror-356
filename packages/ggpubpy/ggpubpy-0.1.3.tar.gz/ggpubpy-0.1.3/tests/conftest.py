"""
Test configuration and fixtures for ggpubpy tests.
"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    """Create sample test data similar to ToothGrowth dataset."""
    np.random.seed(42)  # For reproducible tests

    len_05 = [
        4.2,
        11.5,
        7.3,
        5.8,
        6.4,
        10,
        11.2,
        11.2,
        5.2,
        7,
        16.5,
        16.5,
        15.2,
        17.3,
        22.5,
        13.6,
        14.5,
        18.8,
        15.5,
        23.6,
    ]
    len_1 = [
        15.2,
        21.5,
        17.6,
        9.7,
        14.5,
        16.9,
        18.9,
        18.1,
        19.7,
        22.5,
        25.5,
        26.4,
        22.9,
        23.3,
        29.4,
        23.0,
        24.8,
        30.9,
        26.4,
        27.3,
    ]
    len_2 = [
        26.4,
        32.5,
        26.7,
        21.5,
        27.3,
        25.5,
        26.4,
        30.3,
        29.4,
        31.3,
        30.9,
        31.5,
        30.0,
        30.0,
        29.4,
        34.8,
        35.2,
        32.5,
        33.3,
        37.0,
    ]

    df = pd.DataFrame(
        {"dose": np.repeat([0.5, 1.0, 2.0], len(len_05)), "len": len_05 + len_1 + len_2}
    )

    return df


@pytest.fixture
def sample_palette():
    """Create sample color palette."""
    return {0.5: "#00AFBB", 1.0: "#E7B800", 2.0: "#FC4E07"}


@pytest.fixture
def small_data():
    """Create minimal test data for edge cases."""
    return pd.DataFrame({"group": ["A", "A", "B", "B"], "value": [1, 2, 3, 4]})
