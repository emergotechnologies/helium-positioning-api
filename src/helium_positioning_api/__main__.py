"""Command-line interface."""
import click
import uvicorn

from helium_positioning_api.Models import Midpoint
from helium_positioning_api.Models import NearestNeighborModel


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.option(
    "--model",
    default="nearest_neighbor",
    type=click.Choice(["best", "nearest_neighbor", "linear_regression"]),
    help="Model to be used to predict the position of the device.",
)
@click.version_option(version="0.1")
def predict(uuid: str, model: str) -> None:
    """Predict the position (lng,lat) of a device with the given uuid.

    :param uuid: device id
    :param model: prediction model
    """
    if model == "nearest_neighbor":
        prediction = NearestNeighborModel().predict(uuid)
        print(prediction)
    elif model == "midpoint":
        prediction = Midpoint().predict(uuid)
    else:
        raise Exception(f"Model '{model}' not implemented.")


@click.command()
@click.option("--port", default=8000, type=int)
@click.version_option(version="0.1")
def serve(port: int) -> None:
    """Service for position-prediction of Helium network devices."""
    uvicorn.run(
        "helium_positioning_api.api:app",
        # host="0.0.0.0",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        proxy_headers=True,
        reload=True,
    )


@click.group(help="CLI tool for device-position-prediction in the Helium network.")
def cli() -> None:
    """CLI tool for device-position-prediction in the Helium network."""
    pass


cli.add_command(predict)
cli.add_command(serve)

if __name__ == "__main__":
    cli()
