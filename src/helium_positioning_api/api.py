"""API Module.

.. module:: api

:synopsis: REST api functions for the prediction of device position.

.. moduleauthor:: DSIA21

"""

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from helium_positioning_api.DataObjects import Prediction
from helium_positioning_api.midpoint import midpoint
from helium_positioning_api.nearest_neighbor import nearest_neighbor


app = FastAPI(title="Helium Positioning API")


class Device(BaseModel):
    """Class for device object."""

    uuid: str


# nearest neighbor model
@app.post("/predict_tf/", status_code=200)
async def predict_tf(request: Device) -> Prediction:
    """Create a prediction with Nearest Neighbor model.

    :param request: Device
    :return: predicted coordinates
    """
    prediction = nearest_neighbor(uuid=request.uuid)
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction


# midpoint model
@app.post("/predict_mp/", status_code=200)
async def predict_mp(request: Device) -> Prediction:
    """Create a prediction with the Midpoint model.

    :param request: Device
    :return: predicted coordinates
    """
    prediction = midpoint(uuid=request.uuid)
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction
