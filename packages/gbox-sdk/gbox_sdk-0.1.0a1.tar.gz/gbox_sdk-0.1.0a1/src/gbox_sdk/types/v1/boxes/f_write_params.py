# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FWriteParams"]


class FWriteParams(TypedDict, total=False):
    content: Required[str]
    """Content of the file"""

    path: Required[str]
    """Path to the file"""
