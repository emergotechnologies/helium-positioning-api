"""Data objects module."""
from typing import List
from typing import Optional
from pydantic import BaseModel
from typing import Any
from typing import Dict

from helium_api_wrapper.devices import get_device_by_uuid


class DataObject(BaseModel):
    """Base class for all data objects."""

    def __len__(self) -> int:
        """Return the length of the object.

        :return: length of object (int)
        """
        return dict(self).__len__()

    def __getitem__(self, item: Any) -> Any:
        """Access the dictionary with the value of item as the key.

        :return: dictionary value for key
        """
        return getattr(self, item)

    def as_dict(self, columns: Optional[List[str]] = None) -> Dict[Any, Any]:
        """
        Cast data as dictionary.

        return: Dictionary
        """
        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data


class Prediction(DataObject):
    """Class to describe a Prediction Object."""

    uuid: str
    lat: float
    lng: float
    conf: Optional[float] = None


class Hotspot(DataObject):
    """Hotspots which received the same packet.

    :param frequency: In MHz, the frequency which the packet was received upon.
    :type frequency: float

    :param id: A base58 encoding of the hotspot's public key.
    :type id: str

    :param name: human-friendly three-word alias of the hotspot's public key.
    :type name: str

    :param reported_at: Timestamp in milliseconds
    :type reported_at: float

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
    reported_at: str
    rssi: float
    snr: float
    spreading: str
    lat: Optional[float] = None
    long: Optional[float] = None

    def load_location(self) -> None:
        """Assign latitude and longitude to the object \
            from the data in Hotspots object."""
        if not self.lat or not self.long:
            hotspot = get_device_by_uuid(self.id)
            self.lat = hotspot["lat"]
            self.long = hotspot["lng"]
