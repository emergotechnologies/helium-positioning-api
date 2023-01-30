"""Result Handler.

.. module:: ResultHandler

:synopsis: Functions to export the data from Helium API to a file

.. moduleauthor:: DSIA21

"""

import logging
import os
from typing import Generator
from typing import List
from typing import Union

import pandas as pd
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def write(
    data: Union[List[BaseModel], Generator[BaseModel, None, None]],
    path: str,
    file_name: str,
    file_format: str,
) -> None:
    """Write the data to a file."""
    parsed_data = pd.DataFrame([x.dict() for x in data])
    os.makedirs(path, exist_ok=True)
    if file_format == "csv":
        __write_csv(parsed_data, path, file_name)
    elif file_format == "json":
        __write_json(parsed_data, path, file_name)
    elif file_format == "pickle":
        __write_pickle(parsed_data, path, file_name)
    elif file_format == "feather":
        __write_feather(parsed_data, path, file_name)
    elif file_format == "parquet":
        __write_parquet(parsed_data, path, file_name)
    else:
        logger.error(f"File format {file_format} not supported.")
    logger.info(f"File {file_name} saved to {path}")


def __write_csv(data: pd.DataFrame, path: str, file_name: str) -> None:
    """Write the data to a csv file."""
    data.to_csv(os.path.join(path, file_name + ".csv"))


def __write_json(data: pd.DataFrame, path: str, file_name: str) -> None:
    """Write the data to a json file."""
    data.to_json(os.path.join(path, file_name + ".json"), orient="records")


def __write_pickle(data: pd.DataFrame, path: str, file_name: str) -> None:
    """Write the data to a pickle file."""
    data.to_pickle(os.path.join(path, file_name + ".pkl"))


def __write_feather(data: pd.DataFrame, path: str, file_name: str) -> None:
    """Write the data to a feather file."""
    data.to_feather(os.path.join(path, file_name + ".feather"))


def __write_parquet(data: pd.DataFrame, path: str, file_name: str) -> None:
    """Write the data to a parquet file."""
    data.to_parquet(os.path.join(path, file_name + ".parquet"))
