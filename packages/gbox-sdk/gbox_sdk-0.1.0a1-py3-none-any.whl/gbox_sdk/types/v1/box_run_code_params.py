# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["BoxRunCodeParams"]


class BoxRunCodeParams(TypedDict, total=False):
    code: Required[str]
    """The code to run"""

    type: Required[Literal["bash", "python3", "typescript"]]
    """The type of the code."""

    argv: List[str]
    """The arguments to run the code. e.g. ["-h"]"""

    envs: object
    """The environment variables to run the code"""

    api_timeout: Annotated[str, PropertyInfo(alias="timeout")]
    """The timeout of the code. e.g. "30s" """

    working_dir: Annotated[str, PropertyInfo(alias="workingDir")]
    """The working directory of the code."""
