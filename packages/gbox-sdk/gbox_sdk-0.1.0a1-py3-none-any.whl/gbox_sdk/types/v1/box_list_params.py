# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["BoxListParams"]


class BoxListParams(TypedDict, total=False):
    page: Required[float]
    """Page number"""

    page_size: Required[Annotated[float, PropertyInfo(alias="pageSize")]]
    """Page size"""
