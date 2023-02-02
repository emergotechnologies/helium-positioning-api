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
from helium_positioning_api.trilateration import trilateration


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


# trilateration with linear regression
@app.post("/predict_tl_lin/", status_code=200)
async def predict_tl_lin(request: Device) -> Prediction:
    """Create a prediction with the Trialteratioin model, using a linear regression distance estimator.

    :param request: Device
    :return: predicted coordinates
    """
    prediction = trilateration(uuid=request.uuid, model="linear_regression")
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction


# trilateration with gradient boost
@app.post("/predict_tl_grad/", status_code=200)
async def predict_tl_grad(request: Device) -> Prediction:
    """Create a prediction with the Midpoint model, using a gradient boosted regression for distance estimaton.

    :param request: Device
    :return: predicted coordinates
    """
    prediction = trilateration(uuid=request.uuid, model="gradient_boosting")
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction
