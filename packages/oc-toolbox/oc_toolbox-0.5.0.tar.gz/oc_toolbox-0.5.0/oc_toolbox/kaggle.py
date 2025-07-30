from typing import Any, Optional, Tuple

import pandas as pd
from retry import retry


def get_kaggle_api() -> Any:
    """
    Instantiates and authenticates the Kaggle API.

    This function creates an instance of the Kaggle API and authenticates it
    using the credentials stored in the user's environment
    (typically ~/.kaggle/kaggle.json).

    Returns
    -------
    KaggleApi
        An authenticated instance of the Kaggle API.

    Notes
    -----
    - Requires a valid `kaggle.json` API token file in the `~/.kaggle/` directory.
    - You must have the `kaggle` Python package installed (`pip install kaggle`).
    - This function is typically used before downloading datasets or submitting to competitions.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi

    kaggle_api = KaggleApi()
    kaggle_api.authenticate()
    return kaggle_api


@retry(tries=3, delay=3)
def get_kaggle_score(
    descr: str,
    competition: str = "home-credit-default-risk",
    kaggle_api: Optional[Any] = None,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Retrieves the public and private leaderboard scores of a Kaggle submission
    based on its description.

    Parameters
    ----------
    descr : str
        The description of the Kaggle submission to look for.
    competition : str, optional
        The Kaggle competition name or ID (default: "home-credit-default-risk").
    kaggle_api : KaggleApi, optional
        An authenticated KaggleApi instance. If None, a new one is created.

    Returns
    -------
    Tuple[Optional[float], Optional[float]]
        A tuple containing the public and private scores of the matching submission.

    Raises
    ------
    Exception
        If no matching submission with status COMPLETE and the given description is found.

    Notes
    -----
    - The function retries up to 3 times with a 3-second delay on failure (using @retry).
    - Only submissions with status `COMPLETE` are considered.
    """
    from kaggle.api.kaggle_api_extended import SubmissionStatus

    if kaggle_api is None:
        kaggle_api = get_kaggle_api()

    submissions = kaggle_api.competition_submissions(competition)

    for sub in submissions:
        if sub.status != SubmissionStatus.COMPLETE:
            continue
        if sub.description != descr:
            continue
        return (sub.public_score, sub.private_score)

    raise Exception(f"No completed submission found with description: {descr}")


def submit_to_kaggle(
    df: pd.DataFrame,
    descr: str,
    competition: str = "home-credit-default-risk",
    filename: str = "submission",
    kaggle_api: Optional[Any] = None,
) -> None:
    """
    Saves a submission DataFrame, compresses it, and submits it to a Kaggle competition.

    Parameters
    ----------
    df : pandas.DataFrame
        The submission DataFrame to be saved and submitted.
    descr : str
        The description of the submission shown on Kaggle.
    competition : str, optional
        The Kaggle competition name or ID (default: "home-credit-default-risk").
    filename : str, optional
        The base name of the file to save (without extension) (default: "submission").
    kaggle_api : KaggleApi, optional
        An authenticated instance of the Kaggle API. If None, it will be created automatically.

    Returns
    -------
    None
        Submits the compressed submission file to the specified Kaggle competition.

    Notes
    -----
    - The function creates two files: `<filename>.csv` and `<filename>.7z`.
    - Requires `py7zr` to be installed (`pip install py7zr`).
    - You must have Kaggle API credentials properly configured (`~/.kaggle/kaggle.json`).
    """
    if kaggle_api is None:
        kaggle_api = get_kaggle_api()

    # Save the submission to a CSV file
    csv_path = f"{filename}.csv"
    zip_path = f"{filename}.7z"
    df.to_csv(csv_path, index=False)

    # Compress the CSV into a 7z archive
    import py7zr

    with py7zr.SevenZipFile(zip_path, "w") as archive:
        archive.write(csv_path)

    # Submit to Kaggle
    kaggle_api.competition_submit(zip_path, descr, competition)
