# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.v1.boxes import (
    action_drag_params,
    action_move_params,
    action_type_params,
    action_click_params,
    action_press_params,
    action_touch_params,
    action_scroll_params,
    action_screenshot_params,
)
from ....types.v1.boxes.action_result import ActionResult
from ....types.v1.boxes.action_screenshot_response import ActionScreenshotResponse

__all__ = ["ActionsResource", "AsyncActionsResource"]


class ActionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ActionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#accessing-raw-response-data-eg-headers
        """
        return ActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ActionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#with_streaming_response
        """
        return ActionsResourceWithStreamingResponse(self)

    def click(
        self,
        id: str,
        *,
        type: object,
        x: float,
        y: float,
        button: Literal["left", "right", "middle"] | NotGiven = NOT_GIVEN,
        double: bool | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          type: Action type for mouse click

          x: X coordinate of the click

          y: Y coordinate of the click

          button: Mouse button to click

          double: Whether to perform a double click

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/click",
            body=maybe_transform(
                {
                    "type": type,
                    "x": x,
                    "y": y,
                    "button": button,
                    "double": double,
                    "output_format": output_format,
                },
                action_click_params.ActionClickParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def drag(
        self,
        id: str,
        *,
        path: Iterable[action_drag_params.Path],
        type: object,
        duration: str | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          path: Path of the drag action as a series of coordinates

          type: Action type for drag interaction

          duration: Time interval between points (e.g. "50ms")

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/drag",
            body=maybe_transform(
                {
                    "path": path,
                    "type": type,
                    "duration": duration,
                    "output_format": output_format,
                },
                action_drag_params.ActionDragParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def move(
        self,
        id: str,
        *,
        type: object,
        x: float,
        y: float,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          type: Action type for cursor movement

          x: X coordinate to move to

          y: Y coordinate to move to

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/move",
            body=maybe_transform(
                {
                    "type": type,
                    "x": x,
                    "y": y,
                    "output_format": output_format,
                },
                action_move_params.ActionMoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def press(
        self,
        id: str,
        *,
        keys: List[str],
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          keys: Array of keys to press

          type: Action type for keyboard key press

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/press",
            body=maybe_transform(
                {
                    "keys": keys,
                    "type": type,
                    "output_format": output_format,
                },
                action_press_params.ActionPressParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def screenshot(
        self,
        id: str,
        *,
        clip: action_screenshot_params.Clip | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        type: Literal["png", "jpeg"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionScreenshotResponse:
        """
        Args:
          clip: clip of the screenshot

          output_format: Type of the URI

          type: Action type for screenshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/screenshot",
            body=maybe_transform(
                {
                    "clip": clip,
                    "output_format": output_format,
                    "type": type,
                },
                action_screenshot_params.ActionScreenshotParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionScreenshotResponse,
        )

    def scroll(
        self,
        id: str,
        *,
        scroll_x: float,
        scroll_y: float,
        type: object,
        x: float,
        y: float,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          scroll_x: Horizontal scroll amount

          scroll_y: Vertical scroll amount

          type: Action type for scroll interaction

          x: X coordinate of the scroll position

          y: Y coordinate of the scroll position

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/scroll",
            body=maybe_transform(
                {
                    "scroll_x": scroll_x,
                    "scroll_y": scroll_y,
                    "type": type,
                    "x": x,
                    "y": y,
                    "output_format": output_format,
                },
                action_scroll_params.ActionScrollParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def touch(
        self,
        id: str,
        *,
        points: Iterable[action_touch_params.Point],
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          points: Array of touch points and their actions

          type: Action type for touch interaction

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/touch",
            body=maybe_transform(
                {
                    "points": points,
                    "type": type,
                    "output_format": output_format,
                },
                action_touch_params.ActionTouchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    def type(
        self,
        id: str,
        *,
        text: str,
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          text: Text to type

          type: Action type for typing text

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/actions/type",
            body=maybe_transform(
                {
                    "text": text,
                    "type": type,
                    "output_format": output_format,
                },
                action_type_params.ActionTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )


class AsyncActionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncActionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#accessing-raw-response-data-eg-headers
        """
        return AsyncActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncActionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#with_streaming_response
        """
        return AsyncActionsResourceWithStreamingResponse(self)

    async def click(
        self,
        id: str,
        *,
        type: object,
        x: float,
        y: float,
        button: Literal["left", "right", "middle"] | NotGiven = NOT_GIVEN,
        double: bool | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          type: Action type for mouse click

          x: X coordinate of the click

          y: Y coordinate of the click

          button: Mouse button to click

          double: Whether to perform a double click

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/click",
            body=await async_maybe_transform(
                {
                    "type": type,
                    "x": x,
                    "y": y,
                    "button": button,
                    "double": double,
                    "output_format": output_format,
                },
                action_click_params.ActionClickParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def drag(
        self,
        id: str,
        *,
        path: Iterable[action_drag_params.Path],
        type: object,
        duration: str | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          path: Path of the drag action as a series of coordinates

          type: Action type for drag interaction

          duration: Time interval between points (e.g. "50ms")

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/drag",
            body=await async_maybe_transform(
                {
                    "path": path,
                    "type": type,
                    "duration": duration,
                    "output_format": output_format,
                },
                action_drag_params.ActionDragParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def move(
        self,
        id: str,
        *,
        type: object,
        x: float,
        y: float,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          type: Action type for cursor movement

          x: X coordinate to move to

          y: Y coordinate to move to

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/move",
            body=await async_maybe_transform(
                {
                    "type": type,
                    "x": x,
                    "y": y,
                    "output_format": output_format,
                },
                action_move_params.ActionMoveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def press(
        self,
        id: str,
        *,
        keys: List[str],
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          keys: Array of keys to press

          type: Action type for keyboard key press

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/press",
            body=await async_maybe_transform(
                {
                    "keys": keys,
                    "type": type,
                    "output_format": output_format,
                },
                action_press_params.ActionPressParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def screenshot(
        self,
        id: str,
        *,
        clip: action_screenshot_params.Clip | NotGiven = NOT_GIVEN,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        type: Literal["png", "jpeg"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionScreenshotResponse:
        """
        Args:
          clip: clip of the screenshot

          output_format: Type of the URI

          type: Action type for screenshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/screenshot",
            body=await async_maybe_transform(
                {
                    "clip": clip,
                    "output_format": output_format,
                    "type": type,
                },
                action_screenshot_params.ActionScreenshotParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionScreenshotResponse,
        )

    async def scroll(
        self,
        id: str,
        *,
        scroll_x: float,
        scroll_y: float,
        type: object,
        x: float,
        y: float,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          scroll_x: Horizontal scroll amount

          scroll_y: Vertical scroll amount

          type: Action type for scroll interaction

          x: X coordinate of the scroll position

          y: Y coordinate of the scroll position

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/scroll",
            body=await async_maybe_transform(
                {
                    "scroll_x": scroll_x,
                    "scroll_y": scroll_y,
                    "type": type,
                    "x": x,
                    "y": y,
                    "output_format": output_format,
                },
                action_scroll_params.ActionScrollParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def touch(
        self,
        id: str,
        *,
        points: Iterable[action_touch_params.Point],
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          points: Array of touch points and their actions

          type: Action type for touch interaction

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/touch",
            body=await async_maybe_transform(
                {
                    "points": points,
                    "type": type,
                    "output_format": output_format,
                },
                action_touch_params.ActionTouchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )

    async def type(
        self,
        id: str,
        *,
        text: str,
        type: object,
        output_format: Literal["base64", "storageKey"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ActionResult:
        """
        Args:
          text: Text to type

          type: Action type for typing text

          output_format: Type of the URI

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/actions/type",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "type": type,
                    "output_format": output_format,
                },
                action_type_params.ActionTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ActionResult,
        )


class ActionsResourceWithRawResponse:
    def __init__(self, actions: ActionsResource) -> None:
        self._actions = actions

        self.click = to_raw_response_wrapper(
            actions.click,
        )
        self.drag = to_raw_response_wrapper(
            actions.drag,
        )
        self.move = to_raw_response_wrapper(
            actions.move,
        )
        self.press = to_raw_response_wrapper(
            actions.press,
        )
        self.screenshot = to_raw_response_wrapper(
            actions.screenshot,
        )
        self.scroll = to_raw_response_wrapper(
            actions.scroll,
        )
        self.touch = to_raw_response_wrapper(
            actions.touch,
        )
        self.type = to_raw_response_wrapper(
            actions.type,
        )


class AsyncActionsResourceWithRawResponse:
    def __init__(self, actions: AsyncActionsResource) -> None:
        self._actions = actions

        self.click = async_to_raw_response_wrapper(
            actions.click,
        )
        self.drag = async_to_raw_response_wrapper(
            actions.drag,
        )
        self.move = async_to_raw_response_wrapper(
            actions.move,
        )
        self.press = async_to_raw_response_wrapper(
            actions.press,
        )
        self.screenshot = async_to_raw_response_wrapper(
            actions.screenshot,
        )
        self.scroll = async_to_raw_response_wrapper(
            actions.scroll,
        )
        self.touch = async_to_raw_response_wrapper(
            actions.touch,
        )
        self.type = async_to_raw_response_wrapper(
            actions.type,
        )


class ActionsResourceWithStreamingResponse:
    def __init__(self, actions: ActionsResource) -> None:
        self._actions = actions

        self.click = to_streamed_response_wrapper(
            actions.click,
        )
        self.drag = to_streamed_response_wrapper(
            actions.drag,
        )
        self.move = to_streamed_response_wrapper(
            actions.move,
        )
        self.press = to_streamed_response_wrapper(
            actions.press,
        )
        self.screenshot = to_streamed_response_wrapper(
            actions.screenshot,
        )
        self.scroll = to_streamed_response_wrapper(
            actions.scroll,
        )
        self.touch = to_streamed_response_wrapper(
            actions.touch,
        )
        self.type = to_streamed_response_wrapper(
            actions.type,
        )


class AsyncActionsResourceWithStreamingResponse:
    def __init__(self, actions: AsyncActionsResource) -> None:
        self._actions = actions

        self.click = async_to_streamed_response_wrapper(
            actions.click,
        )
        self.drag = async_to_streamed_response_wrapper(
            actions.drag,
        )
        self.move = async_to_streamed_response_wrapper(
            actions.move,
        )
        self.press = async_to_streamed_response_wrapper(
            actions.press,
        )
        self.screenshot = async_to_streamed_response_wrapper(
            actions.screenshot,
        )
        self.scroll = async_to_streamed_response_wrapper(
            actions.scroll,
        )
        self.touch = async_to_streamed_response_wrapper(
            actions.touch,
        )
        self.type = async_to_streamed_response_wrapper(
            actions.type,
        )
