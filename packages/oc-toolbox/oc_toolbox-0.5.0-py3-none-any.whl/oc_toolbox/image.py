import os
from typing import Any, Optional, Tuple

import numpy as np
import pandas as pd
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # disables the warning


def extract_orb_features(
    img: np.ndarray,
    nfeatures: int = 500,
    orb: Optional[Any] = None,  # type: ignore # cv2.ORB is not imported here to avoid circular import issues
) -> Optional[np.ndarray]:
    """
    Extracts ORB (Oriented FAST and Rotated BRIEF) features from an image and returns the mean descriptor vector.

    Parameters
    ----------
    img : np.ndarray
        Input image as a NumPy array.
    nfeatures : int, optional
        Maximum number of features to retain (default: 500).
    orb : cv2.ORB, optional
        Preconfigured ORB object. If None, a new ORB instance is created.

    Returns
    -------
    np.ndarray or None
        A 32-dimensional feature vector representing the mean of the ORB descriptors,
        or None if no descriptors are found.
    """
    if orb is None:
        import cv2

        orb = cv2.ORB_create(nfeatures=nfeatures)

    _, descriptors = orb.detectAndCompute(img, None)

    if descriptors is None or len(descriptors) == 0:
        return None

    # Return mean descriptor (converted to float64)
    return descriptors.mean(axis=0)


def extract_sift_features(
    img: np.ndarray,
    sift: Optional[Any] = None,  # type: ignore # cv2.SIFT is not imported here to avoid circular import issues
) -> Optional[np.ndarray]:
    """
    Extracts SIFT (Scale-Invariant Feature Transform) features from an image and returns the mean descriptor vector.

    Parameters
    ----------
    img : np.ndarray
        Input image as a NumPy array (typically grayscale or BGR).
    sift : Optional[cv2.SIFT], default=None
        Pre-initialized SIFT extractor. If None, a new instance is created.

    Returns
    -------
    Optional[np.ndarray]
        A 128-dimensional feature vector representing the mean of the SIFT descriptors,
        or None if no descriptors are found.

    Notes
    -----
    - Requires OpenCV with SIFT enabled (non-free module).
    - Output is a float64 vector.
    """
    import cv2

    if sift is None:
        sift = cv2.SIFT_create()

    _, descriptors = sift.detectAndCompute(img, None)

    if descriptors is None or len(descriptors) == 0:
        return None

    return descriptors.mean(axis=0)


def extract_surf_features(
    img: np.ndarray,
    hessianThreshold: int = 400,
    surf: Optional[Any] = None,  # type: ignore # cv2.xfeatures2d.SURF is not imported here to avoid circular import issues
) -> Optional[np.ndarray]:
    """
    Extracts SURF (Speeded-Up Robust Features) descriptors from an image and returns their mean vector.

    Parameters
    ----------
    img : np.ndarray
        Input image as a NumPy array.
    hessianThreshold : int, default=400
        Threshold for the Hessian keypoint detector. Higher values reduce the number of keypoints detected.
    surf : Optional[cv2.xfeatures2d.SURF], default=None
        Pre-configured SURF extractor. If None, a new instance is created using the given hessianThreshold.

    Returns
    -------
    Optional[np.ndarray]
        A feature vector (typically 64 or 128 dimensions, float64) representing the mean of the SURF descriptors,
        or None if no descriptors are found.

    Notes
    -----
    - Requires OpenCV with the `xfeatures2d` module (contrib).
    - The number of descriptor dimensions depends on the SURF configuration (default: 64).
    """
    import cv2

    if surf is None:
        surf = cv2.xfeatures2d.SURF_create(hessianThreshold=hessianThreshold)

    _, descriptors = surf.detectAndCompute(img, None)

    if descriptors is None or len(descriptors) == 0:
        return None

    return descriptors.mean(axis=0)


def get_image_stats_from_path(
    name: str,
    root_dir: str = ".",
) -> pd.Series:
    """
    Extracts basic statistics from a grayscale image located at a given path.

    Parameters
    ----------
    name : str
        Image file name (relative to `root_dir`).
    root_dir : str, default="."
        Directory where the image is stored.

    Returns
    -------
    pd.Series
        A series containing the following statistics:
        - height (int): Image height in pixels.
        - width (int): Image width in pixels.
        - aspect_ratio (float): Width / Height.
        - mean_intensity (float): Mean pixel intensity.
        - std_intensity (float): Standard deviation of pixel intensities.
        - non_zero_ratio (float): Ratio of non-zero pixels to total pixels.
        - is_valid (bool): True if image is readable and non-empty, else False.
    """
    path = os.path.join(root_dir, name)

    if not os.path.exists(path):
        return pd.Series(
            {
                "height": 0,
                "width": 0,
                "aspect_ratio": 0,
                "mean_intensity": 0,
                "std_intensity": 0,
                "non_zero_ratio": 0,
                "is_valid": False,
            }
        )

    import cv2

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return pd.Series(
            {
                "height": 0,
                "width": 0,
                "aspect_ratio": 0,
                "mean_intensity": 0,
                "std_intensity": 0,
                "non_zero_ratio": 0,
                "is_valid": False,
            }
        )

    h, w = img.shape

    return pd.Series(
        {
            "height": h,
            "width": w,
            "aspect_ratio": w / h if h else 0,
            "mean_intensity": float(np.mean(img)),
            "std_intensity": float(np.std(img)),
            "non_zero_ratio": float(np.count_nonzero(img) / (h * w)),
            "is_valid": True,
        }
    )


def load_and_preprocess_image_resnet50(
    name: str,
    root_dir: str = ".",
    target_size: Optional[Tuple[int, int]] = (224, 224),
) -> Optional[np.ndarray]:
    """
    Load and preprocess an image for ResNet50 input.

    Parameters
    ----------
    name : str
        File name of the image to load.
    root_dir : str, default="."
        Directory path where the image is located.
    target_size : tuple of int, optional
        Desired image size (height, width) for the model input. Default is (224, 224).

    Returns
    -------
    np.ndarray or None
        Preprocessed image as a NumPy array with shape (1, height, width, 3),
        or None if the image file does not exist.
    """
    path = os.path.join(root_dir, name)

    if not os.path.exists(path):
        return None

    from tensorflow.keras.applications.resnet50 import preprocess_input
    from tensorflow.keras.preprocessing import image

    img = image.load_img(path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    return preprocess_input(img_array)


def load_and_preprocess_image_vgg16(
    name: str,
    root_dir: str = ".",
    target_size: Optional[Tuple[int, int]] = (224, 224),
) -> Optional[np.ndarray]:
    """
    Load and preprocess an image for VGG16 input.

    Parameters
    ----------
    name : str
        File name of the image to load.
    root_dir : str, default="."
        Directory where the image file is stored.
    target_size : tuple of int, optional
        Desired image size (height, width) for the model input. Default is (224, 224).

    Returns
    -------
    np.ndarray or None
        Preprocessed image as a NumPy array with shape (1, height, width, 3),
        or None if the image file does not exist.
    """
    path = os.path.join(root_dir, name)

    if not os.path.exists(path):
        return None

    from tensorflow.keras.applications.vgg16 import preprocess_input
    from tensorflow.keras.preprocessing import image

    img = image.load_img(path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    return preprocess_input(img_array)


def load_and_resize_image(
    name: str,
    color_mode: Optional[str] = None,
    root_dir: str = ".",
    resize_to: Optional[Tuple[int, int]] = (128, 128),
) -> Optional[np.ndarray]:
    """
    Load an image from a given path, convert it to grayscale if specified,
    and resize it to the given dimensions.

    Parameters
    ----------
    name : str
        Name of the image file.
    color_mode : str, optional
        If "gray" or "grayscale", the image is loaded in grayscale mode.
        Otherwise, the image is loaded in color (BGR).
    root_dir : str, default="."
        Root directory where the image file is located.
    resize_to : tuple of int, optional
        Target size for resizing the image, in (height, width) format.
        If None, the image is not resized.

    Returns
    -------
    np.ndarray or None
        The loaded and resized image as a NumPy array, or None if the file
        could not be read.
    """
    import cv2

    path = os.path.join(root_dir, name)

    if not os.path.exists(path):
        return None

    if color_mode in ["gray", "grayscale"]:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path)

    if img is None:
        return None

    if resize_to is not None:
        img = cv2.resize(
            img,
            (resize_to[1], resize_to[0]),  # OpenCV uses (width, height)
        )

    return img
