"""Main module.

.. module:: __main__

:synopsis: Command-line interface

.. moduleauthor:: DSIA21

"""

import click

from helium_api_wrapper.challenges import get_challenges
from helium_api_wrapper.challenges import get_challenges_by_address
from helium_api_wrapper.challenges import load_challenge_data
from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.devices import get_device_by_uuid
from helium_api_wrapper.devices import get_last_event
from helium_api_wrapper.devices import get_last_integration
from helium_api_wrapper.hotspots import get_hotspot_by_address
from helium_api_wrapper.hotspots import get_hotspots
from helium_api_wrapper.ResultHandler import write


@click.command()
@click.option("--address", type=str, help="Address of the hotspot")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="hotspot", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_hotspot(address: str, file_format: str, file_name: str, path: str) -> None:
    """This function returns a Hotspot for a given address."""
    if address:
        hotspot = get_hotspot_by_address(address)
    else:
        raise ValueError("No address given")

    write(
        data=hotspot,
        file_format=file_format,
        file_name=file_name,
        path=path,
    )


@click.command()
@click.option("--n", type=int, help="Nr. of pages to load. 1 page = 1000 hotspots")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="hotspots", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def load_hotspots(n: int, file_format: str, file_name: str, path: str) -> None:
    """This function returns a given number of random Hotspots."""
    hotspots = get_hotspots(n)
    write(
        data=hotspots,
        file_format=file_format,
        file_name=file_name,
        path=path,
    )


@click.command()
@click.option("--address", type=str, help="Address of the hotspot")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="challenges", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_challenges_for_hotspot(
    address: str, file_format: str, file_name: str, path: str
) -> None:
    """This function returns a list of challenges for a given hotspot."""
    write(
        get_challenges_by_address(address),
        file_format=file_format,
        file_name=file_name,
        path=path,
    )


@click.command()
@click.option("--n", type=int, help="Amount of challenges to return")
@click.option(
    "--incremental", is_flag=True, help="Set to save data after each challenge"
)
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="challenges", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def load_challenges(
    n: int, incremental: bool, file_format: str, file_name: str, path: str
) -> None:
    """This function returns a list of challenges."""
    if incremental:
        challenges = get_challenges(limit=n)
        write(
            load_challenge_data(challenges),
            file_format=file_format,
            file_name=file_name,
            path=path,
        )
    else:
        write(
            load_challenge_data(load_type="all", limit=n),
            file_format=file_format,
            file_name=file_name,
            path=path,
        )


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device(uuid: str) -> Device:
    """This function returns a device for a given UUID."""
    device = get_device_by_uuid(uuid)
    print(device)
    return device


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device_integration(uuid: str) -> Event:
    """This function returns the last integration for a given UUID."""
    integration = get_last_integration(uuid)
    print(integration)
    return integration


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device_event(uuid: str) -> Event:
    """This function returns the last event for a given UUID."""
    event = get_last_event(uuid)
    print(event)
    return event


@click.group(
    help="CLI tool to load data from the Helium Blockchain API and Helium Console API"
)
def cli() -> None:
    """Not implemented yet."""
    pass


cli.add_command(get_hotspot)
cli.add_command(load_hotspots)
cli.add_command(load_challenges)
cli.add_command(get_challenges_for_hotspot)
cli.add_command(get_device)
cli.add_command(get_device_integration)
cli.add_command(get_device_event)

if __name__ == "__main__":
    cli()
