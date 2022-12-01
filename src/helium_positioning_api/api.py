"""API Module.

.. module:: api

:synopsis: REST api functions for the prediction of device position. 

.. moduleauthor:: DSIA21

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from helium_positioning_api.Models import NearestNeighborModel

app = FastAPI(title="Helium Positioning API")

class Device(BaseModel):
    uuid: str

@app.get("/predict/{uuid}", status_code=200)
async def predict(uuid: str):
    """Hotspots which received the same packet.
    
    :param uuid: UUID of the device.
    :type uuid: str

    :return: Prediction of device position.
    :rtype: dict
    """
    prediction = NearestNeighborModel().predict(uuid=uuid)
    if not prediction:
        raise HTTPException(
            status_code=404, detail="Device not found."
        )
    return prediction

