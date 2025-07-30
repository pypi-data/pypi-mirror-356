# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionDragParams", "Path"]


class ActionDragParams(TypedDict, total=False):
    path: Required[Iterable[Path]]
    """Path of the drag action as a series of coordinates"""

    type: Required[object]
    """Action type for drag interaction"""

    duration: str
    """Time interval between points (e.g. "50ms")"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""


class Path(TypedDict, total=False):
    x: Required[float]
    """X coordinate of a point in the drag path"""

    y: Required[float]
    """Y coordinate of a point in the drag path"""
