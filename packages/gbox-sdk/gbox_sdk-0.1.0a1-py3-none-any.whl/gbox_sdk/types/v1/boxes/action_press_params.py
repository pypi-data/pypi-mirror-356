# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ActionPressParams"]


class ActionPressParams(TypedDict, total=False):
    keys: Required[List[str]]
    """Array of keys to press"""

    type: Required[object]
    """Action type for keyboard key press"""

    output_format: Annotated[Literal["base64", "storageKey"], PropertyInfo(alias="outputFormat")]
    """Type of the URI"""
