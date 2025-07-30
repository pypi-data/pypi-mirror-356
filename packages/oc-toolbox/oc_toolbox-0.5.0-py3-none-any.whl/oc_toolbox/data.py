import pandas as pd


def load_data(
    file_path="fr.openfoodfacts.org.products.csv",
    encoding="utf-8",
    sep="\t",
    **kwargs,
) -> pd.DataFrame:
    """
    Loads Open Food Facts data from a CSV file using chunk processing.

    Reads the CSV file in chunks of 100,000 rows to optimize memory usage
    and concatenates them into a single DataFrame.

    Parameters
    ----------
    file_path : str, optional
        Path to the CSV file (default: 'fr.openfoodfacts.org.products.csv').

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the loaded data.

    Notes
    -----
    - Uses `low_memory=False` to prevent mixed data types.
    - Assumes tab-separated values (`\t`).
    - May consume significant memory for large files.
    """
    chunks = pd.read_csv(
        file_path,
        chunksize=100000,
        encoding=encoding,
        low_memory=False,
        sep=sep,
        **kwargs,
    )
    return pd.concat(
        [c for c in chunks],
        ignore_index=True,
    )
