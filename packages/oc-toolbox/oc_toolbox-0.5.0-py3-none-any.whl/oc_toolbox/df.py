from collections import Counter
from functools import partial
from itertools import combinations
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

import numpy as np
import pandas as pd
from sklearn.base import (
    ClassifierMixin,
    RegressorMixin,
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfVectorizer,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    adjusted_rand_score,
    calinski_harabasz_score,
    classification_report,
    confusion_matrix,
    davies_bouldin_score,
    f1_score,
    mean_absolute_error,
    mutual_info_score,
    r2_score,
    rand_score,
    root_mean_squared_error,
    silhouette_score,
)
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import (
    LabelEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from tqdm import tqdm

from .image import (
    extract_orb_features,
    extract_sift_features,
    extract_surf_features,
    get_image_stats_from_path,
    load_and_preprocess_image_resnet50,
    load_and_preprocess_image_vgg16,
    load_and_resize_image,
)
from .text import (
    extract_fasttext_features,
)


def batch_apply(
    df: pd.DataFrame,
    col: str,
    apply_func: Callable[[Any], Any] = lambda x: x,
    batch_size: int = 50,
    should_tqdm: bool = True,
) -> pd.Series:
    """
    Applies a function to a DataFrame column in batches, with optional progress display.

    Useful when applying slow functions (e.g., API calls, NLP transforms) to large datasets,
    while preserving order and tracking progress.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the column to apply the function to.
    col : str
        Name of the column to apply the function to.
    apply_func : Callable, optional
        Function to apply to each element of the column (default: identity function).
    batch_size : int, optional
        Number of rows to process at once (default: 50).
    should_tqdm : bool, optional
        Whether to display a progress bar using tqdm (default: True).

    Returns
    -------
    pd.Series
        A Series containing the transformed values, aligned to the original index.

    Example
    -------
    >>> df["clean_text"] = batch_apply(df, col="text", apply_func=clean_text)
    """
    results = []

    slices = list(range(0, len(df), batch_size))
    _pbar = tqdm(total=len(slices)) if should_tqdm else None

    for i in slices:
        batch = df.iloc[i : i + batch_size].copy()
        batch["new_col"] = batch[col].apply(apply_func)
        results.append(batch[["new_col"]])

        if should_tqdm:
            _pbar.update(1)

    if should_tqdm:
        _pbar.close()

    result_df = pd.concat(results).sort_index()
    return result_df["new_col"]


def classification_report_to_df(
    y: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]
) -> pd.DataFrame:
    """
    Converts a classification report into a DataFrame.

    This function generates a classification report (precision, recall, f1-score, support)
    using scikit-learn and returns it as a pandas DataFrame for easier inspection and formatting.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True class labels.
    y_pred : array-like (pandas.Series or numpy.ndarray)
        Predicted class labels.

    Returns
    -------
    pandas.DataFrame
        A DataFrame version of the classification report with metrics per class and averages.

    Notes
    -----
    - Useful for saving classification metrics or visualizing them in tabular format.
    - Includes weighted, macro, and micro averages.
    """
    # Generate the classification report as a dictionary
    report_dict = classification_report(y, y_pred, output_dict=True)

    # Convert to a pandas DataFrame
    df_report = pd.DataFrame(report_dict).transpose()

    return df_report


def confusion_matrix_to_df(
    y: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]
) -> pd.DataFrame:
    """
    Converts a confusion matrix into a readable pandas DataFrame.

    This function computes the confusion matrix from true and predicted labels,
    then formats it as a DataFrame with understandable row and column labels.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True class labels.
    y_pred : array-like (pandas.Series or numpy.ndarray)
        Predicted class labels.

    Returns
    -------
    pandas.DataFrame
        A formatted confusion matrix with labels like 'expected-<class>' and 'predicted-<class>'.

    Notes
    -----
    - Automatically handles multi-class classification.
    - Replaces periods in class names with underscores for cleaner labels.
    """
    cm = confusion_matrix(y, y_pred)
    labels = np.unique(y)

    df_cm = pd.DataFrame(
        cm,
        index=[f"expected-{str(label).replace('.', '_')}" for label in labels],
        columns=[f"predicted-{str(label).replace('.', '_')}" for label in labels],
    )

    return df_cm


def create_polynomial_features(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    degree: int = 3,
    skip: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Generates polynomial features from selected numerical columns in a DataFrame,
    while optionally skipping certain columns (e.g., target variables or IDs).

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    columns : Sequence[str], optional
        A list of column names to use for generating polynomial features.
        If None, all columns are used (default: None).
    degree : int, optional
        The degree of polynomial features to generate (default: 3).
    skip : Sequence[str], optional
        List of column names to exclude from transformation but keep in the output (default: None).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the generated polynomial features, along with skipped columns.

    Notes
    -----
    - Skipped columns (e.g., target, ID) are excluded from the transformation
      and reattached to the result.
    - Column names in the output are sanitized to remove spaces.
    - Uses scikit-learn's `PolynomialFeatures` under the hood.
    """
    # Copy the original DataFrame
    poly_features = df.copy()

    # Determine which columns to use
    if columns:
        poly_features = poly_features[columns]
    else:
        columns = list(poly_features.columns)

    # Store skipped columns
    skip_dict = {col: [] for col in skip or []}

    for col in skip or []:
        if col in columns:
            skip_dict[col] = poly_features[col]
            poly_features = poly_features.drop(columns=[col])
            columns.remove(col)

    # Generate polynomial features
    poly_transformer = PolynomialFeatures(degree=degree)
    poly_array = poly_transformer.fit_transform(poly_features)

    # Convert to DataFrame with generated feature names
    poly_features = pd.DataFrame(
        poly_array, columns=poly_transformer.get_feature_names_out(columns)
    )

    # Reattach skipped columns
    for col, poly_skip in skip_dict.items():
        poly_features[col] = poly_skip

    # Clean column names
    poly_features.columns = poly_features.columns.str.replace(" ", "_")

    return poly_features


def encode_labels(
    df: pd.DataFrame,
    limit_categories: int = 2,
) -> pd.DataFrame:
    """
    Encodes categorical variables using label encoding for binary categories
    and one-hot encoding for all other categorical variables.

    This function applies label encoding to categorical columns with two or fewer unique values
    and one-hot encoding to all other categorical variables.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with categorical variables encoded.

    Notes
    -----
    - Label encoding is applied to columns with 2 or fewer unique values.
    - One-hot encoding is applied to all other categorical variables.
    - The function ensures that categorical values are transformed properly without data leakage.
    """
    tmp_df = df.copy()
    le = LabelEncoder()

    # Iterate through the columns
    for col in tmp_df:
        if tmp_df[col].dtype == "object":
            # Apply Label Encoding if the column has 2 or fewer unique categories
            if tmp_df[col].nunique() <= limit_categories:
                tmp_df[col] = le.fit_transform(tmp_df[col])

    # Apply one-hot encoding for remaining categorical variables
    return pd.get_dummies(tmp_df)


def evaluate_2D_reduction_for_clustering(
    X: pd.DataFrame,
    y_true: np.ndarray,
    method_grid: Optional[Dict[str, Any]] = None,
    param_grid: Optional[Dict[str, Dict[str, Any]]] = None,
    n_clusters: int = 5,
    sorting: Optional[str] = "Adjusted Rand Index",
) -> pd.DataFrame:
    """
    Evaluates different 2D dimensionality reduction techniques for clustering quality.

    For each combination of dimensionality reduction method and parameters,
    applies KMeans clustering and computes clustering quality metrics.

    Parameters
    ----------
    X : pd.DataFrame
        Input feature matrix.
    y_true : np.ndarray
        True labels (used for external evaluation metrics).
    method_grid : dict, optional
        Dictionary mapping method names to reduction classes (e.g., {"PCA": PCA}).
        Default includes PCA and TruncatedSVD.
    param_grid : dict, optional
        Dictionary mapping method names to parameter grids.
        Default uses {"n_components": [2]} for both methods.
    n_clusters : int, optional
        Number of clusters to use in KMeans (default: 5).
    sorting : str, optional
        Metric used to sort the result DataFrame (default: "Adjusted Rand Index").

    Returns
    -------
    pd.DataFrame
        A DataFrame with clustering evaluation scores for each reduction method and parameter combination.

    Notes
    -----
    - If a method fails to produce the expected number of clusters, it is skipped.
    - Requires `get_clustering_metrics` to be defined and accessible.
    """
    results = []

    # Handle missing values
    X_sample = X.fillna(0) if isinstance(X, pd.DataFrame) else X

    if method_grid is None:
        method_grid = {
            "PCA": PCA,
            "TruncatedSVD": TruncatedSVD,
        }

    if param_grid is None:
        param_grid = {
            "PCA": {"n_components": [2]},
            "TruncatedSVD": {"n_components": [2]},
        }

    for method_name, method_class in method_grid.items():
        for params in ParameterGrid(param_grid[method_name]):
            reducer = method_class(**params)
            X_reduced = reducer.fit_transform(X_sample)

            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init="auto",
            )
            labels = kmeans.fit_predict(X_reduced)

            if len(np.unique(labels)) != n_clusters:
                continue

            df_metrics = get_clustering_metrics(
                X_reduced,
                labels,
                y_true=y_true,
            )

            result_dict = {
                "Méthode": method_name,
                "Paramètres": params,
                "Silhouette Score": df_metrics.loc["Silhouette Score", "Score"],
                "Calinski-Harabasz Index": df_metrics.loc[
                    "Calinski-Harabasz Index", "Score"
                ],
                "Davies-Bouldin Index": df_metrics.loc["Davies-Bouldin Index", "Score"],
            }

            if y_true is not None:
                result_dict.update(
                    {
                        "Rand Index": df_metrics.loc["Rand Index", "Score"],
                        "Adjusted Rand Index": df_metrics.loc[
                            "Adjusted Rand Index", "Score"
                        ],
                        "Mutual Information": df_metrics.loc[
                            "Mutual Information", "Score"
                        ],
                    }
                )

            results.append(result_dict)

    results_df = pd.DataFrame(results)
    results_df.sort_values(by=sorting, ascending=False, inplace=True)

    return results_df


def evaluate_clustering_hyperparams(
    X: pd.DataFrame,
    clustering_alg: Type[ClassifierMixin],
    param_grid: Dict[str, Any],
    sample_size: int = None,
    y_true: Optional[np.ndarray] = None,
    sorting: Optional[str] = "Silhouette Score",
) -> pd.DataFrame:
    """
    Evaluates a grid of hyperparameters for a clustering algorithm using internal metrics.

    For each combination of parameters in the grid, the function fits the specified
    clustering algorithm on a sample of the data and computes clustering metrics
    (Silhouette Score, Calinski-Harabasz Index, Davies-Bouldin Index).

    Parameters
    ----------
    X : pd.DataFrame
        Input DataFrame with numerical features for clustering.
    clustering_alg : Type[ClassifierMixin]
        The clustering algorithm class to evaluate (e.g., KMeans, DBSCAN).
    param_grid : dict
        Dictionary representing the grid of parameters to search.
    sample_size : int, optional
        Number of rows to sample from `X` for each evaluation (default: 10000).

    Returns
    -------
    pd.DataFrame
        A DataFrame sorted by Silhouette Score, containing the metrics for each parameter combination.

    Notes
    -----
    - All NaNs in the sample are replaced by 0.
    - If a parameter combination causes an error, it is skipped and printed.
    - Requires `get_cluster_labels` and `get_clustering_metrics` to be defined elsewhere.
    """
    results = []

    if y_true is not None:
        sample_size = len(y_true)
        sorting = "Adjusted Rand Index"

    # X_sample = X.sample(n=sample_size, random_state=42).fillna(0)
    if isinstance(X, pd.DataFrame) and sample_size is not None and len(X) > sample_size:
        X_sample = X.sample(n=sample_size, random_state=42)
    else:
        # If the sample size is larger than the DataFrame, use the entire DataFrame
        X_sample = X

    if isinstance(X_sample, pd.DataFrame):
        X_sample = X_sample.fillna(0)

    for params in tqdm(ParameterGrid(param_grid), desc="Évaluation des paramètres"):
        try:
            cluster_labels = get_cluster_labels(
                X_sample,
                clustering_alg=clustering_alg,
                **params,
            )

            df_metrics = get_clustering_metrics(
                X_sample,
                cluster_labels,
                y_true=y_true,
            )

            result_dict = {
                "paramètres": params,
                "Silhouette Score": df_metrics.loc["Silhouette Score", "Score"],
                "Calinski-Harabasz Index": df_metrics.loc[
                    "Calinski-Harabasz Index", "Score"
                ],
                "Davies-Bouldin Index": df_metrics.loc["Davies-Bouldin Index", "Score"],
            }

            if y_true is not None:
                result_dict.update(
                    {
                        "Rand Index": df_metrics.loc["Rand Index", "Score"],
                        "Adjusted Rand Index": df_metrics.loc[
                            "Adjusted Rand Index", "Score"
                        ],
                        "Mutual Information": df_metrics.loc[
                            "Mutual Information", "Score"
                        ],
                    }
                )

            results.append(result_dict)

        except Exception as e:
            print(f"Erreur avec paramètres {params} : {e}")
            continue

    results_df = pd.DataFrame(results)
    results_df.sort_values(by=sorting, ascending=False, inplace=True)

    return results_df


def get_cluster_labels(
    df: pd.DataFrame,
    clustering_alg: Type[ClassifierMixin] = KMeans,
    **kwargs: Any,
) -> np.ndarray:
    """
    Applies a clustering algorithm to normalized data and returns the cluster labels.

    The function scales the input features using StandardScaler, fits the specified
    clustering algorithm, and returns the predicted cluster labels for each observation.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing numerical features to be clustered.
    clustering_alg : Type[ClassifierMixin], optional
        A scikit-learn compatible clustering algorithm class (default: KMeans).
    **kwargs : Any
        Additional keyword arguments to pass to the clustering algorithm constructor.

    Returns
    -------
    np.ndarray
        A NumPy array containing the cluster label for each row in the input DataFrame.

    Notes
    -----
    - This function does not modify the input DataFrame.
    - The clustering algorithm must implement `fit_predict()`.
    - For reproducibility, consider passing `random_state` in kwargs.
    """
    X = df.copy()

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Clustering
    model = clustering_alg(**kwargs)
    return model.fit_predict(X_scaled)


def get_clustering_metrics(
    df: pd.DataFrame,
    labels: np.ndarray,
    y_true: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """
    Computes intrinsic and extrinsic clustering evaluation metrics.

    This function evaluates the quality of clustering using internal metrics
    (Silhouette, Calinski-Harabasz, Davies-Bouldin) and, if ground-truth labels
    are available, external metrics (Rand Index, Adjusted Rand Index, Mutual Information).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the features used for clustering.
    labels : np.ndarray
        Predicted cluster labels for each row in `df`.
    y_true : np.ndarray, optional
        Ground-truth labels for supervised evaluation (optional).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the clustering metrics and their corresponding scores.

    Notes
    -----
    - Internal (intrinsic) metrics evaluate the clustering structure itself.
    - External (extrinsic) metrics compare predicted clusters to known class labels.
    - Suitable for evaluating results from any clustering algorithm.
    """
    X = df.copy()

    # Intrinsic metrics
    metrics = {
        "Silhouette Score": silhouette_score(X, labels),
        "Calinski-Harabasz Index": calinski_harabasz_score(X, labels),
        "Davies-Bouldin Index": davies_bouldin_score(X, labels),
    }

    # Extrinsic metrics (if ground truth is available)
    if y_true is not None:
        metrics.update(
            {
                "Rand Index": rand_score(y_true, labels),
                "Adjusted Rand Index": adjusted_rand_score(y_true, labels),
                "Mutual Information": mutual_info_score(y_true, labels),
            }
        )

    return pd.DataFrame.from_dict(metrics, orient="index", columns=["Score"])


def get_image_cnn_resnet50_df(
    df: pd.DataFrame,
    image_tf_col: str = "resnet50_img",
    input_size: Optional[Tuple[int, int]] = (224, 224),
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Extracts CNN feature vectors from images using the ResNet50 model (pretrained on ImageNet).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing preprocessed images in TensorFlow format.
    image_tf_col : str, optional
        Column name containing image tensors (default: "resnet50_img").
    input_size : tuple of int, optional
        Size of the input images (default: (224, 224)).
    keep_columns : list of str, optional
        Optional list of column names to retain in the output DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with one row per image and 2048 ResNet50 features
        (columns named "resnet_0" to "resnet_2047"), plus optionally retained columns.

    Notes
    -----
    - Requires TensorFlow and Keras to be installed.
    - Assumes that the image tensors are already resized and normalized.
    - The ResNet50 model is used without the top classification layers,
      with global average pooling to return a 2048-dim vector.
    """
    cnn_vectors = []
    keep_columns = keep_columns or []

    # Load ResNet50 without the top classification layers
    from tensorflow.keras.applications.resnet50 import ResNet50

    model = ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(input_size[0], input_size[1], 3),
        pooling="avg",
    )

    for idx, row in df.iterrows():
        # Predict feature vector
        feature_vec = model.predict(
            row[image_tf_col],
            verbose=0,
        ).squeeze()  # Output shape: (2048,)

        # Create dict with CNN vector and optional metadata
        row_dict = {"cnn_vector": feature_vec}
        for col in keep_columns:
            row_dict[col] = row[col]

        cnn_vectors.append(row_dict)

    # Create intermediate DataFrame with cnn_vector + metadata
    df_rnet = pd.DataFrame(cnn_vectors)

    # Expand CNN vector into separate columns
    cnn_details = df_rnet["cnn_vector"].apply(
        lambda x: pd.Series(x) if x is not None else pd.Series([np.nan] * 2048)
    )
    cnn_details.columns = [f"resnet_{i}" for i in range(2048)]

    # Concatenate with metadata if specified
    if keep_columns:
        cnn_details = pd.concat(
            [df_rnet[keep_columns], cnn_details],
            axis=1,
        )

    return cnn_details


def get_image_cnn_vgg16_df(
    df: pd.DataFrame,
    image_tf_col: str = "vgg16_img",
    input_size: Optional[Tuple[int, int]] = (224, 224),
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Extracts CNN feature vectors from images using the VGG16 model (pretrained on ImageNet).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing image tensors and optional metadata.
    image_tf_col : str, optional
        Column name containing the image tensors in TensorFlow format (default: "vgg16_img").
    input_size : tuple of int, optional
        Size of input images (height, width). Default is (224, 224).
    keep_columns : list of str, optional
        List of metadata columns to retain in the output DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with one row per image and 512 extracted CNN features
        (columns "vgg16_0" to "vgg16_511"), plus optional metadata columns.

    Notes
    -----
    - Assumes image tensors are already resized and normalized.
    - The model is loaded with `include_top=False` and `pooling='avg'`.
    """
    cnn_vectors = []
    keep_columns = keep_columns or []

    # Load VGG16 without classification head
    from tensorflow.keras.applications.vgg16 import VGG16

    model = VGG16(
        weights="imagenet",
        include_top=False,
        input_shape=(input_size[0], input_size[1], 3),
        pooling="avg",
    )

    for _, row in df.iterrows():
        # Compute CNN feature vector
        feature_vec = model.predict(
            row[image_tf_col],
            verbose=0,
        ).squeeze()  # Output shape: (512,)

        # Store vector and optional metadata
        row_data = {"cnn_vector": feature_vec}
        for col in keep_columns:
            row_data[col] = row[col]

        cnn_vectors.append(row_data)

    # Create DataFrame from extracted vectors
    df_vgg = pd.DataFrame(cnn_vectors)

    # Expand CNN vector into individual columns
    cnn_details = df_vgg["cnn_vector"].apply(
        lambda x: pd.Series(x) if x is not None else pd.Series([np.nan] * 512)
    )
    cnn_details.columns = [f"vgg16_{i}" for i in range(512)]

    # Add metadata columns if needed
    if keep_columns:
        cnn_details = pd.concat(
            [df_vgg[keep_columns], cnn_details],
            axis=1,
        )

    return cnn_details


def get_image_df(
    df: pd.DataFrame,
    color_mode: Optional[str] = None,
    image_name_col: str = "image",
    image_vec_col: str = "image_vec",
    root_dir: str = ".",
    resize_to: Optional[Tuple[int, int]] = (128, 128),
) -> pd.DataFrame:
    """
    Loads and preprocesses images listed in a DataFrame column into a new column as image arrays.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing image filenames.
    color_mode : str, optional
        Color mode to use: "grayscale", "rgb", or "rgba". Default is None (auto).
    image_name_col : str, optional
        Column name containing image file names (default: "image").
    image_vec_col : str, optional
        Name of the column to store the image vectors (default: "image_vec").
    root_dir : str, optional
        Root directory containing the image files (default: current directory).
    resize_to : tuple of int, optional
        Size to resize the images to (height, width). Default is (128, 128).

    Returns
    -------
    pd.DataFrame
        A DataFrame with a new column of loaded and resized image arrays,
        and without the original image filename column.

    Notes
    -----
    - Requires a function `load_and_resize_image()` to be defined externally.
    - Useful for transforming image paths into model-ready tensors or arrays.
    """
    image_df = df.copy()

    image_df[image_vec_col] = image_df[image_name_col].apply(
        lambda name: load_and_resize_image(
            name,
            root_dir=root_dir,
            resize_to=resize_to,
            color_mode=color_mode,
        )
    )

    return image_df.drop(columns=[image_name_col])


def get_image_orb_df(
    df: pd.DataFrame,
    image_vec_col: str = "image_vec",
    keep_columns: Optional[Sequence[str]] = None,
    nfeatures: int = 500,
) -> pd.DataFrame:
    """
    Extracts ORB (Oriented FAST and Rotated BRIEF) features from image arrays
    and flattens the result into a tabular format.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing image arrays in `image_vec_col`.
    image_vec_col : str, optional
        Name of the column containing image arrays (default: "image_vec").
    keep_columns : list of str, optional
        List of metadata columns to retain in the output (default: None).
    nfeatures : int, optional
        Number of keypoints to detect using ORB (default: 500).

    Returns
    -------
    pd.DataFrame
        A DataFrame with 32 ORB-based numeric features (`orb_0` to `orb_31`)
        and optionally the metadata columns.

    Notes
    -----
    - Assumes a function `extract_orb_features(image: np.ndarray, orb: cv2.ORB) -> np.ndarray`
      is defined and returns a 32-dimensional feature vector.
    - Works on grayscale or RGB images (OpenCV handles conversion internally).
    """
    orb_vectors = []
    keep_columns = keep_columns or []

    # Initialize ORB detector
    import cv2

    orb = cv2.ORB_create(nfeatures=nfeatures)

    # Process each row and extract features
    for _, row in df.iterrows():
        orb_vec = extract_orb_features(row[image_vec_col], orb=orb)

        row_data = {"orb_vector": orb_vec}
        for col in keep_columns:
            row_data[col] = row[col]

        orb_vectors.append(row_data)

    df_orb = pd.DataFrame(orb_vectors)

    # Expand the 32-dimensional ORB vector into separate columns
    orb_details = df_orb["orb_vector"].apply(
        lambda x: pd.Series(x) if x is not None else pd.Series([np.nan] * 32)
    )
    orb_details.columns = [f"orb_{i}" for i in range(32)]

    # Include metadata columns if requested
    if keep_columns:
        orb_details = pd.concat([df_orb[keep_columns], orb_details], axis=1)

    return orb_details


def get_image_resnet50_df(
    df: pd.DataFrame,
    image_col: str = "image",
    image_resnet50_col: str = "resnet50_img",
    root_dir: str = ".",
    target_size: Optional[Union[int, Tuple[int, int]]] = (224, 224),
) -> pd.DataFrame:
    """
    Loads and preprocesses images from a DataFrame column for use with ResNet50.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing image filenames.
    image_col : str, optional
        Name of the column containing image file names (default: "image").
    image_resnet50_col : str, optional
        Name of the output column to store processed image tensors (default: "resnet50_img").
    root_dir : str, optional
        Root directory where images are stored (default: current directory).
    target_size : int or tuple of int, optional
        Target size to resize images to (default: (224, 224)). Can also be a single int for square.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the processed ResNet50-compatible image tensors
        in a new column (`image_resnet50_col`), and without the original filename column.

    Notes
    -----
    - Assumes a function `load_and_preprocess_image_resnet50(filename, root_dir, target_size)`
      is available to load, resize and normalize the image as required by Keras ResNet50.
    """
    df_image = df.copy()

    df_image[image_resnet50_col] = df_image[image_col].apply(
        lambda name: load_and_preprocess_image_resnet50(
            name, root_dir=root_dir, target_size=target_size
        )
    )

    return df_image.drop(columns=[image_col])


def get_image_sift_df(
    df: pd.DataFrame,
    image_vec_col: str = "image_vec",
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Extracts SIFT (Scale-Invariant Feature Transform) descriptors from image arrays
    and expands them into individual columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing image arrays in `image_vec_col`.
    image_vec_col : str, optional
        Column name containing image arrays (default: "image_vec").
    keep_columns : list of str, optional
        List of metadata columns to retain in the output (default: None).

    Returns
    -------
    pd.DataFrame
        A DataFrame with one row per image and 128 SIFT features (`sift_0` to `sift_127`),
        along with optional metadata columns.

    Notes
    -----
    - Requires the external function `extract_sift_features(image: np.ndarray, sift: cv2.SIFT) -> np.ndarray`.
    - This version assumes the final feature vector returned by SIFT is already reduced to 128 dimensions
      (e.g., via averaging or PCA on descriptors).
    - Images should be preprocessed (resized, grayscale) before passing to this function.
    """
    sift_vectors = []
    keep_columns = keep_columns or []

    # Initialize SIFT detector
    import cv2

    sift = cv2.SIFT_create()

    # Extract SIFT features row by row
    for _, row in df.iterrows():
        sift_vec = extract_sift_features(row[image_vec_col], sift=sift)
        row_data = {"sift_vector": sift_vec}
        for col in keep_columns:
            row_data[col] = row[col]
        sift_vectors.append(row_data)

    df_sift = pd.DataFrame(sift_vectors)

    # Expand SIFT vector into separate columns
    sift_details = df_sift["sift_vector"].apply(
        lambda x: pd.Series(x) if x is not None else pd.Series([np.nan] * 128)
    )
    sift_details.columns = [f"sift_{i}" for i in range(128)]

    if keep_columns:
        sift_details = pd.concat([df_sift[keep_columns], sift_details], axis=1)

    return sift_details


def get_image_surf_df(
    df: pd.DataFrame,
    image_vec_col: str = "image_vec",
    hessianThreshold: int = 400,
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Extracts SURF (Speeded-Up Robust Features) descriptors from image arrays
    and returns a flattened DataFrame of SURF features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing image arrays in `image_vec_col`.
    image_vec_col : str, optional
        Name of the column containing image data (default: "image_vec").
    hessianThreshold : int, optional
        Threshold for SURF keypoint detection (default: 400).
    keep_columns : list of str, optional
        List of metadata columns to retain in the output (default: None).

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per image and SURF features (`surf_0`, ..., `surf_n`),
        plus optional metadata columns.

    Notes
    -----
    - Requires OpenCV contrib modules (`cv2.xfeatures2d.SURF_create`).
    - Assumes a function `extract_surf_features(image: np.ndarray, surf: cv2.SURF) -> np.ndarray`
      that reduces the SURF descriptors to a 1D feature vector (e.g., mean or PCA).
    """
    keep_columns = keep_columns or []
    surf_vectors = []

    # Initialize SURF extractor (requires opencv-contrib-python)
    import cv2

    surf = cv2.xfeatures2d.SURF_create(hessianThreshold=hessianThreshold)

    for _, row in df.iterrows():
        surf_vec = extract_surf_features(row[image_vec_col], surf=surf)
        row_data = {"surf_vector": surf_vec}
        for col in keep_columns:
            row_data[col] = row[col]
        surf_vectors.append(row_data)

    df_surf = pd.DataFrame(surf_vectors)

    # Determine vector dimension dynamically
    vector_dim = max([len(vec) for vec in df_surf["surf_vector"].dropna()] or [64])

    # Expand vector into individual columns
    surf_details = df_surf["surf_vector"].apply(
        lambda x: pd.Series(x) if x is not None else pd.Series([np.nan] * vector_dim)
    )
    surf_details.columns = [f"surf_{i}" for i in range(vector_dim)]

    # Append metadata columns if needed
    if keep_columns:
        surf_details = pd.concat([df_surf[keep_columns], surf_details], axis=1)

    return surf_details


def get_image_vgg16_df(
    df: pd.DataFrame,
    image_col: str = "image",
    image_vgg16_col: str = "vgg16_img",
    root_dir: str = ".",
    target_size: Optional[Union[int, Tuple[int, int]]] = (224, 224),
) -> pd.DataFrame:
    """
    Loads and preprocesses images from a DataFrame column for use with the VGG16 model.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing image file names.
    image_col : str, optional
        Name of the column in the DataFrame containing the image file names (default: "image").
    image_vgg16_col : str, optional
        Name of the output column that will contain the preprocessed image tensors (default: "vgg16_img").
    root_dir : str, optional
        Directory containing the image files (default: current directory).
    target_size : int or tuple of int, optional
        Target size for resizing the images. Either an integer (for square images)
        or a tuple (width, height). Default is (224, 224), which is required for VGG16.

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with the preprocessed VGG16-compatible images stored
        in a new column `image_vgg16_col`, and the original `image_col` dropped.

    Notes
    -----
    - Requires a preprocessing function `load_and_preprocess_image_vgg16()` to be defined,
      which should load, resize, normalize and return the image in the correct VGG16 format.
    """
    image_df = df.copy()

    image_df[image_vgg16_col] = image_df[image_col].apply(
        lambda name: load_and_preprocess_image_vgg16(
            name, root_dir=root_dir, target_size=target_size
        )
    )

    return image_df.drop(columns=[image_col])


def get_image_stats_df(
    df: pd.DataFrame,
    image_col: str = "image",
    root_dir: str = ".",
) -> pd.DataFrame:
    """
    Computes descriptive statistics (e.g., size, mode, color depth) for images listed in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing image file names or relative paths.
    image_col : str, optional
        Name of the column in `df` that contains image filenames (default: "image").
    root_dir : str, optional
        Path to the root directory containing the image files (default: current directory).

    Returns
    -------
    pd.DataFrame
        A new DataFrame with original content plus image statistics (e.g., width, height, format).

    Notes
    -----
    - Assumes a function `get_image_stats_from_path(image_name: str, root_dir: str)` is defined
      and returns a Series or dictionary of image statistics.
    - This function preserves the original DataFrame structure.
    """
    new_df = df.copy()

    # Partial function to include root_dir as a default argument
    get_image_stats_from_path_func = partial(
        get_image_stats_from_path,
        root_dir=root_dir,
    )

    # Apply stats extraction to each image
    df_stats = df[image_col].apply(get_image_stats_from_path_func)

    # Combine original data with computed stats
    return pd.concat([new_df, df_stats], axis=1)


def get_labels_df(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    suffix: str = "_encoded",
) -> pd.DataFrame:
    """
    Encodes specified categorical columns in a DataFrame using Label Encoding.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing categorical columns to encode.
    columns : list of str, optional
        List of column names to encode. If None, no encoding is performed.
    suffix : str, optional
        Suffix to add to the new encoded columns (default: "_encoded").

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with additional encoded columns.
        Original columns are left unchanged.

    Notes
    -----
    - Only columns with object dtype are encoded.
    - Columns that are not of type 'object' are silently skipped.
    - Uses `sklearn.preprocessing.LabelEncoder`.
    """
    tmp_df = df.copy()
    le = LabelEncoder()

    if columns is None:
        return tmp_df  # Nothing to encode

    for col in columns:
        if tmp_df[col].dtype != "object":
            continue
        tmp_df[col + suffix] = le.fit_transform(tmp_df[col].astype(str))

    return tmp_df


def get_predict_proba_df(
    model: ClassifierMixin,
    X: Union[pd.DataFrame, np.ndarray],
    y: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    label: int = 1,
) -> pd.DataFrame:
    """
    Constructs a DataFrame containing prediction results, including probability scores
    and classification types (true positive, false positive, etc.).

    Parameters
    ----------
    model : ClassifierMixin
        A trained classification model that implements `predict_proba`.
    X : pandas.DataFrame or numpy.ndarray
        Feature matrix used for prediction.
    y : pandas.Series or numpy.ndarray
        True labels.
    y_pred : pandas.Series or numpy.ndarray
        Predicted labels.
    label : int, optional
        Class label index for which to extract predicted probabilities (default: 1).

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the following columns:
        - "TARGET": actual class labels.
        - "prediction": predicted class labels.
        - "probality_score": predicted probability for the selected label.
        - "prediction_type": classification type ("TP", "FP", "FN", "TN", etc.).

    Notes
    -----
    - Assumes a helper function `get_prediction_type(pred, true)` is available to classify outcomes.
    - Can be useful for inspecting prediction confidence and building calibration plots.
    """
    predict_proba = model.predict_proba(X)[:, label]

    predict_proba_df = pd.DataFrame()
    predict_proba_df["TARGET"] = y.to_numpy()
    predict_proba_df["prediction"] = y_pred
    predict_proba_df["probality_score"] = predict_proba
    predict_proba_df["prediction_type"] = predict_proba_df.apply(
        lambda row: get_prediction_type(row["prediction"], row["TARGET"]), axis=1
    )

    return predict_proba_df


def get_metrics_df(
    model: RegressorMixin,
    X_train: Union[pd.DataFrame, np.ndarray],
    y_train: Union[pd.Series, np.ndarray],
    y_train_pred: Union[pd.Series, np.ndarray],
    X_test: Union[pd.DataFrame, np.ndarray],
    y_test: Union[pd.Series, np.ndarray],
    y_test_pred: Union[pd.Series, np.ndarray],
) -> pd.DataFrame:
    """
    Computes key regression metrics for training and testing sets.

    This function evaluates a model's performance on both training and testing sets
    and returns a summary DataFrame containing common regression metrics.

    Parameters
    ----------
    model : RegressorMixin
        A trained regression model implementing the `score` method.
    X_train : array-like
        Features used for training.
    y_train : array-like
        Ground truth labels for training.
    y_train_pred : array-like
        Predicted labels for the training set.
    X_test : array-like
        Features used for testing.
    y_test : array-like
        Ground truth labels for testing.
    y_test_pred : array-like
        Predicted labels for the testing set.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metrics for both Train and Test sets, including:
        - Model Score (R² by default)
        - Accuracy (for classification tasks)
        - RMSE
        - MAE
        - R² Score

    Notes
    -----
    - Accuracy is included, but only relevant for classification tasks.
    - RMSE is computed via a custom helper function.
    - All values are rounded to 2 decimal places.
    """
    metrics_dict = {
        "Accuracy": [
            round(accuracy_score(y_train, y_train_pred), 2),
            round(accuracy_score(y_test, y_test_pred), 2),
        ],
        "F1 Score": [
            round(f1_score(y_train, y_train_pred), 2),
            round(f1_score(y_test, y_test_pred), 2),
        ],
        "MAE": [
            round(mean_absolute_error(y_train, y_train_pred), 2),
            round(mean_absolute_error(y_test, y_test_pred), 2),
        ],
        "RMSE": [
            round(root_mean_squared_error(y_train, y_train_pred), 2),
            round(root_mean_squared_error(y_test, y_test_pred), 2),
        ],
        "R² Score": [
            round(r2_score(y_train, y_train_pred), 2),
            round(r2_score(y_test, y_test_pred), 2),
        ],
    }

    if hasattr(model, "score"):
        metrics_dict["Model Score"] = [
            round(model.score(X_train, y_train), 2),
            round(model.score(X_test, y_test), 2),
        ]

    return pd.DataFrame(metrics_dict, index=["Train", "Test"])


def get_prediction_type(prediction: int, target: int) -> str:
    """
    Determines the classification outcome type for a binary prediction.

    This function compares a predicted label and the true label (target)
    and returns a string indicating whether the result is:
    - true_positive
    - true_negative
    - false_positive
    - false_negative

    Parameters
    ----------
    prediction : int
        The predicted label (usually 0 or 1).
    target : int
        The true label (usually 0 or 1).

    Returns
    -------
    str
        A string indicating the prediction type:
        - "true_positive"
        - "true_negative"
        - "false_positive"
        - "false_negative"
        - "unknown" (in case of invalid input)

    Notes
    -----
    - This function assumes binary classification with values in {0, 1}.
    - It returns "unknown" if the inputs are not in expected form.
    """
    if prediction and target:
        return "true_positive"
    elif not prediction and not target:
        return "true_negative"
    elif prediction and not target:
        return "false_positive"
    elif not prediction and target:
        return "false_negative"
    else:
        return "unknown"


def get_stats(
    df: pd.DataFrame,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    missing_only: Optional[bool] = False,
    with_outliers: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Computes statistical summaries for numerical columns in a DataFrame.

    This function analyzes numerical columns and computes missing values,
    outlier statistics, and descriptive statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    ascending : bool, optional
        Whether to sort the output DataFrame in ascending order of missing values (default: True).
    columns : Sequence[str], optional
        A list of specific numerical columns to analyze. If not provided, all numerical columns are used.
    missing_only : bool, optional
        If True, only numerical columns with missing values are included in the output (default: False).
    with_outliers : bool, optional
        If True, calculates outlier statistics using the IQR method (default: False).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing:
        - Percentage of missing values.
        - (Optional) Outlier statistics.
        - (Optional) Descriptive statistics (min, max, mean, median, variance, etc.).

    Notes
    -----
    - Only numerical columns are analyzed (categorical columns are excluded).
    - If `missing_only=True`, columns without missing values are excluded.
    - If `with_outliers=True`, outliers are detected using the IQR method:
      * Lower bound = Q1 - 1.5 * IQR
      * Upper bound = Q3 + 1.5 * IQR
      * Counts of values below and above these bounds are recorded.
    - If `with_metrics=True`, additional statistics such as mean, variance, and skewness are included.
    - Results are sorted by percentage of missing values.
    """
    bound_lower_list = []
    bound_upper_list = []
    nb_outliers_list = []

    # Select only numerical columns
    num_df = df.drop(columns=df.select_dtypes(include=["object"]).columns)

    if missing_only:
        # Identify and drop columns without missing values
        num_df = num_df.drop(columns=num_df.columns[num_df.isna().sum() == 0])

    if columns is None:
        columns = num_df.columns

    # Compute outlier statistics if requested
    for col in columns:
        if with_outliers:
            q1 = num_df[col].quantile(0.25)
            q3 = num_df[col].quantile(0.75)
            iqr = q3 - q1

            _bound_lower = q1 - 1.5 * iqr
            _bound_upper = q3 + 1.5 * iqr

            _nb_of_lower = len(num_df[num_df[col] < _bound_lower])
            _nb_of_upper = len(num_df[num_df[col] > _bound_upper])

            bound_lower_list.append(_bound_lower)
            bound_upper_list.append(_bound_upper)
            nb_outliers_list.append(f"{_nb_of_lower} - {_nb_of_upper}")

    # Compute missing value percentages
    data = {
        "% Missing Values": round(
            (num_df[columns].isna().sum() / len(num_df)) * 100, 2
        ),
    }

    # Add outlier statistics if requested
    if with_outliers:
        data.update(
            {
                "Nb. Outliers": nb_outliers_list,
                "Lower Outlier Bound": bound_lower_list,
                "Upper Outlier Bound": bound_upper_list,
            }
        )

    # Compute descriptive statistics if requested
    data.update(
        {
            "% Null Values": round(
                (num_df[columns].eq(0).sum() / len(num_df)) * 100, 2
            ),
            "Minimum": num_df[columns].min(),
            "Maximum": num_df[columns].max(),
            "Mean": num_df[columns].mean(),
            "Median": num_df[columns].median(),
            "Mode": [num_df[c].mode()[0] for c in columns],
            "Variance": num_df[columns].var(),
            "Standard Deviation": num_df[columns].std(),
            "Skewness": num_df[columns].skew(),
            "Kurtosis": num_df[columns].kurtosis(),
        }
    )

    return pd.DataFrame(data).sort_values(by="% Missing Values", ascending=ascending)


def get_stats_missing(
    df: pd.DataFrame,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    missing_only: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Computes missing value statistics for categorical (object-type) columns in a DataFrame.

    This function analyzes categorical columns and computes the percentage of missing values.
    It can optionally exclude columns without missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.
    ascending : bool, optional
        Whether to sort the output DataFrame in ascending order of missing values (default: True).
    columns : Sequence[str], optional
        A list of specific categorical columns to analyze. If not provided, all categorical columns are used.
    missing_only : bool, optional
        If True, only categorical columns with missing values are included in the output (default: False).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing:
        - Percentage of missing values per categorical column.

    Notes
    -----
    - If `missing_only=True`, columns without missing values are excluded from the results.
    - Results are sorted by percentage of missing values.
    """
    # Select only categorical columns
    tmp_df = df.copy()

    if missing_only:
        # Identify columns without missing values and drop them
        tmp_df = tmp_df.drop(columns=tmp_df.columns[tmp_df.isna().sum() == 0])

    # Use specified columns or default to all remaining categorical columns
    if columns is None:
        columns = tmp_df.columns

    # Compute missing value percentages
    data = {
        "% Missing Values": round((tmp_df[columns].isna().sum() / len(tmp_df)) * 100, 2)
    }

    return pd.DataFrame(data).sort_values(by="% Missing Values", ascending=ascending)


def get_text_clean_n_common_words_df(
    df: pd.DataFrame,
    column: str = "corpus_text",
    new_column: str = "corpus_text_clean",
    n: int = 50,
) -> pd.DataFrame:
    """
    Removes the top `n` most frequent words from a text column and stores the result
    in a new column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the text data.
    column : str, optional
        Name of the column containing the raw text (default: "corpus_text").
    new_column : str, optional
        Name of the new column to store the cleaned text (default: "corpus_text_clean").
    n : int, optional
        Number of most frequent words to remove (default: 50).

    Returns
    -------
    pd.DataFrame
        The original DataFrame with an additional column containing the cleaned text.

    Notes
    -----
    - The function uses `nltk.tokenize.word_tokenize` and expects the texts to be in a tokenizable language.
    - Lowercasing is applied before token filtering.
    - Punctuation is not removed unless they are among the top frequent tokens.
    """
    from nltk.tokenize import word_tokenize

    clean_df = df.copy()

    # Tokenize all non-null texts to build a global frequency distribution
    all_tokens = []
    for text in clean_df[column].dropna():
        tokens = word_tokenize(text.lower())
        all_tokens.extend(tokens)

    freq_dist = Counter(all_tokens)
    top_n_words = set(word for word, _ in freq_dist.most_common(n))

    def clean_text(text: Optional[str]) -> str:
        if pd.isnull(text):
            return ""
        tokens = word_tokenize(text.lower())
        return " ".join([word for word in tokens if word not in top_n_words])

    clean_df[new_column] = clean_df[column].apply(clean_text)

    return clean_df


def get_text_bert_df(
    df: pd.DataFrame,
    model: Optional[Any] = None,  # type: ignore # Should be a SentenceTransformer model
    column: str = "corpus_text",
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Encodes a text column using a BERT-based SentenceTransformer model
    and returns a DataFrame with the resulting embeddings.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the text column to encode.
    model : SentenceTransformer, optional
        Pre-loaded SentenceTransformer model. If None, a default multilingual model is loaded.
    column : str, optional
        Name of the column in the DataFrame containing the texts to encode (default: "corpus_text").
    keep_columns : list of str, optional
        List of columns from the original DataFrame to retain alongside the embeddings.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing one row per input text and columns named `bert_0`, `bert_1`, ..., `bert_n`,
        with optional metadata columns from `keep_columns`.

    Notes
    -----
    - Requires the `sentence-transformers` library.
    - Texts are pre-filled with empty strings if missing.
    - If the model is not passed, it defaults to `"distiluse-base-multilingual-cased"`.
    """
    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("distiluse-base-multilingual-cased")

    texts = df[column].fillna("").tolist()

    vectors = model.encode(
        texts,
        show_progress_bar=False,
    )

    emb_df = pd.DataFrame(
        vectors,
        columns=[f"bert_{i}" for i in range(vectors.shape[1])],
    )

    if keep_columns:
        emb_df = pd.concat([df[keep_columns].reset_index(drop=True), emb_df], axis=1)

    return emb_df


def get_text_bow_df(
    df: pd.DataFrame,
    max_features: int = 1000,
    column: str = "corpus_text",
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Extracts Bag-of-Words (BoW) features from a text column of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the text data.
    max_features : int, optional
        Maximum number of words to include in the vocabulary (default: 1000).
    column : str, optional
        Name of the column containing the text to vectorize (default: "corpus_text").
    keep_columns : list of str, optional
        List of columns from the original DataFrame to retain in the output.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing BoW features with columns named `bow_<word>`, and optionally
        additional columns from the original DataFrame specified by `keep_columns`.

    Notes
    -----
    - Requires `scikit-learn` (CountVectorizer).
    - Uses raw word counts (no TF-IDF or normalization).
    """
    vectorizer = CountVectorizer(max_features=max_features)

    # Fit and transform text data
    X = vectorizer.fit_transform(df[column].fillna(""))

    # Create the BoW features DataFrame
    bow_df = pd.DataFrame(
        X.toarray(),
        columns=[f"bow_{w}" for w in vectorizer.get_feature_names_out()],
        index=df.index,  # to preserve alignment
    )

    # Append optional metadata columns
    if keep_columns:
        bow_df = pd.concat([df[keep_columns], bow_df], axis=1)

    return bow_df


def get_text_fasttext_df(
    df: pd.DataFrame,
    column: str = "corpus_text",
    model: Optional[Any] = None,  # type: ignore # Should be a gensim KeyedVectors model
    keep_columns: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Applies FastText embeddings to a text column of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the text data.
    column : str, optional
        Name of the column containing text to embed (default: "corpus_text").
    model : KeyedVectors, optional
        A pre-loaded FastText word vector model. If None, tries to load `cc.en.300.vec`.
    keep_columns : list of str, optional
        Columns from the original DataFrame to include in the result.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing FastText embeddings (columns `fasttext_0` to `fasttext_299`)
        along with the optional `keep_columns`.

    Notes
    -----
    - Requires a FastText model trained and available on disk.
    - Assumes you have implemented or imported `extract_fasttext_features(text, model)`.
    """
    if model is None:
        from gensim.models import KeyedVectors

        model = KeyedVectors.load_word2vec_format("cc.en.300.vec", binary=False)

    embeddings = []
    keep_columns = keep_columns or []

    for _, row in df.iterrows():
        vector = extract_fasttext_features(row[column], model)
        embeddings.append(
            {
                k: v
                for k, v in (
                    [("fasttext_vector", vector)] + [(c, row[c]) for c in keep_columns]
                )
            }
        )

    df_embed = pd.DataFrame(embeddings)

    # Expand vector into individual columns
    embed_expanded = df_embed["fasttext_vector"].apply(lambda x: pd.Series(x))
    embed_expanded.columns = [f"fasttext_{i}" for i in range(model.vector_size)]

    # Concatenate with selected metadata columns
    if keep_columns:
        embed_expanded = pd.concat([df_embed[keep_columns], embed_expanded], axis=1)

    return embed_expanded


def get_text_tfidf_df(
    df: pd.DataFrame,
    column: str = "corpus_text",
    keep_columns: Optional[Sequence[str]] = None,
    max_features: int = 1000,
) -> pd.DataFrame:
    """
    Extracts TF-IDF (Term Frequency-Inverse Document Frequency) features from a text column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the text data.
    max_features : int, optional
        Maximum number of features (terms) to keep in the vocabulary (default: 1000).
    column : str, optional
        Name of the column containing the text to vectorize (default: "corpus_text").
    keep_columns : list of str, optional
        List of additional columns from the original DataFrame to retain in the result.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing TF-IDF features with columns named `tfidf_<word>`,
        and optionally the selected columns from `keep_columns`.

    Notes
    -----
    - Requires `scikit-learn`.
    - Text is automatically lowercased and tokenized by the default TfidfVectorizer.
    - `NaN` values in the text column are not handled; fill them with empty strings beforehand if necessary.
    """
    vectorizer = TfidfVectorizer(max_features=max_features)

    # Vectorization (consider filling NaNs before if needed)
    X = vectorizer.fit_transform(df[column].fillna(""))

    tfidf_df = pd.DataFrame(
        X.toarray(),
        columns=[f"tfidf_{w}" for w in vectorizer.get_feature_names_out()],
        index=df.index,  # To preserve alignment with original df
    )

    # Optionally include additional columns
    if keep_columns:
        tfidf_df = pd.concat([df[keep_columns], tfidf_df], axis=1)

    return tfidf_df


def get_text_use_df(
    df: pd.DataFrame,
    model=None,
    column: str = "corpus_text",
    keep_columns: Optional[Sequence[str]] = None,
    model_url: str = "https://tfhub.dev/google/universal-sentence-encoder/4",
) -> pd.DataFrame:
    """
    Encodes text data using the Universal Sentence Encoder (USE) and returns a DataFrame of embeddings.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the text data.
    model : Optional, default=None
        Loaded USE model from TensorFlow Hub. If None, the model will be loaded from `model_url`.
    column : str, default="corpus_text"
        Column name in the DataFrame containing the text to encode.
    keep_columns : list of str, optional
        List of additional columns from the original DataFrame to include in the result.
    model_url : str, default="https://tfhub.dev/google/universal-sentence-encoder/4"
        URL to the Universal Sentence Encoder model on TensorFlow Hub.

    Returns
    -------
    pd.DataFrame
        DataFrame containing USE embeddings with column names `use_0` to `use_511`,
        along with any additional columns specified in `keep_columns`.

    Notes
    -----
    - Requires TensorFlow and TensorFlow Hub.
    - Make sure to run in an environment where the model can be downloaded if not already cached.
    """
    sentences = df[column].fillna("").tolist()

    if model is None:
        import tensorflow_hub as hub

        model = hub.load(model_url)

    embeddings = model(sentences).numpy()

    emb_df = pd.DataFrame(
        embeddings,
        columns=[f"use_{i}" for i in range(embeddings.shape[1])],
        index=df.index,  # conserve l’index initial
    )

    if keep_columns:
        emb_df = pd.concat([df[keep_columns], emb_df], axis=1)

    return emb_df


def impute_missing_values(
    df: pd.DataFrame,
    columns: Sequence[str],
    na_threshold: float = 0.1,
    imputer_cls: Type[SimpleImputer] = SimpleImputer,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Imputes missing values in selected columns of a DataFrame using a specified imputer.

    This function first removes rows where the percentage of missing values in a column
    exceeds a given threshold, then applies an imputer to fill the remaining missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and/or categorical data.
    columns : Sequence[str]
        The list of column names to be imputed.
    na_threshold : float, optional
        The maximum allowed percentage of missing values per column before
        dropping rows containing those missing values (default: 0.1, i.e., 10%).
    imputer_cls : Type[SimpleImputer], optional
        The imputer class to use for missing value imputation (default: `SimpleImputer`).
    **kwargs : Any
        Additional keyword arguments passed to the imputer's constructor.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the same column names as the original selection,
        but with missing values imputed.

    Notes
    -----
    - If a column has more than `na_threshold` fraction of missing values,
      all rows with missing values in that column are dropped before imputation.
    - The imputer is instantiated dynamically using `imputer_cls(**kwargs)`,
      allowing flexibility in choosing different imputation strategies.
    - The function returns a DataFrame with the same column names but without missing values.
    """
    # Create a new DataFrame with the selected columns
    tmp_df = df.copy()[columns]

    # Identify columns where NaN proportion exceeds the threshold
    na_columns = tmp_df.columns[tmp_df.isna().mean() > na_threshold]

    # Drop rows with NaN values in these columns
    tmp_df = tmp_df.dropna(subset=na_columns)

    # Impute missing values and return as a DataFrame with the same column names
    return pd.DataFrame(
        imputer_cls(**kwargs).fit_transform(tmp_df),
        columns=tmp_df.columns,
    )


def list_unique_modalities_by_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lists unique modalities (categories) for each categorical column in the DataFrame.

    This function inspects all columns of type 'object' or 'category' and returns a
    summary table listing the unique non-null values for each such column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and/or numerical variables.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns:
        - 'column': Name of the categorical column.
        - 'modalities': A comma-separated string of unique values (sorted).

    Notes
    -----
    - Null values are excluded from the modality list.
    - The values are converted to strings and sorted alphabetically.
    - Useful for exploring and auditing categorical variables.
    """
    cols = df.select_dtypes(include=["object", "category"]).columns
    summary = []

    for col in cols:
        values = sorted(df[col].dropna().unique())
        summary.append({"column": col, "modalities": ", ".join(map(str, values))})

    summary_df = pd.DataFrame(summary)

    if not summary:
        summary_df = pd.DataFrame(columns=["column", "modalities"])

    return summary_df.sort_values(by="column").set_index("column")


def sort_columns_by_filled_ratio(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Sorts a DataFrame's columns by the percentage of non-missing values.

    Columns with the highest proportion of filled values appear first.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns sorted by completeness (non-NaN ratio).
    """
    # Calculer le taux de remplissage (valeurs non NaN) pour chaque colonne
    ratio_filled = df.notna().mean()

    # Trier les colonnes par taux de remplissage décroissant
    columns_sorted_list = ratio_filled.sort_values(ascending=False).index

    # Réorganiser le DataFrame avec ces colonnes triées
    return df[columns_sorted_list]


def summarize_columns_by_prefix(
    df: pd.DataFrame, prefixes: Sequence[str]
) -> pd.DataFrame:
    """
    Summarizes columns in a DataFrame that start with given prefixes.

    This function scans all column names in the DataFrame and groups them
    by the specified prefixes, returning a summary of matching columns per prefix.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing column names to be analyzed.
    prefixes : Sequence[str]
        A list or sequence of string prefixes to match against column names.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns:
        - 'prefix': The prefix string being matched.
        - 'matching_columns': A comma-separated string of all matching column names.

    Notes
    -----
    - If no columns match a prefix, the 'matching_columns' field will be an empty string.
    - This is useful for exploring grouped variable sets (e.g., "EXT_SOURCE", "DAYS_", "FLAG_").
    """
    summary = []

    for prefix in prefixes:
        matching = [col for col in df.columns if col.startswith(prefix)]
        summary.append(
            {
                "prefix": prefix,
                "matching_columns": ", ".join(matching) if matching else "",
            }
        )

    return pd.DataFrame(summary).set_index("prefix")


def rank_feature_combinations_for_clustering(
    df: pd.DataFrame,
    features: List[str],
    min_comb_size: int = 3,
    n_clusters: int = 5,
    sample_size: int = 10000,
) -> pd.DataFrame:
    """
    Evaluates multiple feature combinations for clustering using KMeans
    and ranks them by Silhouette Score.

    This function tests various combinations of the given features, performs KMeans clustering
    on a random sample of the data, and computes clustering quality metrics. The combinations
    are ranked by the Silhouette Score.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset containing the features for clustering.
    features : list of str
        List of feature names to consider for combinations.
    min_comb_size : int, optional
        Minimum number of features per combination (default: 3).
    n_clusters : int, optional
        Number of clusters for the KMeans algorithm (default: 5).
    sample_size : int, optional
        Size of the random sample from the DataFrame for each combination (default: 10000).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the tested combinations and their clustering scores,
        sorted by Silhouette Score in descending order.

    Notes
    -----
    - Requires `get_cluster_labels()` and `get_clustering_metrics()` helper functions.
    - Automatically fills missing values with 0 (may affect clustering quality).
    - Can be slow depending on the number of combinations and sample size.
    """
    results = []

    features_sorted = sorted(features)
    unique_combinations = []
    for r in range(min_comb_size, len(features_sorted) + 1):
        unique_combinations.extend(combinations(features_sorted, r))

    print(f"{len(unique_combinations)} combinations generated.")

    for combo in tqdm(unique_combinations, desc="Evaluating combinations"):
        X = df[list(combo)].sample(n=sample_size, random_state=42).fillna(0)

        cluster_labels = get_cluster_labels(
            X,
            clustering_alg=KMeans,
            init="k-means++",
            n_clusters=n_clusters,
            n_init=10,
        )

        df_metrics = get_clustering_metrics(X, cluster_labels)

        results.append(
            {
                "Variables": combo,
                "Silhouette Score": df_metrics.loc["Silhouette Score", "Score"],
                "Calinski-Harabasz Index": df_metrics.loc[
                    "Calinski-Harabasz Index", "Score"
                ],
                "Davies-Bouldin Index": df_metrics.loc["Davies-Bouldin Index", "Score"],
            }
        )

    results_df = pd.DataFrame(results)
    results_df.sort_values(by="Silhouette Score", ascending=False, inplace=True)

    return results_df
