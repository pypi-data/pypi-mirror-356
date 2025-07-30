# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["BoxExecuteCommandsParams"]


class BoxExecuteCommandsParams(TypedDict, total=False):
    commands: Required[List[str]]
    """The command to run"""

    envs: object
    """The environment variables to run the command"""

    api_timeout: Annotated[str, PropertyInfo(alias="timeout")]
    """The timeout of the command. e.g. '30s'"""

    working_dir: Annotated[str, PropertyInfo(alias="workingDir")]
    """The working directory of the command"""
