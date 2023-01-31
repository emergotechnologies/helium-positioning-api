"""Data Objects module.

.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class Geocode(BaseModel):  # type: ignore[misc]
    """Class to describe Geocode Object."""

    long_city: Optional[str] = None
    long_country: Optional[str] = None
    long_state: Optional[str] = None
    long_street: Optional[str] = None
    short_city: Optional[str] = None
    short_country: Optional[str] = None
    short_state: Optional[str] = None
    short_street: Optional[str] = None
    city_id: Optional[str] = None


class Status(BaseModel):
    """Class to describe Status Object."""

    height: Optional[int] = None
    online: Optional[str] = None


class Hotspot(BaseModel):
    """Class to describe Hotspot Object."""

    address: Optional[str] = None
    block: Optional[int] = None
    block_added: Optional[int] = None
    geocode: Optional[Geocode] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    location: Optional[str] = None
    name: Optional[str] = None
    nonce: Optional[int] = None
    owner: Optional[str] = None
    reward_scale: Optional[float] = None
    status: Optional[Status] = None


class Role(BaseModel):
    """Class to describe Role Object."""

    type: str
    time: int
    role: str
    height: Optional[int] = None
    hash: Optional[str] = None


class Witness(BaseModel):
    """Class to describe Witness Object."""

    timestamp: int
    signal: int
    packet_hash: str
    owner: str
    location: str
    gateway: str
    is_valid: Optional[bool] = None
    datarate: Optional[str] = None
    snr: Optional[float] = None


class Receipt(BaseModel):
    """Class to describe Receipt Object."""

    timestamp: int
    signal: int
    origin: str
    gateway: str
    data: str


class Challenge(BaseModel):
    """Class to describe a Challenge loaded from the Helium API."""

    type: str
    time: int
    secret: str
    path: Optional[List[Dict[str, Any]]] = None
    onion_key_hash: Optional[str] = None
    height: Optional[int] = None
    hash: Optional[str] = None
    challenger_owner: Optional[str] = None
    challenger_lon: Optional[float] = None
    challenger_location: Optional[str] = None
    challenger_lat: Optional[float] = None
    challenger: Optional[str] = None
    fee: Optional[int] = None


class ChallengeResult(BaseModel):
    """Class to describe a Challenge loaded from the Helium API."""

    challengee: Optional[str]
    challengee_lat: Optional[float]
    challengee_lng: Optional[float]
    witness: Optional[str]
    witness_lat: Optional[float]
    witness_lng: Optional[float]
    signal: Optional[int]
    snr: Optional[float]
    datarate: Optional[str]
    is_valid: Optional[bool]
    hash: Optional[str]
    time: Optional[int]
    distance: Optional[float]


class ChallengeResolved(BaseModel):
    """Class to describe a resolved Challenge."""

    type: str
    time: int
    secret: str
    # path: List[Dict[str, AnyOptional[]]] = None
    onion_key_hash: Optional[str] = None
    height: Optional[int] = None
    hash: Optional[str] = None
    witnesses: Optional[List[Witness]] = None
    receipt: Optional[Receipt] = None
    geocode: Optional[Geocode] = None
    challengee_owner: Optional[str] = None
    challengee_lon: Optional[float] = None
    challengee_location: Optional[str] = None
    challengee_lat: Optional[float] = None
    challengee: Optional[str] = None
    challenger_owner: Optional[str] = None
    challenger_lon: Optional[float] = None
    challenger_location: Optional[str] = None
    challenger_lat: Optional[float] = None
    challenger: Optional[str] = None
    fee: Optional[int] = None


class Device(BaseModel):
    """Class to describe Device in Helium API."""

    adr_allowed: Optional[bool] = None
    app_eui: Optional[str] = None
    app_key: Optional[str] = None
    cf_list_enabled: Optional[bool] = None
    dc_usage: Optional[int] = None
    dev_eui: Optional[str] = None
    id: Optional[str] = None
    in_xor_filter: Optional[bool] = None
    labels: Optional[List[Any]] = None
    last_connected: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[str] = None
    oui: Optional[str] = None
    total_packets: Optional[int] = None


class Event(BaseModel):
    """Class to describe an Integration Event."""

    data: Dict[str, Any]
    description: str
    device_id: str
    frame_down: Optional[int] = None
    frame_up: Optional[int] = None
    organization_id: str
    reported_at: str
    router_uuid: str
    sub_category: str
