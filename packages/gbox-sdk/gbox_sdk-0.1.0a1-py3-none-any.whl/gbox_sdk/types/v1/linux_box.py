# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["LinuxBox", "Config", "ConfigBrowser", "ConfigOs", "ConfigResolution"]


class ConfigBrowser(BaseModel):
    type: Literal["chromium", "firefox", "webkit"]
    """Supported browser types for Linux boxes"""

    version: str
    """Browser version string (e.g. '12')"""


class ConfigOs(BaseModel):
    version: str
    """OS version string (e.g. 'ubuntu-20.04')"""


class ConfigResolution(BaseModel):
    height: float
    """Height of the box"""

    width: float
    """Width of the box"""


class Config(BaseModel):
    browser: ConfigBrowser
    """Browser configuration"""

    cpu: float
    """CPU cores allocated to the box"""

    envs: object
    """Environment variables for the box"""

    labels: object
    """Key-value pairs of labels for the box"""

    memory: float
    """Memory allocated to the box in MB"""

    os: ConfigOs
    """Operating system configuration"""

    resolution: ConfigResolution
    """Resolution of the box"""

    storage: float
    """Storage allocated to the box in GB."""

    working_dir: str = FieldInfo(alias="workingDir")
    """Working directory path for the box"""


class LinuxBox(BaseModel):
    id: str
    """Unique identifier for the box"""

    config: Config
    """Configuration for a Linux box instance"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Creation timestamp of the box"""

    expires_at: datetime = FieldInfo(alias="expiresAt")
    """Expiration timestamp of the box"""

    status: Literal["pending", "running", "stopped", "error"]
    """The current status of a box instance"""

    type: Literal["linux"]
    """Box type is Linux"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Last update timestamp of the box"""
