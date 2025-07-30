# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FListResponse", "Data", "DataFile", "DataDir"]


class DataFile(BaseModel):
    last_modified: datetime = FieldInfo(alias="lastModified")
    """Last modified time of the file"""

    name: str
    """Name of the file"""

    path: str
    """Full path to the file"""

    size: str
    """Size of the file"""

    type: Literal["file"]
    """File type indicator"""


class DataDir(BaseModel):
    name: str
    """Name of the directory"""

    path: str
    """Full path to the directory"""

    type: Literal["dir"]
    """Directory type indicator"""


Data: TypeAlias = Union[DataFile, DataDir]


class FListResponse(BaseModel):
    data: List[Data]
    """A box instance that can be either Linux or Android type"""
