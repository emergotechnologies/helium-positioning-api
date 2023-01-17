"""Data Objects module.

.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from datetime import datetime
from typing import Optional

from helium_api_wrapper.hotspots import get_hotspot_by_address
from pydantic import BaseModel


class Prediction(BaseModel):
    """Class to describe a Prediction Object."""

    uuid: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    timestamp: datetime
    conf: Optional[float] = None

    def __str__(self) -> str:
        """Return a string representation of the object."""
        if self.lat and self.lng:
            return (
                f"\nuuid: {self.uuid}\nlast connection: {self.timestamp.isoformat()}\n"
                f"lat: {self.lat}  lng: {self.lng}\nconfidence: {self.conf}"
            )
        else:
            return f"\nuuid: {self.uuid}\nlast connection: {self.timestamp.isoformat()}\nprediction not successful"


class Hotspot(BaseModel):
    """Hotspots which received the same packet.

    :param frequency: In MHz, the frequency which the packet was received upon.
    :type frequency: float

    :param id: A base58 encoding of the hotspot's public key.
    :type id: str

    :param name: human-friendly three-word alias of the hotspot's public key.
    :type name: str

    :param reported_at: Timestamp in milliseconds
    :type reported_at: int

    :param rssi: Received Signal Strength Indicator is reported\
        by the hotspot and indicates how strong the signal device's \
        radio signal was
    :type rssi: float

    :param snr: In dB, Signal to Noise Ratio is reported by the\
        hotspot to indicate how clear the signal was relative \
        to environmental noise
    :type snr: float

    :param spreading: LoRa Spreading Factor and Bandwidth \
        used for the radio transmission.
    :type spreading: str

    """

    frequency: float
    id: str
    name: str
    reported_at: datetime
    rssi: float
    snr: float
    spreading: str
    lat: float
    long: float

    def load_location(self) -> None:
        """Assign latitude and longitude to the object \
            from the data in Hotspots object."""
        if not self.lat or not self.long:
            hotspot = get_hotspot_by_address(self.id)
            self.lat = hotspot[0].lat
            self.long = hotspot[0].lng
