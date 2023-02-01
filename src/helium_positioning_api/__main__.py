"""Main module.

.. module:: __main__

:synopsis: Command-line interface

.. moduleauthor:: DSIA21

"""

import click
import uvicorn

from helium_positioning_api.midpoint import midpoint
from helium_positioning_api.nearest_neighbor import nearest_neighbor
from helium_positioning_api.trilateration import trilateration


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.option(
    "--model",
    default="nearest_neighbor",
    type=click.Choice(
        [
            "best",
            "nearest_neighbor",
            "midpoint",
            "linear_regression",
            "gradient_boosting",
        ]
    ),
    help="Model to be used to predict the position of the device.",
)
@click.version_option(version="0.1")
def predict(uuid: str, model: str) -> None:
    """Predict the position (lng,lat) of a device with the given uuid.

    :param uuid: device id
    :param model: prediction model
    """
    if model == "nearest_neighbor":
        prediction = nearest_neighbor(uuid)
        print(prediction)
    elif model == "midpoint":
        prediction = midpoint(uuid)
        print(prediction)
    elif model == "linear_regression":
        prediction = trilateration(uuid, model="linear_regression")
        print(prediction)
    elif model == "gradient_boosting":
        prediction = trilateration(uuid, model="gradient_boosting")
        print(prediction)
    else:
        raise Exception(f"Model {model} not implemented.")


@click.command()
@click.option("--port", default=8000, type=int)
@click.version_option(version="0.1")
def serve(port: int) -> None:
    """Serve a prediction service for the prediction of the position of a device in the Helium network."""
    uvicorn.run(
        "helium_positioning_api.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        proxy_headers=True,
        reload=True,
    )


@click.group(
    help="CLI tool to predict the position of a LoraWan device in the Helium network."
)
def cli() -> None:
    """CLI tool for device-position-prediction in the Helium network."""
    pass


cli.add_command(predict)
cli.add_command(serve)

if __name__ == "__main__":
    cli()
