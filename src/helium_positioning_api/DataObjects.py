from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from helium_api_wrapper.helpers import load_hotspot
from pydantic import BaseModel


class DataObject(BaseModel):
    """Base class for all data objects."""

    def __len__(self):
        return dict(self).__len__()

    def __getitem__(self, item):
        return getattr(self, item)

    def as_dict(self, columns: Optional[List[str]] = None):
        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data


class Prediction(DataObject):
    """Class to describe a Prediction Object."""

    uuid: str
    lat: float
    lng: float
    timestamp: datetime
    conf: float = None

    def __str__(self):
        return f"\nuuid: {self.uuid}\nlast connection: {self.timestamp.isoformat()}\nlat: {self.lat}  lng: {self.lng}"


class Hotspot(DataObject):
    """Hotspots which received the same packet.

    :param frequency: In MHz, the frequency which the packet was received upon.
    :type frequency: float

    :param id: A base58 encoding of the hotspot's public key.
    :type id: str

    :param name: A human-friendly three-word encoding of the hotspot's public key.
    :type name: str

    :param reported_at: Timestamp in milliseconds
    :type reported_at: int

    :param rssi: Received Signal Strength Indicator is reported by the hotspot and indicates how strong the signal device's radio signal was
    :type rssi: float

    :param snr: In dB, Signal to Noise Ratio is reported by the hotspot to indicate how clear the signal was relative to environmental noise
    :type snr: float

    :param spreading: LoRa Spreading Factor and Bandwidth used for the radio transmission.
    :type spreading: str

    """

    frequency: float
    id: str
    name: str
    reported_at: datetime
    rssi: float
    snr: float
    spreading: str
    lat: float = None
    long: float = None

    def __post_init__(self):
        if isinstance(self.reported_at, int):
            self.reported_at = datetime.fromtimestamp(self.reported_at)
        elif isinstance(self.reported_at, str):
            self.reported_at = datetime.fromtimestamp(int(self.reported_at))
        else:
            raise Exception("Timestamp has to be type 'int' or 'str'.")

    def load_location(self):
        if not self.lat or not self.long:
            hotspot = load_hotspot(self.id)
            self.lat = hotspot["lat"]
            self.long = hotspot["lng"]
