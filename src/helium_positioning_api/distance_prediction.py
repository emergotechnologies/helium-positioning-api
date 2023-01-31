"""Distance prediction module."""
import os
from typing import List, Union, Dict

import joblib
import pandas as pd
from dotenv import find_dotenv
from dotenv import load_dotenv
from sklearn.base import RegressorMixin, MultiOutputMixin
from sklearn.compose import ColumnTransformer


def predict_distance(model: str, features: Dict[str, List]) -> float:
    """Return the predicted distance from the model.

    :param model: The model object
    :param features: The features to predict the distance
    :return: The predicted distance
    """
    # preprocess features
    path = __get_model_path()
    preprocessor = joblib.load(path + "preprocessor.joblib")
    model = joblib.load(path + model + ".joblib")
    data = pd.DataFrame(features)
    y = preprocessor.transform(data)
    return model.predict(y)


def __get_model_path() -> str:
    """Return the path to the model.

    :return: The path to the model
    """
    if not (dotenv_path := find_dotenv()):
        dotenv_path = find_dotenv(usecwd=True)

    load_dotenv(dotenv_path)
    model_path = os.getenv("MODEL_PATH")

    if not model_path:
        model_path = "./models/"

    return model_path
