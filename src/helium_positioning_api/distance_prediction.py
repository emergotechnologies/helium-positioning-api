"""Distance prediction module."""
import os
from typing import Any
from typing import Dict
from typing import List

import joblib
import pandas as pd
from dotenv import find_dotenv
from dotenv import load_dotenv


def predict_distance(model_selection: str, features: Dict[str, List[Any]]) -> float:
    """Return the predicted distance from the model.

    :param model_selection: The model object
    :param features: The features to predict the distance
    :return: The predicted distance
    """
    path = __get_model_path()
    preprocessor = joblib.load(path + "preprocessor.joblib")
    model = joblib.load(path + model_selection + ".joblib")
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
        model_path = "../models/"

    return model_path
