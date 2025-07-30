# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CreateBoxConfigParam"]


class CreateBoxConfigParam(TypedDict, total=False):
    envs: object
    """Environment variables for the box"""

    expires_in: Annotated[str, PropertyInfo(alias="expiresIn")]
    """The box will be alive for the given duration (e.g. '10m')"""

    labels: object
    """Key-value pairs of labels for the box"""
