"""Test cases for the models module."""
import json
from typing import Any
from typing import List

import pytest
from haversine import Unit  # type: ignore[import]
from haversine import haversine
from helium_api_wrapper import DataObjects as DataObjects
from helium_api_wrapper.hotspots import get_hotspot_by_address
from pytest_mock import MockFixture

from helium_positioning_api.DataObjects import Prediction
from helium_positioning_api.Models import NearestNeighborModel


@pytest.fixture
def mock_integration() -> Any:
    """Mock integration for testing.

    :return: integration Event
    """
    with open("tests/data/integration_events.json") as file:
        integrations = json.load(file)
    return integrations[0]


@pytest.fixture
def mock_hotspots() -> Any:
    """Mock hotspots.

    :return: List of hotspots
    :rtype: Any
    """
    with open("tests/data/hotspots.json") as file:
        hotspot = json.load(file)
    return hotspot


def test_nearest_neighbor_model(
    module_mocker: MockFixture, mock_integration: Any, mock_hotspots: Any
) -> None:
    """Test for the nearest neighbor model.

    :param mocker: Mocker
    :param mock_integration: Event

    """
    module_mocker.patch(
        "helium_positioning_api.Models.get_last_integration",
        return_value=transform_integration(
            [mock_integration], module_mocker, mock_hotspots
        ),
        autospec=True,
    )

    prediction = NearestNeighborModel().predict(uuid="uuid")
    print(prediction)

    assert prediction == Prediction(
        uuid="uuid",
        lat=47.47771443776213,
        lng=12.053189171302527,
        timestamp=1669295750681,
    )
    # TODO consider testing strategy that is not reliant on hardcoded values,
    # as they are potentially subject to change in most recent integration
    # assert prediction == Prediction(
    #   uuid="uuid", lat=47.47771443776213, lng=12.053189171302527)
    assert (
        haversine(
            prediction, (47.47771443776213, 12.053189171302527), unit=Unit.KILOMETERS
        )
        < 14
    )


# def test_midpoint_model() -> None:
#     """Test for the midpoint model."""
#     prediction = Midpoint().predict(uuid="uuid")
#
#     assert (
#         haversine(
#             prediction, (47.47771443776213, 12.053189171302527), unit=Unit.KILOMETERS
#         )
#         < 14
#     )


def transform_integration(
    event: List[dict], module_mocker: MockFixture, mock_hotspots: Any
) -> DataObjects.Event:
    """Transform integration."""
    module_mocker.patch(
        "helium_api_wrapper.hotspots.get_hotspot_by_address",
        return_value=DataObjects.Hotspot(**mock_hotspots[0]),
        autospec=True,
    )

    event = event[0]
    hotspots = []

    for hotspot in event["data"]["req"]["body"]["hotspots"]:
        print(get_hotspot_by_address(hotspot["id"]))
        h = get_hotspot_by_address(hotspot["id"])[0].dict()
        h["rssi"] = hotspot["rssi"]
        h["snr"] = hotspot["snr"]
        h["spreading"] = hotspot["spreading"]
        h["frequency"] = hotspot["frequency"]
        h["reported_at"] = hotspot["reported_at"]
        h["status"] = hotspot["snr"]
        hotspots.append(DataObjects.IntegrationHotspot(**h))

    event["hotspots"] = hotspots

    try:
        return DataObjects.Event(**event)
    except IndexError:
        raise IndexError("No hotspots found") from None
