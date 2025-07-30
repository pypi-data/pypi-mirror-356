# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .create_box_config_param import CreateBoxConfigParam

__all__ = ["CreateAndroidBoxParam"]


class CreateAndroidBoxParam(TypedDict, total=False):
    type: Required[Literal["android"]]
    """Box type is Android"""

    config: CreateBoxConfigParam
    """Configuration for an Android box instance"""
