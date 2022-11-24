"""Test cases for the models module."""
import pytest
import json
from helium_positioning_api.Models import NearestNeighborModel 
from helium_positioning_api.DataObjects import Prediction


@pytest.fixture
def mock_integration():
    with open("tests/data/integration_events.json", "r") as file:
        integrations = json.load(file)
    return integrations[0]

def test_nearest_neighbor_model(mocker, mock_integration):

    mocker.patch("helium_positioning_api.Models.load_last_integration", return_value=mock_integration, autospec=True)
    mocker.patch("helium_positioning_api.DataObjects.load_hotspot", return_value={"lat": 47.47771443776213, "lng": 12.053189171302527})

    prediction = NearestNeighborModel().predict(uuid="uuid")

    assert prediction == Prediction(uuid="uuid", lat=47.47771443776213, lng=12.053189171302527)




