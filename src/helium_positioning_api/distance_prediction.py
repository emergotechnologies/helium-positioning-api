"""
some doc string
"""

from typing import List

import joblib
import pickle

from sklearn.base import BaseEstimator


def get_model(path: str) -> BaseEstimator:
    """Return the model object from the path."""
    # todo check model file type and leave one of the lines
    loaded_model = joblib.load(path)
    loaded_model = pickle.load(open(path, 'rb'))
    return loaded_model


def predict_distance(model: BaseEstimator, features: List[float]) -> float:
    """Return the predicted distance from the model."""
    # preprocess features
    return model.predict(features)
