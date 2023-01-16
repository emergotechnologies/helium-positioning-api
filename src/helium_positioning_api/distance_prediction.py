"""
some doc string
"""

from typing import Any
from typing import List

import joblib
import pickle


def get_model(path: str) -> Any:
    """Return the model object from the path."""
    # todo check model file type and leave one of the lines
    loaded_model = joblib.load(path)
    loaded_model = pickle.load(open(path, 'rb'))
    return loaded_model


def predict_distance(model: Any, features: List[Any]) -> float:
    """Return the predicted distance from the model."""
    # preprocess features
    return model.predict(features)
