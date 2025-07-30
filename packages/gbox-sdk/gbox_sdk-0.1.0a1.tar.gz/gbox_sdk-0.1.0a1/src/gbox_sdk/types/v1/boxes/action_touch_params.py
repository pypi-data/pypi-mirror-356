# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionTouchParams", "Point", "PointStart"]


class ActionTouchParams(TypedDict, total=False):
    points: Required[Iterable[Point]]
    """Array of touch points and their actions"""

    type: Required[object]
    """Action type for touch interaction"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""


class PointStart(TypedDict, total=False):
    x: Required[float]
    """Starting X coordinate"""

    y: Required[float]
    """Starting Y coordinate"""


class Point(TypedDict, total=False):
    start: Required[PointStart]
    """Starting position for touch"""

    actions: Iterable[object]
    """Sequence of actions to perform after initial touch"""
