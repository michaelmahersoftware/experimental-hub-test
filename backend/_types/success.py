"""Provide the `SuccessDict` TypedDict.

Use for type hints and static type checking without any overhead during runtime.
"""

from __future__ import annotations

from typing import TypedDict, Literal


class SuccessDict(TypedDict):
    """Response TypedDict to successfull api calls.

    Attributes
    ----------
    type : _types.success.SUCCESS_TYPES
        Unique success type, defining what accion was successfully executed.
    description : str
        Description of what action (api call) was successfully executed.

    See Also
    --------
    Data Types Wiki :
        https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#success
    """

    type: SUCCESS_TYPES
    description: str


# TODO define valid types
SUCCESS_TYPES = Literal[
    "TO_BE_DEFINED",
    "SAVE_SESSION",
    "DELETE_SESSION",
    "START_EXPERIMENT",
    "STOP_EXPERIMENT",
    "ADD_NOTE",
]
"""Possible success types for _types.success.SuccessDict.

See Also
--------
Data Types Wiki :
    https://github.com/TUMFARSynchorny/experimental-hub/wiki/Data-Types#message
"""
