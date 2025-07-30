import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def get_r2_score(
    df: pd.DataFrame,
    v1: str,
    v2: str,
) -> float:
    """
    Computes the R² (coefficient of determination) score for a linear regression model.

    This function fits a simple linear regression model using `v1` as the independent
    variable and `v2` as the dependent variable, then computes the R² score.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the variables.
    v1 : str
        The independent variable (feature).
    v2 : str
        The dependent variable (target).

    Returns
    -------
    float
        The R² score, measuring how well `v1` explains the variance in `v2`.

    Notes
    -----
    - The R² score ranges from 0 to 1, where a higher value indicates a better fit.
    - A score close to 1 means the model explains most of the variance in `v2`.
    - Assumes a linear relationship between `v1` and `v2`.
    """
    stat_df = df[[v1, v2]].dropna(subset=[v1, v2])

    # Extract the variables of interest
    X = stat_df[[v1]]
    y = stat_df[v2]

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predictions
    y_pred = model.predict(X)

    # Compute the R² score
    return r2_score(y, y_pred)
