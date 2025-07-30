# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .create_box_config_param import CreateBoxConfigParam

__all__ = ["BoxCreateParams", "CreateLinuxBox", "CreateAndroidBox"]


class CreateLinuxBox(TypedDict, total=False):
    type: Required[Literal["linux"]]
    """Box type is Linux"""

    config: CreateBoxConfigParam
    """Configuration for a Linux box instance"""


class CreateAndroidBox(TypedDict, total=False):
    type: Required[Literal["android"]]
    """Box type is Android"""

    config: CreateBoxConfigParam
    """Configuration for an Android box instance"""


BoxCreateParams: TypeAlias = Union[CreateLinuxBox, CreateAndroidBox]
