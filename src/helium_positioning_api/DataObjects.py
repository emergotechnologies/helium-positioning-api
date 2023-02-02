"""Data Objects module.

.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from typing import Optional

from pydantic import BaseModel


class Prediction(BaseModel):
    """Class to describe a Prediction Object."""

    uuid: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    # timestamp: int
    conf: Optional[float] = None

    def __str__(self) -> str:
        """Return a string representation of the object."""
        if self.lat is None or self.lng is None:
            return f"\nuuid: {self.uuid}\nprediction not successful"
        else:
            return f"\nuuid: {self.uuid}\nlat: {self.lat}\nlng: {self.lng}\nconfidence: {self.conf}"
