# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .create_box_config_param import CreateBoxConfigParam

__all__ = ["CreateLinuxBoxParam"]


class CreateLinuxBoxParam(TypedDict, total=False):
    type: Required[Literal["linux"]]
    """Box type is Linux"""

    config: CreateBoxConfigParam
    """Configuration for a Linux box instance"""
