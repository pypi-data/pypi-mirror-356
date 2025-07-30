# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionClickParams"]


class ActionClickParams(TypedDict, total=False):
    type: Required[object]
    """Action type for mouse click"""

    x: Required[float]
    """X coordinate of the click"""

    y: Required[float]
    """Y coordinate of the click"""

    button: Literal["left", "right", "middle"]
    """Mouse button to click"""

    double: bool
    """Whether to perform a double click"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""
