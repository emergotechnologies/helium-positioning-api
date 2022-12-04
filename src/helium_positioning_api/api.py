from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from helium_positioning_api.Models import NearestNeighborModel, Midpoint

app = FastAPI(title="Helium Positioning API")


class Device(BaseModel):
    """Class for device object."""
    uuid: str


# nearest neighbor model
@app.post("/predict_tf/", status_code=200)
async def predict_tf(request: Device):
    """Creates a prediction with Nearest Neighbor model."""
    prediction = NearestNeighborModel().predict(uuid=request.uuid)
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction


# midpoint model
@app.post("/predict_mp/", status_code=200)
async def predict_mp(request: Device):
    """Creates a prediction with Midpoint model."""
    prediction = Midpoint().predict(uuid=request.uuid)
    if not prediction:
        raise HTTPException(status_code=404, detail="Device not found.")
    return prediction
