"""Challenge Module.

.. module:: helpers

:synopsis: Functions to load Challenges from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

from haversine import Unit
from haversine import haversine

from helium_api_wrapper.DataObjects import Challenge
from helium_api_wrapper.DataObjects import ChallengeResolved
from helium_api_wrapper.DataObjects import ChallengeResult
from helium_api_wrapper.DataObjects import Hotspot
from helium_api_wrapper.DataObjects import Witness
from helium_api_wrapper.endpoint import request
from helium_api_wrapper.hotspots import get_hotspot_by_address


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_challenges(limit: int = 50) -> List[ChallengeResolved]:
    """Load a list of challenges.

    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    challenges = request(
        url="challenges",
        endpoint="api",
        params={"limit": limit},
    )

    return [__resolve_challenge(Challenge(**challenge)) for challenge in challenges]


def get_challenge_by_id(id: str) -> Union[ChallengeResolved, None]:
    """Load a challenge.

    :param id: Hash of the challenge
    :return: Challenge
    """
    logger.info(f"Getting challenges from transaction {id}")
    transaction = request(url=f"transactions/{id}", endpoint="api")
    # todo: check if transaction is a challenge
    logger.info(transaction)
    if transaction[0]["type"] != "poc_receipts_v1":
        logger.warning(f"Transaction {id} is not a challengee")
        logger.warning(transaction)
        return None  # todo: raise exception or do sth better
    challenge = Challenge(**transaction[0])
    return __resolve_challenge(challenge)


def get_challenges_by_address(address: str, limit: int = 50) -> List[ChallengeResolved]:
    """Get a list of challenges.

    When passed an address, it will get the challenges for that hotspot.

    :param address: The address of the hotspot, defaults to ""
    :type address: str, optional

    :param limit: The amount of challenges to get. Defaults to 50
    :type limit: int

    :return: The challenges.
    :rtype: list[Challenge]
    """
    logger.info(f"Getting challenges for {address}")
    challenges = request(
        url=f"hotspots/{address}/challenges",
        endpoint="api",
        params={"limit": limit},
    )

    return [__resolve_challenge(Challenge(**challenge)) for challenge in challenges]


def load_challenge_data(
    challenges: Optional[List[ChallengeResolved]] = None,
    load_type: str = "triangulation",
    limit: int = 50,
) -> Generator[ChallengeResult, None, None]:
    """Load challenge data.

    :param challenges: List of challenges
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    if challenges is None:
        challenges = get_challenges(limit=limit)
    else:
        challenges = challenges

    for challenge in challenges:
        witnesses = __sort_witnesses(challenge.witnesses, load_type=load_type)
        challengee = get_hotspot_by_address(address=challenge.challengee)

        for witness in witnesses:
            witness_hotspot = get_hotspot_by_address(address=witness.gateway)

            if witness_hotspot is None or challengee is None:
                yield

            yield __get_challenge_data(
                challenge=challenge,
                witness=witness,
                hotspot=witness_hotspot[0],
                challengee=challengee[0],
            )


def __get_challenge_data(  # TODO: check if this works I did a lot of changes here I might have messed stuff up
    challenge: ChallengeResolved,
    witness: Witness,
    hotspot: Hotspot,
    challengee: Hotspot,
) -> ChallengeResult:
    """Get challenge data.

    :param challenge: Challenge
    :param witness: Witness
    :param hotspot: Witness hotspot
    :param challengee: Challengee
    :return: Challenge data
    """
    # @todo: check if best position for distance
    distance = haversine(
        (challengee.lat, challengee.lng),
        (hotspot.lat, hotspot.lng),
        unit=Unit.METERS,
    )
    return ChallengeResult(
        challengee=challengee.address,
        challengee_lat=challengee.lat,
        challengee_lng=challengee.lng,
        witness=hotspot.address,
        witness_lat=hotspot.lat,
        witness_lng=hotspot.lng,
        signal=witness.signal,
        snr=witness.snr,
        datarate=witness.datarate,
        is_valid=witness.is_valid,
        hash=challenge.hash,
        time=challenge.time,
        distance=distance,
    )


def __resolve_challenge(challenge: Challenge) -> ChallengeResolved:
    """Resolve a challenge.

    :param challenge: The challenge to resolve, defaults to None
    :type: Challenge

    :return: The resolved challenge.
    :rtype: ChallengeResolved
    """
    logger.info(f"Resolving challenge {challenge.hash}")
    challenge = challenge.dict()

    # We can assume the path to be length 0 or 1 because Multihop PoC is deprecated.
    # see https://github.com/helium/HIP/blob/main/0015-beaconing-rewards.md
    challenge_resolved = {key: challenge[key] for key in challenge if key != "path"}
    challenge_resolved.update(challenge["path"][0])
    return ChallengeResolved(**challenge_resolved)


def __sort_witnesses(witnesses: List[Witness], load_type: str = "all") -> List[Witness]:
    """Sort witnesses by signal and limit by load type.

    :param witnesses: List of witnesses
    :param load_type: Load type
    :return: List of witnesses
    """
    return_witnesses: List[Witness]
    if load_type == "triangulation":
        return_witnesses = sorted(
            witnesses, key=lambda witness: witness.signal, reverse=False
        )[: max(3, len(witnesses))]
    elif load_type == "best_signal":
        if len(witnesses) == 0:
            return witnesses
        return_witnesses = [
            sorted(witnesses, key=lambda witness: witness.signal, reverse=False)[0]
        ]
    else:
        return_witnesses = sorted(
            witnesses,
            key=lambda witness: witness.signal,
            reverse=False,
        )
    return return_witnesses
