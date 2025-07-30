#!/usr/bin/env python3
"""
Generate example plots for README documentation.

This script generates the example PNGs referenced in the README:
- violin_example.png (3-group violin plot)
- boxplot_example.png (3-group box plot)
- violin_2groups_example.png (2-group violin plot)
- boxplot_2groups_example.png (2-group box plot)
"""

import os
import sys

# Add the parent directory to sys.path to import ggpubpy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import ggpubpy
    print("✓ Successfully imported ggpubpy")
except Exception as e:
    print(f"✗ Failed to import ggpubpy: {e}")
    sys.exit(1)

import matplotlib.pyplot as plt


def main():
    """Generate all example plots for README."""
    # Generate PNGs in current directory (examples folder)
    examples_dir = "."
    
    # Load the iris dataset
    print("Loading iris dataset...")
    try:
        iris = ggpubpy.datasets.load_iris()
        print(f"✓ Loaded iris dataset with {len(iris)} rows")
        print(f"  Columns: {list(iris.columns)}")
        print(f"  Species: {iris['species'].unique()}")
    except Exception as e:
        print(f"✗ Failed to load iris dataset: {e}")
        return
    
    print("Generating example plots...")    # 1. Violin plot - 3 groups (all species) - NON-PARAMETRIC
    print("  - violin_example.png (3 groups, non-parametric)")
    try:
        fig, ax = ggpubpy.violinggplot(
            df=iris,
            x='species',
            y='sepal_length',
            x_label='Species',
            y_label='Sepal Length (cm)',
            parametric=False  # Non-parametric tests
        )
        plt.suptitle('Iris Dataset: Sepal Length by Species (Non-parametric)', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(examples_dir, 'violin_example.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ Generated violin_example.png")
    except Exception as e:
        print(f"    ✗ Failed to generate violin_example.png: {e}")
    
    # 2. Box plot - 3 groups (all species) - PARAMETRIC
    print("  - boxplot_example.png (3 groups, parametric)")
    try:
        fig, ax = ggpubpy.boxggplot(
            df=iris,
            x='species',
            y='sepal_length',
            x_label='Species',
            y_label='Sepal Length (cm)',
            parametric=True  # Parametric tests (ANOVA)
        )
        plt.suptitle('Iris Dataset: Sepal Length by Species (Parametric)', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(examples_dir, 'boxplot_example.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ Generated boxplot_example.png")
    except Exception as e:
        print(f"    ✗ Failed to generate boxplot_example.png: {e}")
    
    # 3. Violin plot - 2 groups (setosa vs versicolor) - PARAMETRIC
    print("  - violin_2groups_example.png (2 groups, parametric)")
    try:
        iris_2groups = iris[iris['species'].isin(['setosa', 'versicolor'])]
        fig, ax = ggpubpy.violinggplot(
            df=iris_2groups,
            x='species',
            y='sepal_length',
            x_label='Species',
            y_label='Sepal Length (cm)',
            parametric=True  # Parametric tests (t-test)
        )
        plt.suptitle('Iris Dataset: Setosa vs Versicolor (Parametric)', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(examples_dir, 'violin_2groups_example.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ Generated violin_2groups_example.png")
    except Exception as e:
        print(f"    ✗ Failed to generate violin_2groups_example.png: {e}")
    
    # 4. Box plot - 2 groups (setosa vs versicolor) - NON-PARAMETRIC
    print("  - boxplot_2groups_example.png (2 groups, non-parametric)")
    try:
        fig, ax = ggpubpy.boxggplot(
            df=iris_2groups,
            x='species',
            y='sepal_length',
            x_label='Species',
            y_label='Sepal Length (cm)',
            parametric=False  # Non-parametric tests (Mann-Whitney U)
        )
        plt.suptitle('Iris Dataset: Setosa vs Versicolor (Non-parametric)', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(examples_dir, 'boxplot_2groups_example.png'), dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ Generated boxplot_2groups_example.png")
    except Exception as e:
        print(f"    ✗ Failed to generate boxplot_2groups_example.png: {e}")
    
    print("\nSummary:")
    for filename in ['violin_example.png', 'boxplot_example.png', 
                    'violin_2groups_example.png', 'boxplot_2groups_example.png']:
        filepath = os.path.join(examples_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} (MISSING)")


if __name__ == "__main__":
    main()
