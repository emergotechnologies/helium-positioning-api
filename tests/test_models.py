"""Test cases for the models module."""
import json
from typing import Any

import pytest
from haversine import Unit  # type: ignore[import]
from haversine import haversine

from pytest_mock import MockFixture

from helium_api_wrapper import DataObjects as DataObjects
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
        return_value=transform_integration(mock_integration),
        autospec=True,
    )

    prediction = NearestNeighborModel().predict(
        uuid="92f23793-6647-40aa-b255-fa1d4baec75d"
    )
    print(prediction)

    assert prediction == Prediction(
        uuid="92f23793-6647-40aa-b255-fa1d4baec75d",
        lat=37.784056617819544,
        lng=-122.39186733984285,
        timestamp=1632353389723,
    )

    assert (
        haversine(
            (prediction.lat, prediction.lng),
            (37.784056617819544, -122.39186733984285),
            unit=Unit.KILOMETERS,
        )
        == 0
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


def transform_integration(event: dict) -> DataObjects.IntegrationEvent:
    """Transform integration."""
    hotspots = []
    for hotspot in event["data"]["req"]["body"]["hotspots"]:
        hotspots.append(DataObjects.IntegrationHotspot(**hotspot))
    event["hotspots"] = hotspots
    return DataObjects.IntegrationEvent(**event)
