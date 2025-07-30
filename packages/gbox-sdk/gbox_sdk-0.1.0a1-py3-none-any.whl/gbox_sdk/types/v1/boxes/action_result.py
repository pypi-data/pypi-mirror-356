# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["ActionResult", "Screenshot", "ScreenshotAfter", "ScreenshotBefore", "ScreenshotHighlight"]


class ScreenshotAfter(BaseModel):
    uri: str
    """URI of the screenshot after the action"""


class ScreenshotBefore(BaseModel):
    uri: str
    """URI of the screenshot before the action"""


class ScreenshotHighlight(BaseModel):
    uri: str
    """URI of the screenshot before the action with highlight"""


class Screenshot(BaseModel):
    after: ScreenshotAfter
    """URI of the screenshot after the action"""

    before: ScreenshotBefore
    """URI of the screenshot before the action"""

    highlight: ScreenshotHighlight
    """URI of the screenshot before the action with highlight"""


class ActionResult(BaseModel):
    screenshot: Screenshot
    """screenshot"""
