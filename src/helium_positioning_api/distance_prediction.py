"""Distance prediction module."""
import os
from typing import List

import joblib
from dotenv import find_dotenv
from dotenv import load_dotenv
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline


def predict_distance(model: str, features: List[float]) -> float:
    """Return the predicted distance from the model.

    :param model: The model object
    :param features: The features to predict the distance
    :return: The predicted distance
    """
    # preprocess features
    model = Pipeline(
        steps=[
            ("preprocessor", __get_preprocessor("preprocessor")), 
            ("estimator", __get_model(model)),
        ]
    )
    return model.predict(features)


def __get_model(model: str) -> BaseEstimator:
    """Return the model object from the path.

    :param model: The name of the model
    :return: The model object
    """
    path = __get_model_path() + model + ".joblib"
    loaded_model = joblib.load(path)
    return loaded_model


def __get_preprocessor(preprocessor: str) -> BaseEstimator:
    """Return the model object from the path.

    :param model: The name of the model
    :return: The model object
    """
    path = __get_model_path() + preprocessor + ".joblib"
    loaded_preprocessor = joblib.load(path)
    return loaded_preprocessor


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
