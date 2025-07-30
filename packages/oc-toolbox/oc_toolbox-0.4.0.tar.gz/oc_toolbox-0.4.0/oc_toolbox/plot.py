import io
import math
from copy import deepcopy
from typing import Any, Dict, Optional, Sequence, Tuple, Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.preprocessing import StandardScaler


def fig_to_image(fig: plt.Figure) -> Image.Image:
    """
    Converts a Matplotlib figure to a PIL Image.

    This function captures a Matplotlib figure (`plt.Figure`) in memory,
    saves it as a PNG, and returns it as a PIL Image object.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The Matplotlib figure to convert.

    Returns
    -------
    PIL.Image.Image
        A deep-copied PIL image of the rendered figure.

    Notes
    -----
    - The function uses an in-memory buffer (`io.BytesIO`) to avoid writing to disk.
    - The image is returned as a deep copy to ensure the buffer is not needed afterward.
    - Useful for exporting plots into reports, GUIs, or storing images in datasets.
    """
    with io.BytesIO() as bytes_io:
        fig.savefig(bytes_io, format="png")
        bytes_io.seek(0)
        return deepcopy(Image.open(bytes_io))


def plot_bar(
    df: pd.DataFrame,
    key: str,
    bins: Optional[int] = 30,
    figsize: Optional[tuple[int, int]] = (6, 6),
    kde: Optional[bool] = True,
) -> None:
    """
    Plots a histogram for a numerical column.

    This function visualizes the distribution of a numerical variable using a histogram
    with an optional Kernel Density Estimate (KDE) curve.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    key : str
        The column to plot.
    bins : int, optional
        The number of bins for the histogram (default: 30).
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    kde : bool, optional
        Whether to display the Kernel Density Estimate (KDE) curve (default: True).

    Returns
    -------
    None
        The function displays the histogram but does not return a value.

    Notes
    -----
    - KDE helps visualize the distribution shape more smoothly.
    - The x-axis represents the numerical values of the selected column.
    - The y-axis represents the frequency of occurrences.
    """
    # Create the histogram
    plt.figure(figsize=figsize)

    sns.histplot(df[key], bins=bins, kde=kde)

    plt.xlabel(f"{key} (units)")
    plt.ylabel("Frequency")

    plt.title(f"Histogram of {key}")

    plt.show()


def plot_bar_by_target(
    df: pd.DataFrame,
    column: str,
    target: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
    num_bins: Optional[int] = 10,
    target_coef: Optional[int] = 100,
) -> None:
    """
    Plots a bar chart showing the relationship between a numerical variable and a target.

    This function bins the numerical column into equal-width intervals, then calculates
    the mean value of the target variable for each bin and visualizes the result as a bar plot.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    column : str
        The numerical column to bin and analyze.
    target : str
        The target variable whose mean is calculated per bin.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    num_bins : int, optional
        The number of bins to divide the numerical column into (default: 10).
    target_coef : int, optional
        A scaling factor to adjust the target values in the plot (default: 100).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - The numerical column is divided into `num_bins` equally spaced bins.
    - The mean of the target variable is computed for each bin.
    - The y-axis represents the scaled mean value of the target.
    - Binned labels on the x-axis are rotated for better readability.
    """
    plt.figure(figsize=figsize)

    # Copy necessary columns
    bar_data = df.copy()[[column, target]]

    # Define bin range
    _min = math.floor(bar_data[column].min())
    _max = math.ceil(bar_data[column].max())

    # Bin the numerical column
    bar_data[f"{column}_BINNED"] = pd.cut(
        bar_data[column], bins=np.linspace(_min, _max, num=(num_bins + 1))
    )

    # Compute mean target value for each bin
    bar_groups = bar_data.groupby(f"{column}_BINNED", observed=False).mean()

    # Plot the bar chart
    plt.bar(bar_groups.index.astype(str), bar_groups[target] * target_coef)

    # Formatting
    plt.xticks(rotation=90)
    plt.xlabel(column)
    plt.ylabel(target)
    plt.title(f"{target} by {column}")

    plt.show()


def plot_bar_category(
    df: pd.DataFrame,
    figsize: Optional[tuple[int, int]] = (6, 6),
    include_other: Optional[bool] = True,
    key: Optional[str] = "category",
    limit: Optional[int] = None,
    palette: Optional[str] = "pastel",
    threshold: Optional[int] = None,
) -> None:
    """
    Plots a bar chart showing the distribution of a categorical variable.

    This function visualizes the count of unique values in the specified column
    as a bar chart, with an optional threshold to group small categories as "Other".

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (8, 6)).
    include_other : bool, optional
        Whether to include a category for "Other" (default: True).
    key : str, optional
        The categorical column to visualize (default: "category").
    limit : int, optional
        The maximum number of categories to display (default: None).
    palette : str, optional
        The color palette used for the bar chart (default: "pastel").
    threshold : int, optional
        Minimum count for a category to be included in the bar chart (default: None).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.
    """
    # Count occurrences of unique values
    category_counts = df[key].value_counts()

    if threshold is not None:
        # Filter out categories below the threshold
        target_counts = category_counts[category_counts >= threshold]
        other_count = category_counts[category_counts < threshold].sum()
    elif limit is not None:
        # Limit the number of categories to display
        target_counts = category_counts.nlargest(limit)
        other_count = category_counts[
            ~category_counts.index.isin(target_counts.index)
        ].sum()
    else:
        target_counts = category_counts
        other_count = 0

    if include_other and other_count > 0:
        target_counts["Other"] = other_count

    x = target_counts.index
    y = target_counts.values

    # Create the bar chart
    plt.figure(figsize=figsize)
    sns.barplot(
        x=x,
        y=y,
        hue=x,  # Assign hue for different colors
        palette=sns.color_palette(
            palette,
            n_colors=len(target_counts),
        ),
    )

    plt.title(f"Distribution of {key}")
    plt.xlabel(key)
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.show()


def plot_bar_missings(
    df: pd.DataFrame,
    bin_width: Optional[int] = 5,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a bar chart showing the distribution of missing values across columns.

    This function groups columns into bins based on their percentage of missing values
    and visualizes the distribution.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing missing values.
    bin_width : int, optional
        The bin width for grouping missing value percentages (default: 5%).
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - Missing values are computed as a percentage of total rows per column.
    - Columns are grouped into bins (default: 5% intervals).
    - Helps identify the distribution of missing values across columns.
    """
    # Compute the percentage of missing values per column
    missing_percentage = df.isnull().mean() * 100

    # Create bins (default: 0% to 100% in 5% increments)
    bins = range(0, 101, bin_width)
    missing_binned = pd.cut(missing_percentage, bins=bins, right=False)

    # Count the number of columns in each bin
    missing_distribution = missing_binned.value_counts().sort_index()

    # Plot the histogram
    plt.figure(figsize=figsize)

    sns.barplot(
        x=missing_distribution.index.astype(str),
        y=missing_distribution.values,
        color="royalblue",
    )

    plt.xticks(rotation=90)
    plt.xlabel("Filling Rate (%)")
    plt.ylabel("Number of Columns")
    plt.title("Column Filling Rate Distribution (5% bins)")

    plt.show()


def plot_bar_unique_classes(
    df: pd.DataFrame,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a bar chart showing the number of unique values per categorical column.

    This function selects categorical (object-type) columns from the DataFrame,
    counts the number of unique values for each, and visualizes the distribution
    using a bar chart with annotations and a dynamic color scale.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical data.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - Only categorical (`object` dtype) columns are analyzed.
    - Columns are sorted in descending order of unique value counts.
    - The number of unique values is displayed on top of each bar.
    """
    # Select categorical (object) columns
    qualitative_columns = df.select_dtypes("object")

    # Count unique values per categorical column
    unique_counts = qualitative_columns.apply(pd.Series.nunique, axis=0)

    # Sort columns by the number of unique values
    unique_counts = unique_counts.sort_values(ascending=False)

    # Normalize the color scale based on unique value counts
    norm = plt.Normalize(unique_counts.min(), unique_counts.max())
    colors = plt.cm.coolwarm(norm(unique_counts.values))

    x = unique_counts.index
    y = unique_counts.values

    # Plot the bar chart with color mapping
    plt.figure(figsize=figsize)
    ax = sns.barplot(
        x=x,
        y=y,
        hue=x,  # Assign hue for different colors
        legend=False,
        palette=list(colors),
    )

    # Annotate each bar with the unique value count
    for index, value in enumerate(unique_counts.values):
        ax.text(
            index,
            value + 1,
            str(value),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="black",
        )

    plt.xticks(rotation=90)
    plt.xlabel("Categorical Columns")
    plt.ylabel("Number of Unique Values")
    plt.title("Unique Values per Categorical Column")

    plt.show()


def plot_boxplot(
    df: pd.DataFrame,
    column: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Displays a boxplot for a specified column.

    This function generates a boxplot to visualize the distribution,
    central tendency, and potential outliers in the given column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    column : str
        The column to visualize.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the plot but does not return a value.

    Notes
    -----
    - NaN values are ignored in the boxplot.
    - The boxplot is colored orange for better visibility.
    """
    _tmp_df = df[~df[column].isna()].copy()[[column]]

    plt.figure(figsize=figsize)

    sns.boxplot(x=_tmp_df[column], color="orange")

    plt.xlabel("Nombre d'éléments")
    plt.title(f"Boxplot de {column}")

    plt.show()


def plot_elbow_curve(
    df: pd.DataFrame,
    nb_clusters_range: Optional[Sequence[int]] = None,
    figsize: Optional[Tuple[int, int]] = (6, 6),
    n_init: Optional[int] = 10,
    random_state: Optional[int] = 42,
) -> None:
    """
    Plots the elbow curve to help determine the optimal number of clusters for KMeans.

    This function normalizes the dataset, fits KMeans for a range of cluster values,
    and plots the inertia (within-cluster sum of squares) for each k. The "elbow"
    point in the curve typically indicates the ideal number of clusters.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to cluster (numerical values only).
    nb_clusters_range : Sequence[int], optional
        The range of cluster values to test (default: 2 to 9).
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    n_init : int, optional
        Number of times the KMeans algorithm will be run with different centroid seeds (default: 10).
    random_state : int, optional
        Random seed for reproducibility (default: 42).

    Returns
    -------
    None
        Displays a plot showing the elbow curve.

    Notes
    -----
    - The range of cluster values tested is from 2 to 9.
    - The optimal k is usually where the inertia begins to diminish less significantly.
    """
    X = df.copy()

    # Scaling the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Compute KMeans for different k values
    inertias = []
    nb_clusters_range = nb_clusters_range or range(2, 10)
    for k in nb_clusters_range:
        kmeans = KMeans(
            n_clusters=k,
            random_state=random_state,
            n_init=n_init,
        )
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    # Tracé du graphe
    plt.figure(figsize=figsize)
    plt.plot(nb_clusters_range, inertias, marker="o")

    plt.title("Méthode du coude pour déterminer le nombre optimal de clusters")
    plt.xlabel("Nombre de clusters (k)")
    plt.ylabel("Inertie intra-cluster")
    plt.grid(True)
    plt.show()


def plot_mean_by_cluster(
    df: pd.DataFrame,
    cluster_col: str = "cluster",
    target_col: str = "target",
    figsize: Optional[Tuple[int, int]] = (6, 6),
    title: Optional[str] = None,
) -> pd.Series:
    """
    Plots a bar chart of the mean value of a target variable for each cluster.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing cluster assignments and the target variable.
    cluster_col : str, optional
        Column name indicating the cluster assignments (default: 'cluster').
    target_col : str, optional
        Column name of the target variable to analyze (default: 'target').
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    title : str, optional
        Custom title for the plot. If None, a title is generated automatically.

    Returns
    -------
    pd.Series
        A Series containing the mean values of the target variable for each cluster.

    Notes
    -----
    - Useful for understanding how the target variable varies across clusters.
    - Assumes both columns exist in the DataFrame.
    """
    # Compute mean values of the target variable for each cluster
    mean_props = df.groupby(cluster_col)[target_col].mean().round(2)

    # Plotting
    plt.figure(figsize=figsize)
    sns.barplot(
        x=mean_props.index,
        y=mean_props.values,
    )

    if title is None:
        title = f"Mean of {target_col.replace('_', ' ')} by {cluster_col}"

    plt.title(title)
    plt.xlabel(cluster_col.capitalize())
    plt.ylabel(f"Mean of {target_col.replace('_', ' ')}")
    plt.grid(True, axis="y")
    plt.show()

    return mean_props


def plot_pie(
    df: pd.DataFrame,
    key: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
    palette: Optional[str] = "pastel",
    threshold: Optional[int] = None,
) -> None:
    """
    Plots a pie chart showing the distribution of a categorical variable.

    This function visualizes the proportion of unique values in the specified column
    as a pie chart.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    key : str
        The categorical column to visualize.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    palette : str, optional
        The color palette used for the pie chart (default: "pastel").
    threshold : int, optional
        Minimum count for a category to be included in the pie chart (default: None).

    Returns
    -------
    None
        The function displays the pie chart but does not return a value.

    Notes
    -----
    - Uses a pastel color palette for better readability.
    - Displays percentages with one decimal place.
    - The pie chart starts at a 90-degree angle for alignment.
    """
    # Count occurrences of unique values in the column
    category_counts = df[key].value_counts()

    if threshold is not None:
        # Filter out categories with fewer occurrences than the threshold
        target_counts = category_counts[category_counts >= threshold]
        # Add an "Other" category for the rest
        other_count = category_counts[category_counts < threshold].sum()
        target_counts["Other"] = other_count

    # Define a pastel color palette
    colors = sns.color_palette(palette)[0 : len(target_counts)]

    # Create the pie chart
    plt.figure(figsize=figsize)

    plt.pie(
        target_counts,
        labels=target_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )

    plt.title(f"Distribution of {key}")

    plt.show()


def plot_pie_column_types(
    df: pd.DataFrame,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a pie chart showing the distribution of column data types in a DataFrame.

    This function visualizes the proportion of different data types present in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the pie chart but does not return a value.

    Notes
    -----
    - Uses a pastel color palette for better readability.
    - Displays percentages with one decimal place.
    - Helps understand the data structure by visualizing the distribution of types.
    """
    # Count the number of columns by data type
    dtype_counts = df.dtypes.value_counts()

    # Define a pastel color palette
    colors = sns.color_palette("pastel")[0 : len(dtype_counts)]

    # Prepare labels with types and number of columns
    labels = [
        f"{dtype} ({count})"
        for dtype, count in zip(dtype_counts.index, dtype_counts.values)
    ]

    # Create the pie chart
    plt.figure(figsize=figsize)

    plt.pie(
        dtype_counts,
        autopct="%1.1f%%",
        colors=colors,
        labels=labels,
        startangle=90,
    )

    plt.title("Distribution of Columns by Data Type")

    plt.show()


def plot_heatmap_chi2(
    df: pd.DataFrame,
    X: str,
    Y: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> float:
    """
    Displays a chi-squared (χ²) contingency heatmap between two categorical variables.

    This function computes a contingency table, calculates the expected frequencies
    under independence, and visualizes the relative contribution of each cell to
    the chi-squared statistic.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical variables.
    X : str
        The first categorical variable (rows of the contingency table).
    Y : str, optional
        The second categorical variable (columns of the contingency table.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays a heatmap but does not return a value.

    Notes
    -----
    - The chi-squared test measures the association between categorical variables.
    - The heatmap colors represent the relative contribution of each cell to the
      chi-squared statistic.
    - The table is normalized by the total chi-squared value for interpretability.
    """
    cont = df[[X, Y]].pivot_table(
        aggfunc=len,
        index=X,
        columns=Y,
        margins=True,
        margins_name="total",
    )

    tx = cont.loc[:, ["total"]]
    ty = cont.loc[["total"], :]

    c = cont.fillna(0)  # On remplace les valeurs nulles par 0
    n = len(df)

    indep = tx.dot(ty) / n
    measure = (c - indep) ** 2 / indep
    xi_n = measure.sum().sum()
    table = measure / xi_n

    plt.figure(figsize=figsize)

    sns.heatmap(
        table.iloc[:-1, :-1],
        annot=c.iloc[:-1, :-1],
        cbar=False,
        cmap="Oranges",
        fmt="d",
        linewidths=0.5,
    )

    plt.title(f"Heatmap des catégories '{X}' et '{Y}'")

    plt.xlabel(Y)
    plt.ylabel(X)

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.show()


def plot_heatmap_confusion_matrix(
    y_true: pd.Series,
    y_pred: pd.Series,
    cmp: Optional[str] = "Blues",
    figsize: Optional[Tuple[int, int]] = (6, 6),
    y_mapping: Optional[Dict[int, str]] = None,
) -> None:
    """
    Displays a heatmap of the confusion matrix.

    Parameters
    ----------
    y_true : pd.Series
        Series containing true class labels.
    y_pred : pd.Series
        Series containing predicted class labels.
    cmp : str, optional
        Color palette to use for the heatmap (default: "Blues").
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    y_mapping : dict of int to str, optional
        Optional mapping from numeric class labels to readable class names.
        If None, numeric labels are used.

    Returns
    -------
    None
    """
    conf_mat = confusion_matrix(y_true, y_pred)
    y_values = sorted(np.unique(y_true))

    if y_mapping is not None:
        y_names = [y_mapping[i] for i in y_values]
    else:
        y_names = y_values

    df_cm = pd.DataFrame(conf_mat, index=y_names, columns=y_names)

    plt.figure(figsize=figsize)
    sns.heatmap(df_cm, annot=True, cmap=cmp, fmt="d")

    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.show()


def plot_heatmap_corr(
    df: pd.DataFrame,
    target: str,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    figsize: Optional[tuple[int, int]] = (6, 6),
    limit: Optional[int] = 10,
    method: Optional[str] = "spearman",
) -> None:
    """
    Plots a Pearson correlation heatmap for the most correlated numerical features with a target variable.

    This function selects the top correlated numerical columns (by absolute correlation)
    with the target variable and displays a heatmap.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    target : str
        The target variable to compute correlations against.
    ascending : bool, optional
        Whether to sort correlations in ascending order (default: True).
    columns : Sequence[str], optional
        A list of specific numerical columns to include. If None, selects the most correlated columns.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    limit : int, optional
        The number of top correlated features to display (default: 10).
    method : str, optional
        The correlation method to use (default: "spearman"). Other options include "kendall" and "pearson".

    Returns
    -------
    None
        The function displays the correlation heatmap but does not return a value.

    Notes
    -----
    - Only numerical columns are considered for correlation calculations.
    - If `columns=None`, the function selects the top correlated features with the target.
    - Uses Pearson correlation for linear relationships.
    - The heatmap masks the upper triangle for better readability.
    """
    # Select only numerical columns
    df_numeric = df.select_dtypes(include=["number"])

    if columns is None:
        # Compute correlation with target and drop NaN values
        tmp_corr = df_numeric.corr(method=method)[target].dropna()
        # Sort by absolute correlation and select the top features
        tmp_cols = tmp_corr.sort_values(ascending=ascending)

        if target in tmp_cols:
            tmp_cols = tmp_cols.drop(target)

        columns = list(tmp_cols.iloc[0:limit].index) + [target]

    # Compute the Pearson correlation matrix
    corr_matrix = df_numeric[columns].corr(method=method)

    # Create a mask to hide the upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    plt.figure(figsize=figsize)

    sns.heatmap(
        corr_matrix,
        annot=True,
        mask=mask,
        cbar=False,
        cmap="Oranges",
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title(f"{method.capitalize()} Correlation Matrix")

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.show()


def plot_by_categories(
    df: pd.DataFrame,
    column: str,
    target: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
    palette: Optional[str] = "tab10",
) -> None:
    """
    Plots the distribution of a numerical variable by categories in a target column.

    This function generates a Kernel Density Estimate (KDE) plot for a numerical column,
    grouped by categories in the target column. Each category is visualized with a
    distinct color.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.
    column : str
        The numerical column to visualize.
    target : str
        The categorical column used to group the KDE plots.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    palette : str, optional
        The color palette used for the categories (default: "tab10").

    Returns
    -------
    None
        The function displays the KDE plot but does not return a value.

    Notes
    -----
    - Each category in the target column gets a unique color from the palette.
    - The KDE plot shows the density distribution of the numerical variable.
    - A legend is added to indicate which color corresponds to each category.
    """
    plt.figure(figsize=figsize)

    categories = df[target].unique()

    # Generate a dynamic color palette
    colors = sns.color_palette(palette, len(categories))

    legends = []

    # KDE plot for each category
    for i, val in enumerate(categories):
        color = colors[i]
        label = f"{target} == {val}"

        sns.kdeplot(
            df.loc[df[target] == val, column], color=color, fill=True, label=label
        )

        legends.append(mpatches.Patch(color=color, label=label))

    # Add legend
    plt.legend(handles=legends)

    # Labeling of the plot
    plt.xlabel(column)
    plt.ylabel("Density")

    plt.title(f"Distribution of {column} by {target}")

    plt.show()


def plot_cluster_heatmap(
    df: pd.DataFrame,
    cmp: Optional[str] = "YlGnBu",
    figsize: Optional[Tuple[int, int]] = (6, 6),
    features: Optional[Sequence[str]] = None,
    cluster_col: str = "cluster",
) -> None:
    """
    Plots a heatmap showing the average values of selected features for each cluster.

    This function assumes the input DataFrame contains a 'cluster' column
    representing assigned cluster labels. It calculates the mean of each feature
    by cluster and visualizes the resulting matrix as a heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing a 'cluster' column and numerical features.
    cmp : str, optional
        Color map for the heatmap (default: "YlGnBu").
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    features : Sequence[str], optional
        List of features to include in the heatmap. If None, all columns are used.

    Returns
    -------
    None
        Displays a heatmap of average feature values per cluster.

    Notes
    -----
    - Useful for interpreting the profiles of clusters found by a clustering algorithm.
    - Assumes that the column 'cluster' exists in the input DataFrame.
    """
    if features is None:
        features = [c for c in df.columns.tolist() if c != cluster_col]

    # Average values of features by cluster
    cluster_profiles = df.groupby(cluster_col)[features].mean().round(2)

    plt.figure(figsize=figsize)
    sns.heatmap(
        cluster_profiles,
        annot=True,
        fmt=".2f",
        cmap=cmp,
    )

    plt.title("Profil moyen des clusters")
    plt.ylabel("Cluster")
    plt.xlabel("Variable")
    plt.tight_layout()
    plt.show()


def plot_cluster_heatmap_per_categories(
    df: pd.DataFrame,
    categories_column: Optional[str] = "category",
    cmp: Optional[str] = "Blues",
    figsize: Optional[Tuple[int, int]] = (6, 6),
    fmt: Optional[str] = ".2f",
) -> None:
    """
    Plots a heatmap showing the proportion of categories per cluster.

    This function groups the data by clusters and a categorical feature,
    computes the proportion of each category within each cluster, and visualizes
    the result as a heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing at least a 'cluster' column and a categorical column.
    categories_column : str, optional
        Name of the categorical column to analyze (default: "category").
    cmp : str, optional
        Seaborn colormap used in the heatmap (default: "Blues").
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    fmt : str, optional
        Format string for annotations inside the heatmap (default: ".2f").

    Returns
    -------
    None
        Displays a heatmap of category proportions per cluster.

    Notes
    -----
    - Useful for analyzing how categorical preferences (e.g. product types, behaviors)
      are distributed across identified clusters.
    - Values in the heatmap represent normalized proportions (0 to 1).
    """
    # Count occurrences of each category in each cluster
    preferred_counts = (
        df.groupby(["cluster", categories_column]).size().unstack(fill_value=0)
    )

    # Compute proportions by dividing by the total count in each cluster
    preferred_props = preferred_counts.div(
        preferred_counts.sum(axis=1),
        axis=0,
    )

    plt.figure(figsize=figsize)
    sns.heatmap(
        preferred_props,
        fmt=fmt,
        cmap=cmp,
    )

    plt.title("Proportion des catégories préférées par cluster")

    plt.xlabel("Catégorie préférée")
    plt.ylabel("Cluster")

    plt.show()


def plot_mutual_info_scores(
    df: pd.DataFrame,
    n_clusters: int = 3,
    figsize: Optional[Tuple[int, int]] = (6, 6),
) -> pd.DataFrame:
    """
    Computes and plots the mutual information scores of features relative to KMeans clusters.

    This function encodes categorical variables, removes missing values,
    applies KMeans clustering, and then evaluates the importance of each
    feature using mutual information. The results are plotted as a bar chart.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing features for clustering and importance evaluation.
    n_clusters : int, optional
        Number of clusters to create using KMeans (default: 3).
    figsize : tuple of int, optional
        Size of the figure for the bar plot (default: (12, 6)).

    Returns
    -------
    pd.DataFrame
        A sorted DataFrame with features and their corresponding mutual information scores.

    Notes
    -----
    - Categorical features are automatically label-encoded.
    - NaN values are dropped before clustering.
    - Features are sorted by importance in descending order.
    """
    X = df.copy().dropna()

    # Clustering
    cluster_labels = KMeans(
        n_clusters=n_clusters,
        random_state=0,
    ).fit_predict(X)

    # Mutual information
    selector = SelectKBest(
        score_func=mutual_info_classif,
        k="all",
    )
    selector.fit(
        X.values,
        cluster_labels,
    )

    scores = selector.scores_
    features = X.columns
    feature_scores = pd.DataFrame({"Feature": features, "Score": scores})
    feature_scores = feature_scores.sort_values(
        by="Score",
        ascending=True,
    )

    # Plot
    plt.figure(figsize=figsize)

    plt.barh(
        feature_scores["Feature"],
        feature_scores["Score"],
    )

    plt.xticks(rotation=90)

    plt.xlabel("Variables")
    plt.ylabel("Score d'information mutuelle")

    plt.title("Importance des variables pour les clusters")

    plt.show()

    return feature_scores.reset_index(drop=True)


def plot_PCA_3d(
    df: pd.DataFrame,
    features: Optional[Sequence[str]] = None,
    figsize: Optional[Tuple[int, int]] = (6, 6),
    labels: Optional[Sequence[int]] = None,
) -> None:
    """
    Applies 3D PCA to the dataset and plots individuals, optionally colored by labels.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset containing the features for PCA.
    features : list of str, optional
        List of feature names to use for PCA. If None, all columns are used.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    labels : array-like of int, optional
        List or array of labels (e.g., cluster assignments) to color the points. Default is None.

    Returns
    -------
    None
        Displays a 3D scatter plot with individuals projected on the first three principal components.

    Notes
    -----
    - If labels are provided, points are colored accordingly and a legend is added.
    - Data is automatically standardized before applying PCA.
    """
    if features is None:
        features = df.columns.tolist()

    X = df.copy()[features]
    X_scaled = StandardScaler().fit_transform(X)

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    scatter = ax.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        X_pca[:, 2],
        c=labels if labels is not None else "royalblue",
        cmap="tab10",
        alpha=0.8,
    )

    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    ax.set_title("3D PCA with Clusters" if labels is not None else "3D PCA")

    if labels is not None:
        unique_labels = sorted(set(labels))
        legend_elements = [
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=str(lbl),
                markerfacecolor=scatter.cmap(scatter.norm(lbl)),
                markersize=8,
            )
            for lbl in unique_labels
        ]
        ax.legend(handles=legend_elements, title="Clusters")

    plt.show()


def plot_PCA_individuals_per_clusters(
    df: pd.DataFrame,
    features: Optional[Sequence[str]] = None,
    figsize: Optional[Tuple[int, int]] = (6, 6),
    labels: Optional[Sequence[int]] = None,
    palette: Optional[str] = "tab10",
    x: Optional[int] = 0,
    y: Optional[int] = 1,
) -> None:
    """
    Plots individuals in 2D PCA space colored by their cluster label.

    This function applies standard scaling and PCA to reduce dimensionality
    and plots the projected data points using a scatter plot, with colors
    corresponding to the cluster labels.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the features to project.
    features : Sequence[str], optional
        List of feature names to include in the PCA. If None, all columns are used.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    labels : Sequence[int], optional
        A sequence of cluster labels corresponding to each row in `df`.
    palette : str, optional
        Seaborn color palette used for cluster coloring (default: "tab10").
    x : int, optional
        Index of the principal component for the x-axis (default: 0).
    y : int, optional
        Index of the principal component for the y-axis (default: 1).

    Returns
    -------
    None
        Displays the PCA scatter plot of individuals by cluster.

    Notes
    -----
    - Useful for visualizing how well clusters are separated in PCA-reduced space.
    - Assumes `cluster_labels` has the same length as `df`.
    """
    X = df.copy()

    if features is None:
        features = X.columns.tolist()

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Reduce dimensionality with PCA
    pca = PCA(n_components=len(features))
    X_pca = pca.fit_transform(X_scaled)

    # Add PCA components to DataFrame
    X[f"pca{x}"] = X_pca[:, x]
    X[f"pca{y}"] = X_pca[:, y]
    if labels is not None:
        X["cluster"] = labels

    plt.figure(figsize=figsize)
    sns.scatterplot(
        data=X,
        x=f"pca{x}",
        y=f"pca{y}",
        hue="cluster" if labels is not None else None,
        palette=palette,
        s=60,
    )

    plt.title("Visualisation des clusters avec PCA")

    plt.xlabel(f"Composante PC{x + 1}")
    plt.ylabel(f"Composante PC{y + 1}")

    plt.legend(title="Cluster")

    plt.grid(True)
    plt.show()


def plot_PCA_feature_projection(
    df: pd.DataFrame,
    figsize: Optional[Tuple[int, int]] = (6, 6),
    x: Optional[int] = 0,
    y: Optional[int] = 1,
    features: Optional[Sequence[str]] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> None:
    """
    Plots the PCA feature projection (correlation circle) for the first two principal components.

    This function normalizes the input features, applies PCA for dimensionality reduction,
    and visualizes the projection of each original feature in the 2D PCA space.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing only numerical features to be projected.
    figsize : tuple of int, optional
        Figure size for the plot (default: (6, 6)).
    x : int, optional
        Index of the principal component for the x-axis (default: 0).
    y : int, optional
        Index of the principal component for the y-axis (default: 1).
    features : Sequence[str], optional
        List of feature names to include. If None, uses all columns from the DataFrame.
    x_label : str, optional
        Label for the x-axis (default: "PC1").
    y_label : str, optional
        Label for the y-axis (default: "PC2").

    Returns
    -------
    None
        Displays a correlation circle showing the PCA projection of features.

    Notes
    -----
    - The PCA is performed on standardized data.
    - The plot includes arrows and labels for each feature.
    - A unit circle is drawn for interpretation of feature contributions.
    """
    X = df.copy()

    if features is None:
        features = X.columns.tolist()

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA
    pca = PCA(n_components=len(features))
    pca.fit_transform(X_scaled)

    _, ax = plt.subplots(figsize=figsize)

    for i in range(pca.components_.shape[1]):
        ax.arrow(
            0,
            0,
            pca.components_[x, i],
            pca.components_[y, i],
            head_length=0.07,
            head_width=0.07,
            width=0.02,
            color="black",
        )
        plt.text(
            pca.components_[x, i] + 0.05,
            pca.components_[y, i] + 0.05,
            features[i],
            fontsize=9,
        )

    # Centred axes
    plt.plot([-1, 1], [0, 0], color="grey", ls="--")
    plt.plot([0, 0], [-1, 1], color="grey", ls="--")

    # Labels
    x_label = x_label or f"PC{x + 1}"
    y_label = y_label or f"PC{y + 1}"

    x_ratio = round(pca.explained_variance_ratio_[x] * 100, 2)
    y_ratio = round(pca.explained_variance_ratio_[y] * 100, 2)

    plt.xlabel(f"{x_label} ({x_ratio}%)")
    plt.ylabel(f"{y_label} ({y_ratio}%)")

    plt.title(f"Cercle des corrélations ({x_label}, {y_label})")

    # Unit circle
    an = np.linspace(0, 2 * np.pi, 100)
    plt.plot(np.cos(an), np.sin(an))
    plt.axis("equal")
    plt.grid(True)
    plt.show()


def plot_pred_images(
    df,
    image_vec_col="image_vec",
    incorrect_only=True,
    limit=10,
    limit_incorrect=1,
    y_pred_col="y_pred",
    y_true_col="category_encoded",
    y_true_only_list=None,
    y_mapping=None,
):
    def _plot(_df, _limit=limit):
        plt.figure(figsize=(_limit, 1))
        for i, row in enumerate(_df.head(_limit).itertuples()):
            plt.subplot(1, _limit, i + 1)
            plt.imshow(getattr(row, image_vec_col))
            plt.axis("off")
        plt.show()

    for category in sorted(df[y_true_col].unique()):
        if y_true_only_list is not None and category not in y_true_only_list:
            continue

        subset = df[df[y_true_col] == category]

        correct = subset[subset[y_true_col] == subset[y_pred_col]]
        incorrect = subset[subset[y_true_col] != subset[y_pred_col]]

        if y_mapping is not None:
            category = f"{category} - {y_mapping[category]}"

        print(category)
        print()

        if not incorrect_only and not correct.empty:
            _plot(correct)
            print()

        if not incorrect.empty:
            # Grouper par la mauvaise catégorie prédite et trier par fréquence décroissante
            pred_counts = (
                incorrect[y_pred_col].value_counts().sort_values(ascending=False).index
            )

            for pred_cat in pred_counts[: min(len(pred_counts), limit_incorrect)]:
                label = (
                    f"{pred_cat} - {y_mapping[pred_cat]}"
                    if y_mapping
                    else str(pred_cat)
                )
                print(f"→ Incorrectement classé comme : {label}")

                _plot(incorrect[incorrect[y_pred_col] == pred_cat])
                print()


def plot_probability_distribution_per_prediction_type(
    X: pd.DataFrame,
    binwidth: Optional[float] = 0.025,
    categories_to_include: Optional[Sequence[str]] = None,
    figsize: Optional[tuple[int, int]] = (6, 6),
    title: Optional[str] = "Distribution des probabilités par type de prédiction",
    palette: Optional[str] = "tab10",
    show: Optional[bool] = True,
) -> None:
    """
    Plots the distribution of prediction probabilities by prediction type.

    This function displays a histogram of predicted probabilities grouped by
    prediction type (e.g., true_positive, false_negative, etc.). Useful for
    analyzing model confidence by classification outcome.

    Parameters
    ----------
    X : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - 'prediction_type': classification of each prediction.
        - 'probality_score': predicted probability for the positive class.
    binwidth : float, optional
        The width of the histogram bins (default: 0.025).
    categories_to_include : Sequence[str], optional
        A list of prediction types to include (e.g., ["true_positive", "false_positive"]).
        If None, all available types are included.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    title : str, optional
        Title of the plot (default: "Distribution des probabilités par type de prédiction").
    palette : str, optional
        Seaborn color palette for the histogram bars (default: "tab10").
    show : bool, optional
        Whether to display the plot immediately with `plt.show()` (default: True).

    Returns
    -------
    None
        Displays a Seaborn histogram grouped by prediction type.

    Raises
    ------
    ValueError
        If required columns are missing from the input DataFrame.
    """
    # Vérification de la présence des colonnes nécessaires
    required_columns = {"prediction_type", "probality_score"}
    missing_columns = required_columns - set(X.columns)
    if missing_columns:
        raise ValueError(
            f"Les colonnes suivantes sont absentes de X: {missing_columns}"
        )

    # Inclure les catégories spécifiées
    if categories_to_include is None:
        x_filtered = X
    else:
        x_filtered = X[X["prediction_type"].isin(categories_to_include)]

    # Vérifier que les données ne sont pas vides après filtrage
    if x_filtered.empty:
        print("Toutes les lignes ont été filtrées, il n'y a rien à tracer.")
        return

    # Créer la figure
    plt.figure(figsize=figsize)

    # Tracer l'histogramme
    sns.histplot(
        data=x_filtered,
        x="probality_score",
        hue="prediction_type",
        binwidth=binwidth,
        legend=True,
        palette=palette,
    )

    plt.title(title)

    if show:
        plt.show()


def plot_roc_curve(
    y: Union[pd.Series, np.ndarray],
    y_proba: Union[pd.Series, np.ndarray],
    figsize: Optional[tuple[int, int]] = (6, 6),
    pos_label: int = 1,
    show: Optional[bool] = True,
) -> None:
    """
    Plots the ROC curve and displays the AUC score.

    This function computes and plots the Receiver Operating Characteristic (ROC)
    curve for a binary classifier, based on the true labels and predicted probabilities.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True binary labels.
    y_proba : array-like (pandas.Series or numpy.ndarray)
        Predicted probabilities for the positive class.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    pos_label : int, optional
        The label of the positive class (default: 1).
        This is used to compute the ROC curve.
    show : bool, optional
        Whether to immediately display the plot using plt.show() (default: True).

    Returns
    -------
    None
        Displays the ROC curve.

    Notes
    -----
    - The diagonal line represents a random classifier (AUC = 0.5).
    - AUC (Area Under the Curve) is shown in the legend for model evaluation.
    """
    fpr, tpr, _ = roc_curve(y, y_proba, pos_label=pos_label)
    auc = roc_auc_score(y, y_proba)

    plt.figure(figsize=figsize)

    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")

    plt.xlabel("Taux de faux positifs (FPR)")
    plt.ylabel("Taux de vrais positifs (TPR)")
    plt.title("Courbe ROC")
    plt.legend()

    if show:
        plt.show()


def plot_shap_waterfall(
    shap_values: Any,
    vars_to_show: Sequence[str],
) -> None:
    """
    Plots a SHAP waterfall diagram using a filtered subset of features.

    Parameters
    ----------
    shap_values : shap.Explanation
        SHAP values object for a single observation.
    vars_to_show : Sequence[str]
        List of feature names to include in the waterfall plot.

    Returns
    -------
    None
        Displays the SHAP waterfall plot using the specified features.

    Raises
    ------
    ValueError
        If `vars_to_show` is empty.

    Notes
    -----
    - Only features in `vars_to_show` will be plotted.
    - This function is intended for single-instance SHAP explanations.
    """
    if not vars_to_show:
        raise ValueError("Please specify at least one variable to display.")

    # Mask for selecting relevant features
    mask = [feature in vars_to_show for feature in shap_values.feature_names]

    import shap

    # Filter SHAP explanation
    filtered_sv = shap.Explanation(
        values=shap_values.values[mask],
        base_values=shap_values.base_values,
        data=shap_values.data[mask],
        feature_names=[
            name for name in shap_values.feature_names if name in vars_to_show
        ],
    )

    # Plot
    shap.plots.waterfall(filtered_sv)


def plot_scatter_2D_data(
    X,
    figsize: Optional[tuple[int, int]] = (6, 6),
    labels: Optional[Sequence[int]] = None,
    palette: Optional[str] = "tab10",
) -> None:
    df = pd.DataFrame(
        X,
        columns=[
            "dim1",
            "dim2",
        ],
    )

    if labels is not None:
        df["labels"] = labels

    # Create the figure
    plt.figure(figsize=figsize)

    sns.scatterplot(
        x="dim1",
        y="dim2",
        hue="labels" if labels is not None else None,
        palette=sns.color_palette(palette, n_colors=7),
        s=50,
        alpha=0.6,
        data=df,
        legend="brief",
    )

    plt.title(
        "Redcuced dimensions with labeling"
        if labels is not None
        else "Reduced dimensions"
    )

    plt.xlabel("dim1")
    plt.ylabel("dim2")

    # Show the plot
    plt.show()


def plot_scatter_corr(
    df: pd.DataFrame,
    v1: str,
    v2: str,
    color_line: Optional[str] = "darkorange",
    color_map: Optional[str] = "plasma",
    figsize: Optional[tuple[int, int]] = (6, 6),
    limit: Optional[int] = 100000,
) -> None:
    """
    Plots a scatter plot with density-based coloring and a regression line.

    This function visualizes the relationship between two numerical variables
    with a scatter plot where point colors reflect density, and a regression
    line is added for trend analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    v1 : str
        The first numerical variable (x-axis).
    v2 : str
        The second numerical variable (y-axis).
    color_line : str, optional
        The color of the regression line (default: "darkorange").
    color_map : str, optional
        The colormap used to color points based on density (default: "plasma").
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    limit : int, optional
        The maximum number of rows to use from the dataset (default: 100000).

    Returns
    -------
    None
        The function displays the scatter plot but does not return a value.

    Notes
    -----
    - Missing values in `v1` and `v2` are dropped before plotting.
    - Point colors are determined based on density estimation using `gaussian_kde`.
    - A regression line is added using Seaborn's `regplot`.
    """
    # Remove missing values and limit the number of rows
    df_clean = df.dropna(subset=[v1, v2]).iloc[:limit, :]

    # Compute density for each point
    xy = np.vstack([df_clean[v1], df_clean[v2]])

    from scipy.stats import gaussian_kde

    density = gaussian_kde(xy)(xy)

    # Create the figure
    plt.figure(figsize=figsize)

    # Plot scatter points colored by density
    plt.scatter(
        df_clean[v1],
        df_clean[v2],
        c=density,
        cmap=color_map,
        alpha=0.6,
    )

    # Add regression line
    sns.regplot(
        data=df_clean,
        x=v1,
        y=v2,
        scatter=False,
        line_kws={"linewidth": 3, "color": color_line},
    )

    # Add labels and title
    plt.xlabel(v1)
    plt.ylabel(v2)
    plt.title(f"Relationship between {v1} and {v2} with Density-based Coloring")

    # Show the plot
    plt.show()
