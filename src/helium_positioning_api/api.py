from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from helium_positioning_api.Models import NearestNeighborModel, Midpoint

app = FastAPI(title="Helium Positioning API")

class Device(BaseModel):
    uuid: str

@app.post("/predict/", status_code=200)
async def predict_tf(request: Device):
    prediction = NearestNeighborModel().predict(uuid=request.uuid)
    if not prediction:
        raise HTTPException(
            status_code=404, detail="Device not found."
        )
    return prediction

@app.post("/predict/", status_code=200)
async def predict_mp(request: Device):
    prediction = Midpoint().predict(uuid=request.uuid)
    if not prediction:
        raise HTTPException(
            status_code=404, detail="Device not found."
        )
    return prediction 