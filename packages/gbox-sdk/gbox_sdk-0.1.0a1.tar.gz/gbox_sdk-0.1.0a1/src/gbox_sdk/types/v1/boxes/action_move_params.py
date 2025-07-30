# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionMoveParams"]


class ActionMoveParams(TypedDict, total=False):
    type: Required[object]
    """Action type for cursor movement"""

    x: Required[float]
    """X coordinate to move to"""

    y: Required[float]
    """Y coordinate to move to"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""
