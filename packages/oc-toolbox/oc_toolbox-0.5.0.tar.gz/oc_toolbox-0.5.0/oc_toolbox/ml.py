import logging
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def business_cost(
    y: np.ndarray, y_pred: np.ndarray, cost_matrix: Optional[Dict[str, float]] = None
) -> float:
    """
    Computes the total business cost based on a user-defined cost matrix.

    This function calculates the number of true positives (TP), false positives (FP),
    true negatives (TN), and false negatives (FN), then applies the cost matrix
    to determine the overall cost of the model's predictions.

    Parameters
    ----------
    y : np.ndarray
        True binary labels.
    y_pred : np.ndarray
        Predicted binary labels.
    cost_matrix : dict, optional
        Dictionary specifying the cost associated with each prediction type:
        {"TP": float, "FP": float, "TN": float, "FN": float}.
        Default is {"TP": 0, "FP": 1, "TN": 0, "FN": 1}.

    Returns
    -------
    float
        The total business cost of the model's predictions.

    Notes
    -----
    - Useful for modeling scenarios where misclassifications have different consequences.
    - Can be used for cost-sensitive learning or model evaluation.
    """
    if cost_matrix is None:
        cost_matrix = {"TP": 0, "FP": 1, "TN": 0, "FN": 1}

    TP = np.sum((y_pred == 1) & (y == 1))
    FP = np.sum((y_pred == 1) & (y == 0))
    TN = np.sum((y_pred == 0) & (y == 0))
    FN = np.sum((y_pred == 0) & (y == 1))

    total_cost = (
        TP * cost_matrix["TP"]
        + FP * cost_matrix["FP"]
        + TN * cost_matrix["TN"]
        + FN * cost_matrix["FN"]
    )

    return total_cost


def create_cnn_model(
    cnn_model: Optional[str] = "ResNet50",
    data_augmented: Optional[bool] = False,
    density: Optional[int] = 1024,
    dropout: Optional[float] = 0.5,
    input_size: Optional[Tuple[int, int]] = (224, 224),
    num_classes: Optional[int] = 4,
    optimizer: Optional[str] = "adam",
    trainable: Optional[bool] = False,
) -> Any:
    """
    Creates and compiles a CNN model using a pretrained backbone (VGG16 or ResNet50).

    Parameters
    ----------
    cnn_model : str, optional
        Name of the base CNN architecture to use. Must be "VGG16" or "ResNet50". Default is "ResNet50".
    data_augmented : bool, optional
        Whether to include data augmentation layers. Default is False.
    density : int, optional
        Number of neurons in the dense hidden layer. Default is 1024.
    dropout : float, optional
        Dropout rate after the dense layer. Default is 0.5.
    input_size : tuple of int, optional
        Input image size (height, width). Default is (224, 224).
    num_classes : int, optional
        Number of output classes. Default is 4.
    optimizer : str, optional
        Optimizer to use during compilation. Default is "adam".
    trainable : bool, optional
        Whether to make the pretrained CNN layers trainable. Default is False.

    Returns
    -------
    keras.Model
        A compiled Keras CNN model ready for training.
    """
    from tensorflow.keras import layers
    from tensorflow.keras.models import Sequential

    layers_list = []

    # Add data augmentation layers if needed
    if data_augmented:
        layers_list += [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.1, 0.1),
            layers.RandomContrast(0.1),
        ]

    # Choose base model
    if cnn_model == "VGG16":
        from tensorflow.keras.applications.vgg16 import VGG16

        base_model_cls = VGG16
    elif cnn_model == "ResNet50":
        from tensorflow.keras.applications.resnet50 import ResNet50

        base_model_cls = ResNet50
    else:
        raise ValueError(
            f"Unknown CNN model: {cnn_model}. Supported models are 'VGG16' and 'ResNet50'."
        )

    base_model = base_model_cls(
        include_top=False,
        input_shape=(input_size[0], input_size[1], 3),
        weights="imagenet",
    )

    # Set trainability of the base model
    for layer in base_model.layers:
        layer.trainable = trainable

    # Add base model and classifier layers
    layers_list += [
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(density, activation="relu"),
        layers.Dropout(dropout),
        layers.Dense(num_classes, activation="softmax"),
    ]

    # Build and compile model
    model = Sequential(layers_list)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"],
    )

    return model


def log_to_mlflow(
    model,
    X,
    y_pred,
    artifacts: Optional[List[Tuple[str, str]]] = None,
    artifact_path: str = "new_model",
    experiment: str = "Default",
    images: Optional[List[Tuple[Any, str]]] = None,
    metrics: Optional[Dict[str, float]] = None,
    model_kind: str = "sklearn",
    model_name: str = "New model",
    name: str = "New run",
    params: Optional[Dict[str, Any]] = None,
    tables: Optional[List[Tuple[Any, str]]] = None,
    tags: Optional[Dict[str, str]] = None,
    uri: str = "http://127.0.0.1:5000",
):
    """
    Logs a machine learning model and associated metadata to MLflow.

    Parameters
    ----------
    model : Any
        The trained model to log.
    X : Any
        Input data used for prediction (for signature inference).
    y_pred : Any
        Model predictions used for signature inference.
    artifacts : list of (str, str), optional
        List of (local_dir, artifact_path) to log as extra artifacts.
    artifact_path : str, optional
        Path where the model artifact will be stored.
    experiment : str, optional
        Name of the MLflow experiment to use.
    images : list of (image, str), optional
        Images to log (image object, filename).
    metrics : dict, optional
        Metrics to log.
    model_kind : str, optional
        Type of model: 'sklearn', 'keras', or 'transformers'.
    model_name : str, optional
        Registered model name in the MLflow model registry.
    name : str, optional
        Name of the MLflow run.
    params : dict, optional
        Parameters to log.
    tables : list of (DataFrame, str), optional
        DataFrames to log as tables (e.g. results, samples).
    tags : dict, optional
        Tags to associate with the run.
    uri : str, optional
        MLflow tracking server URI.

    Returns
    -------
    None
    """
    import mlflow
    from mlflow.models import infer_signature

    # Silence MLflow internal logs
    logger = logging.getLogger("mlflow")
    logger.setLevel(logging.ERROR)

    # Set MLflow tracking server URI
    mlflow.set_tracking_uri(uri=uri)

    # Set or create experiment
    mlflow.set_experiment(experiment)

    # Start logging run
    with mlflow.start_run(run_name=name, nested=True):
        # Log any provided images
        for img, path in images or []:
            mlflow.log_image(img, path)

        # Log evaluation metrics
        mlflow.log_metrics(metrics or {})

        # Log training parameters
        mlflow.log_params(params or {})

        # Log additional DataFrames
        for tab, tab_name in tables or []:
            mlflow.log_table(tab, f"{tab_name}.json")

        # Add metadata tags
        mlflow.set_tags(tags or {})

        # Infer model signature
        signature = infer_signature(X, y_pred)

        # Prepare common logging arguments
        log_model_args = {
            "artifact_path": artifact_path,
            "signature": signature,
            "input_example": None,
            "registered_model_name": model_name,
        }

        # Log the model according to its type
        if model_kind == "sklearn":
            mlflow.sklearn.log_model(model, **log_model_args)
        elif model_kind == "keras":
            mlflow.keras.log_model(model, **log_model_args)
        elif model_kind == "transformers":
            mlflow.transformers.log_model(model, **log_model_args)
        else:
            raise ValueError(f"Unsupported model kind: {model_kind}")

        # Log extra artifacts
        for local_dir, art_path in artifacts or []:
            mlflow.log_artifact(local_dir, artifact_path=art_path)


class PandasStandardScaler(TransformerMixin):
    """
    A wrapper around StandardScaler that returns a pandas DataFrame
    with preserved column names after scaling.

    This transformer behaves like scikit-learn's StandardScaler, but ensures
    that the output remains a pandas DataFrame with the same column names.

    Parameters
    ----------
    **kwargs : dict
        Additional keyword arguments passed to `sklearn.preprocessing.StandardScaler`.

    Attributes
    ----------
    scaler : StandardScaler
        The underlying scikit-learn scaler.
    feature_names : pd.Index
        The feature names extracted from the input DataFrame.
    is_fitted_ : bool
        Flag indicating whether the scaler has been fitted.
    """

    def __init__(self, **kwargs):
        self.scaler = StandardScaler(**kwargs)

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> "PandasStandardScaler":
        """
        Fits the scaler to the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            The input features to scale.
        y : pd.Series, optional
            Not used. Included for compatibility.

        Returns
        -------
        PandasStandardScaler
            The fitted scaler instance.
        """
        self.scaler.fit(X)
        self.feature_names = X.columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input DataFrame using the fitted scaler.

        Parameters
        ----------
        X : pd.DataFrame
            The input features to transform.

        Returns
        -------
        pd.DataFrame
            A DataFrame of scaled values with the original column names.
        """
        X_scaled = self.scaler.transform(X)
        return pd.DataFrame(X_scaled, columns=self.feature_names, index=X.index)


class NumericSelector(BaseEstimator, TransformerMixin):
    """
    Transformer that selects only numeric columns from a pandas DataFrame.

    This transformer can be used in a preprocessing pipeline to isolate
    numerical features before applying numerical-specific transformations
    such as scaling or imputation.

    Attributes
    ----------
    numeric_columns : pd.Index
        The names of the numeric columns selected during fitting.
    is_fitted_ : bool
        Indicates whether the transformer has been fitted.
    """

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None, **kwargs
    ) -> "NumericSelector":
        """
        Identifies numeric columns in the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame.
        y : pd.Series, optional
            Not used. Included for compatibility with pipelines.
        **kwargs : dict
            Additional arguments (ignored).

        Returns
        -------
        NumericSelector
            The fitted transformer.
        """
        self.numeric_columns = X.select_dtypes(include=[np.number]).columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Transforms the input DataFrame by selecting only numeric columns.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame to transform.
        y : pd.Series, optional
            Not used. Included for compatibility with pipelines.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing only the numeric columns.
        """
        return X[self.numeric_columns]


class PandasSimpleImputer(TransformerMixin):
    """
    Wrapper around scikit-learn's SimpleImputer that preserves pandas column names.

    This transformer applies simple imputation (mean, median, most frequent, or constant)
    to missing values and returns a DataFrame instead of a NumPy array, retaining
    the original column names.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments passed to `sklearn.impute.SimpleImputer`.

    Attributes
    ----------
    imputer : SimpleImputer
        The underlying SimpleImputer instance.
    feature_names : pd.Index
        Column names of the input DataFrame.
    is_fitted_ : bool
        Indicates whether the imputer has been fitted.
    """

    def __init__(self, **kwargs):
        self.imputer = SimpleImputer(**kwargs)

    def fit(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> "PandasSimpleImputer":
        """
        Fits the SimpleImputer to the input DataFrame.

        Parameters
        ----------
        X : pd.DataFrame
            Input features with possible missing values.
        y : pd.Series, optional
            Not used. Included for pipeline compatibility.

        Returns
        -------
        PandasSimpleImputer
            The fitted imputer.
        """
        self.imputer.fit(X)
        self.feature_names = X.columns
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input DataFrame by imputing missing values.

        Parameters
        ----------
        X : pd.DataFrame
            Input features to transform.

        Returns
        -------
        pd.DataFrame
            A new DataFrame with imputed values and original column names.
        """
        X_imputed = self.imputer.transform(X)
        return pd.DataFrame(X_imputed, columns=self.feature_names, index=X.index)


class ThresholdClassifier(BaseEstimator, ClassifierMixin):
    """
    Wrapper classifier that applies a custom decision threshold on the predicted probabilities.

    This meta-classifier wraps a base binary classifier and overrides its default threshold
    of 0.5 for classifying instances. It is useful when optimizing for business constraints
    such as precision, recall, or cost-based decisions.

    Parameters
    ----------
    base_model : ClassifierMixin
        A fitted scikit-learn compatible binary classifier with a `predict_proba` method.
    threshold : float, optional
        The probability threshold to classify instances as positive (default is 0.5).

    Attributes
    ----------
    is_fitted_ : bool
        Indicates whether the model has been fitted.
    """

    def __init__(
        self, base_model: Optional[ClassifierMixin] = None, threshold: float = 0.5
    ):
        self.base_model = base_model
        self.threshold = threshold

    def fit(self, X, y=None):
        """
        Fits the base model to the training data.

        Parameters
        ----------
        X : array-like
            Training features.
        y : array-like
            Target labels.

        Returns
        -------
        self : ThresholdClassifier
            The fitted classifier.
        """
        self.base_model.fit(X, y)
        self.is_fitted_ = True
        return self

    def predict(self, X) -> np.ndarray:
        """
        Predicts binary class labels using the custom threshold.

        Parameters
        ----------
        X : array-like
            Input features to classify.

        Returns
        -------
        numpy.ndarray
            Binary predictions (0 or 1) based on the specified threshold.
        """
        proba = self.base_model.predict_proba(X)[:, 1]
        return (proba >= self.threshold).astype(int)

    def predict_proba(self, X) -> np.ndarray:
        """
        Returns predicted probabilities from the base model.

        Parameters
        ----------
        X : array-like
            Input features.

        Returns
        -------
        numpy.ndarray
            Probabilities for both classes (shape: [n_samples, 2]).
        """
        return self.base_model.predict_proba(X)

    def get_params(self, deep: bool = True) -> dict:
        """
        Returns parameters for this estimator.

        Parameters
        ----------
        deep : bool, optional
            Whether to return parameters of nested objects (default: True).

        Returns
        -------
        dict
            Parameters of the classifier.
        """
        return {"base_model": self.base_model, "threshold": self.threshold}

    def set_params(self, **params):
        """
        Sets parameters for this estimator.

        Parameters
        ----------
        **params : dict
            Parameter names mapped to their new values.

        Returns
        -------
        self : ThresholdClassifier
            The updated classifier.
        """
        for param, value in params.items():
            setattr(self, param, value)
        return self
