"""Data Objects module.

.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Prediction(BaseModel):
    """Class to describe a Prediction Object."""

    uuid: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    timestamp: int
    conf: Optional[float] = None

    def __str__(self) -> str:
        """Return a string representation of the object."""
        ts = datetime.fromtimestamp(self.timestamp)
        if self.lat is None or self.lng is None:
            return (
                f"\nuuid: {self.uuid}\nlast connection: {ts}\nprediction not successful"
            )
        else:
            return (
                f"\nuuid: {self.uuid}\nlast connection: {ts}\n"
                f"lat: {self.lat}  lng: {self.lng}\nconfidence: {self.conf}"
            )
