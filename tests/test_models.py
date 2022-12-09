"""Test cases for the models module."""
import json
from typing import Any

import pytest
from haversine import Unit
from haversine import haversine
from helium_api_wrapper.devices import Event

from helium_positioning_api.Models import Midpoint
from helium_positioning_api.Models import NearestNeighborModel


@pytest.fixture
def mock_integration() -> Event:
    """Mock integration for testing.

    :return: integration Event
    """
    with open("tests/data/integration_events.json") as file:
        integrations = json.load(file)
    return integrations[0]


def test_nearest_neighbor_model(mocker: Any, mock_integration: Event) -> None:
    """Test for the nearest neighbor model.

    :param mocker: Mocker
    :param mock_integration: Event

    """
    mocker.patch(
        "helium_positioning_api.Models.load_last_integration",
        return_value=mock_integration,
        autospec=True,
    )
    mocker.patch(
        "helium_positioning_api.DataObjects.load_hotspot",
        return_value={"lat": 47.47771443776213, "lng": 12.053189171302527},
    )
    prediction = NearestNeighborModel().predict(uuid="uuid")
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


def test_midpoint_model() -> None:
    """Test for the midpoint model."""
    prediction = Midpoint().predict(uuid="uuid")

    assert (
        haversine(
            prediction, (47.47771443776213, 12.053189171302527), unit=Unit.KILOMETERS
        )
        < 14
    )
