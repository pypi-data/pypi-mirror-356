import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def remap_cluster_labels(y_true, y_pred):
    conf_mat = confusion_matrix(y_true, y_pred)
    corresp = np.argmax(conf_mat, axis=0)

    labels = pd.Series(y_true, name="y_true").to_frame()
    labels["y_pred"] = y_pred
    labels["y_pred_transform"] = labels["y_pred"].apply(lambda x: corresp[x])

    return labels["y_pred_transform"]
