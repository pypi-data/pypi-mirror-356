# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionScrollParams"]


class ActionScrollParams(TypedDict, total=False):
    scroll_x: Required[Annotated[float, PropertyInfo(alias="scrollX")]]
    """Horizontal scroll amount"""

    scroll_y: Required[Annotated[float, PropertyInfo(alias="scrollY")]]
    """Vertical scroll amount"""

    type: Required[object]
    """Action type for scroll interaction"""

    x: Required[float]
    """X coordinate of the scroll position"""

    y: Required[float]
    """Y coordinate of the scroll position"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""
