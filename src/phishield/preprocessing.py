"""Transformações aprendidas exclusivamente no treino de cada fold."""
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def pipeline_for(frame, model, scaled=False):
    categorical = list(frame.select_dtypes(exclude="number").columns)
    numeric = list(frame.select_dtypes(include="number").columns)
    steps = [("impute", SimpleImputer(strategy="median", keep_empty_features=True))]
    if scaled:
        steps.append(("scale", StandardScaler()))
    transformer = ColumnTransformer([
        ("num", Pipeline(steps), numeric),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="constant", fill_value="", keep_empty_features=True)),
            ("onehot", OneHotEncoder(handle_unknown="ignore", max_categories=16,
                                     sparse_output=False, dtype=np.float32)),
        ]), categorical),
    ])
    return Pipeline([("preparation", transformer), ("model", model)])
