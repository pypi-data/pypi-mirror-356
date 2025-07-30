# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
from typing_extensions import Literal, overload

import httpx

from .fs import (
    FsResource,
    AsyncFsResource,
    FsResourceWithRawResponse,
    AsyncFsResourceWithRawResponse,
    FsResourceWithStreamingResponse,
    AsyncFsResourceWithStreamingResponse,
)
from .actions import (
    ActionsResource,
    AsyncActionsResource,
    ActionsResourceWithRawResponse,
    AsyncActionsResourceWithRawResponse,
    ActionsResourceWithStreamingResponse,
    AsyncActionsResourceWithStreamingResponse,
)
from .browser import (
    BrowserResource,
    AsyncBrowserResource,
    BrowserResourceWithRawResponse,
    AsyncBrowserResourceWithRawResponse,
    BrowserResourceWithStreamingResponse,
    AsyncBrowserResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import required_args, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ....types.v1 import (
    box_list_params,
    box_create_params,
    box_run_code_params,
    box_create_linux_params,
    box_create_android_params,
    box_execute_commands_params,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.v1.linux_box import LinuxBox
from ....types.v1.android_box import AndroidBox
from ....types.v1.box_list_response import BoxListResponse
from ....types.v1.box_stop_response import BoxStopResponse
from ....types.v1.box_start_response import BoxStartResponse
from ....types.v1.box_create_response import BoxCreateResponse
from ....types.v1.box_retrieve_response import BoxRetrieveResponse
from ....types.v1.box_run_code_response import BoxRunCodeResponse
from ....types.v1.create_box_config_param import CreateBoxConfigParam
from ....types.v1.box_execute_commands_response import BoxExecuteCommandsResponse

__all__ = ["BoxesResource", "AsyncBoxesResource"]


class BoxesResource(SyncAPIResource):
    @cached_property
    def actions(self) -> ActionsResource:
        return ActionsResource(self._client)

    @cached_property
    def fs(self) -> FsResource:
        return FsResource(self._client)

    @cached_property
    def browser(self) -> BrowserResource:
        return BrowserResource(self._client)

    @cached_property
    def with_raw_response(self) -> BoxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#accessing-raw-response-data-eg-headers
        """
        return BoxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BoxesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#with_streaming_response
        """
        return BoxesResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        type: Literal["linux"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        """
        Create box

        Args:
          type: Box type is Linux

          config: Configuration for a Linux box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        type: Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        """
        Create box

        Args:
          type: Box type is Android

          config: Configuration for an Android box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["type"])
    def create(
        self,
        *,
        type: Literal["linux"] | Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        return cast(
            BoxCreateResponse,
            self._post(
                "/api/v1/boxes",
                body=maybe_transform(
                    {
                        "type": type,
                        "config": config,
                    },
                    box_create_params.BoxCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxCreateResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxRetrieveResponse:
        """
        Get box detail

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxRetrieveResponse,
            self._get(
                f"/api/v1/boxes/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, BoxRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        page: float,
        page_size: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxListResponse:
        """
        List box

        Args:
          page: Page number

          page_size: Page size

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v1/boxes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    box_list_params.BoxListParams,
                ),
            ),
            cast_to=BoxListResponse,
        )

    def create_android(
        self,
        *,
        type: Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AndroidBox:
        """
        Create android box

        Args:
          type: Box type is Android

          config: Configuration for an Android box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/boxes/android",
            body=maybe_transform(
                {
                    "type": type,
                    "config": config,
                },
                box_create_android_params.BoxCreateAndroidParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AndroidBox,
        )

    def create_linux(
        self,
        *,
        type: Literal["linux"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LinuxBox:
        """
        Create linux box

        Args:
          type: Box type is Linux

          config: Configuration for a Linux box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/boxes/linux",
            body=maybe_transform(
                {
                    "type": type,
                    "config": config,
                },
                box_create_linux_params.BoxCreateLinuxParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LinuxBox,
        )

    def execute_commands(
        self,
        id: str,
        *,
        commands: List[str],
        envs: object | NotGiven = NOT_GIVEN,
        api_timeout: str | NotGiven = NOT_GIVEN,
        working_dir: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxExecuteCommandsResponse:
        """
        Args:
          commands: The command to run

          envs: The environment variables to run the command

          api_timeout: The timeout of the command. e.g. '30s'

          working_dir: The working directory of the command

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/commands",
            body=maybe_transform(
                {
                    "commands": commands,
                    "envs": envs,
                    "api_timeout": api_timeout,
                    "working_dir": working_dir,
                },
                box_execute_commands_params.BoxExecuteCommandsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BoxExecuteCommandsResponse,
        )

    def run_code(
        self,
        id: str,
        *,
        code: str,
        type: Literal["bash", "python3", "typescript"],
        argv: List[str] | NotGiven = NOT_GIVEN,
        envs: object | NotGiven = NOT_GIVEN,
        api_timeout: str | NotGiven = NOT_GIVEN,
        working_dir: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxRunCodeResponse:
        """
        Args:
          code: The code to run

          type: The type of the code.

          argv: The arguments to run the code. e.g. ["-h"]

          envs: The environment variables to run the code

          api_timeout: The timeout of the code. e.g. "30s"

          working_dir: The working directory of the code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v1/boxes/{id}/run-code",
            body=maybe_transform(
                {
                    "code": code,
                    "type": type,
                    "argv": argv,
                    "envs": envs,
                    "api_timeout": api_timeout,
                    "working_dir": working_dir,
                },
                box_run_code_params.BoxRunCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BoxRunCodeResponse,
        )

    def start(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxStartResponse:
        """
        Start box

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxStartResponse,
            self._post(
                f"/api/v1/boxes/{id}/start",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxStartResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def stop(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxStopResponse:
        """
        Stop box

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxStopResponse,
            self._post(
                f"/api/v1/boxes/{id}/stop",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxStopResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncBoxesResource(AsyncAPIResource):
    @cached_property
    def actions(self) -> AsyncActionsResource:
        return AsyncActionsResource(self._client)

    @cached_property
    def fs(self) -> AsyncFsResource:
        return AsyncFsResource(self._client)

    @cached_property
    def browser(self) -> AsyncBrowserResource:
        return AsyncBrowserResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBoxesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#accessing-raw-response-data-eg-headers
        """
        return AsyncBoxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBoxesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/babelcloud/gbox-sdk-py#with_streaming_response
        """
        return AsyncBoxesResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        type: Literal["linux"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        """
        Create box

        Args:
          type: Box type is Linux

          config: Configuration for a Linux box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        type: Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        """
        Create box

        Args:
          type: Box type is Android

          config: Configuration for an Android box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["type"])
    async def create(
        self,
        *,
        type: Literal["linux"] | Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxCreateResponse:
        return cast(
            BoxCreateResponse,
            await self._post(
                "/api/v1/boxes",
                body=await async_maybe_transform(
                    {
                        "type": type,
                        "config": config,
                    },
                    box_create_params.BoxCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxCreateResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxRetrieveResponse:
        """
        Get box detail

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxRetrieveResponse,
            await self._get(
                f"/api/v1/boxes/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, BoxRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        page: float,
        page_size: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxListResponse:
        """
        List box

        Args:
          page: Page number

          page_size: Page size

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v1/boxes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                    },
                    box_list_params.BoxListParams,
                ),
            ),
            cast_to=BoxListResponse,
        )

    async def create_android(
        self,
        *,
        type: Literal["android"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AndroidBox:
        """
        Create android box

        Args:
          type: Box type is Android

          config: Configuration for an Android box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/boxes/android",
            body=await async_maybe_transform(
                {
                    "type": type,
                    "config": config,
                },
                box_create_android_params.BoxCreateAndroidParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AndroidBox,
        )

    async def create_linux(
        self,
        *,
        type: Literal["linux"],
        config: CreateBoxConfigParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LinuxBox:
        """
        Create linux box

        Args:
          type: Box type is Linux

          config: Configuration for a Linux box instance

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/boxes/linux",
            body=await async_maybe_transform(
                {
                    "type": type,
                    "config": config,
                },
                box_create_linux_params.BoxCreateLinuxParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LinuxBox,
        )

    async def execute_commands(
        self,
        id: str,
        *,
        commands: List[str],
        envs: object | NotGiven = NOT_GIVEN,
        api_timeout: str | NotGiven = NOT_GIVEN,
        working_dir: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxExecuteCommandsResponse:
        """
        Args:
          commands: The command to run

          envs: The environment variables to run the command

          api_timeout: The timeout of the command. e.g. '30s'

          working_dir: The working directory of the command

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/commands",
            body=await async_maybe_transform(
                {
                    "commands": commands,
                    "envs": envs,
                    "api_timeout": api_timeout,
                    "working_dir": working_dir,
                },
                box_execute_commands_params.BoxExecuteCommandsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BoxExecuteCommandsResponse,
        )

    async def run_code(
        self,
        id: str,
        *,
        code: str,
        type: Literal["bash", "python3", "typescript"],
        argv: List[str] | NotGiven = NOT_GIVEN,
        envs: object | NotGiven = NOT_GIVEN,
        api_timeout: str | NotGiven = NOT_GIVEN,
        working_dir: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxRunCodeResponse:
        """
        Args:
          code: The code to run

          type: The type of the code.

          argv: The arguments to run the code. e.g. ["-h"]

          envs: The environment variables to run the code

          api_timeout: The timeout of the code. e.g. "30s"

          working_dir: The working directory of the code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v1/boxes/{id}/run-code",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "type": type,
                    "argv": argv,
                    "envs": envs,
                    "api_timeout": api_timeout,
                    "working_dir": working_dir,
                },
                box_run_code_params.BoxRunCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BoxRunCodeResponse,
        )

    async def start(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxStartResponse:
        """
        Start box

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxStartResponse,
            await self._post(
                f"/api/v1/boxes/{id}/start",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxStartResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def stop(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BoxStopResponse:
        """
        Stop box

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            BoxStopResponse,
            await self._post(
                f"/api/v1/boxes/{id}/stop",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, BoxStopResponse),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class BoxesResourceWithRawResponse:
    def __init__(self, boxes: BoxesResource) -> None:
        self._boxes = boxes

        self.create = to_raw_response_wrapper(
            boxes.create,
        )
        self.retrieve = to_raw_response_wrapper(
            boxes.retrieve,
        )
        self.list = to_raw_response_wrapper(
            boxes.list,
        )
        self.create_android = to_raw_response_wrapper(
            boxes.create_android,
        )
        self.create_linux = to_raw_response_wrapper(
            boxes.create_linux,
        )
        self.execute_commands = to_raw_response_wrapper(
            boxes.execute_commands,
        )
        self.run_code = to_raw_response_wrapper(
            boxes.run_code,
        )
        self.start = to_raw_response_wrapper(
            boxes.start,
        )
        self.stop = to_raw_response_wrapper(
            boxes.stop,
        )

    @cached_property
    def actions(self) -> ActionsResourceWithRawResponse:
        return ActionsResourceWithRawResponse(self._boxes.actions)

    @cached_property
    def fs(self) -> FsResourceWithRawResponse:
        return FsResourceWithRawResponse(self._boxes.fs)

    @cached_property
    def browser(self) -> BrowserResourceWithRawResponse:
        return BrowserResourceWithRawResponse(self._boxes.browser)


class AsyncBoxesResourceWithRawResponse:
    def __init__(self, boxes: AsyncBoxesResource) -> None:
        self._boxes = boxes

        self.create = async_to_raw_response_wrapper(
            boxes.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            boxes.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            boxes.list,
        )
        self.create_android = async_to_raw_response_wrapper(
            boxes.create_android,
        )
        self.create_linux = async_to_raw_response_wrapper(
            boxes.create_linux,
        )
        self.execute_commands = async_to_raw_response_wrapper(
            boxes.execute_commands,
        )
        self.run_code = async_to_raw_response_wrapper(
            boxes.run_code,
        )
        self.start = async_to_raw_response_wrapper(
            boxes.start,
        )
        self.stop = async_to_raw_response_wrapper(
            boxes.stop,
        )

    @cached_property
    def actions(self) -> AsyncActionsResourceWithRawResponse:
        return AsyncActionsResourceWithRawResponse(self._boxes.actions)

    @cached_property
    def fs(self) -> AsyncFsResourceWithRawResponse:
        return AsyncFsResourceWithRawResponse(self._boxes.fs)

    @cached_property
    def browser(self) -> AsyncBrowserResourceWithRawResponse:
        return AsyncBrowserResourceWithRawResponse(self._boxes.browser)


class BoxesResourceWithStreamingResponse:
    def __init__(self, boxes: BoxesResource) -> None:
        self._boxes = boxes

        self.create = to_streamed_response_wrapper(
            boxes.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            boxes.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            boxes.list,
        )
        self.create_android = to_streamed_response_wrapper(
            boxes.create_android,
        )
        self.create_linux = to_streamed_response_wrapper(
            boxes.create_linux,
        )
        self.execute_commands = to_streamed_response_wrapper(
            boxes.execute_commands,
        )
        self.run_code = to_streamed_response_wrapper(
            boxes.run_code,
        )
        self.start = to_streamed_response_wrapper(
            boxes.start,
        )
        self.stop = to_streamed_response_wrapper(
            boxes.stop,
        )

    @cached_property
    def actions(self) -> ActionsResourceWithStreamingResponse:
        return ActionsResourceWithStreamingResponse(self._boxes.actions)

    @cached_property
    def fs(self) -> FsResourceWithStreamingResponse:
        return FsResourceWithStreamingResponse(self._boxes.fs)

    @cached_property
    def browser(self) -> BrowserResourceWithStreamingResponse:
        return BrowserResourceWithStreamingResponse(self._boxes.browser)


class AsyncBoxesResourceWithStreamingResponse:
    def __init__(self, boxes: AsyncBoxesResource) -> None:
        self._boxes = boxes

        self.create = async_to_streamed_response_wrapper(
            boxes.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            boxes.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            boxes.list,
        )
        self.create_android = async_to_streamed_response_wrapper(
            boxes.create_android,
        )
        self.create_linux = async_to_streamed_response_wrapper(
            boxes.create_linux,
        )
        self.execute_commands = async_to_streamed_response_wrapper(
            boxes.execute_commands,
        )
        self.run_code = async_to_streamed_response_wrapper(
            boxes.run_code,
        )
        self.start = async_to_streamed_response_wrapper(
            boxes.start,
        )
        self.stop = async_to_streamed_response_wrapper(
            boxes.stop,
        )

    @cached_property
    def actions(self) -> AsyncActionsResourceWithStreamingResponse:
        return AsyncActionsResourceWithStreamingResponse(self._boxes.actions)

    @cached_property
    def fs(self) -> AsyncFsResourceWithStreamingResponse:
        return AsyncFsResourceWithStreamingResponse(self._boxes.fs)

    @cached_property
    def browser(self) -> AsyncBrowserResourceWithStreamingResponse:
        return AsyncBrowserResourceWithStreamingResponse(self._boxes.browser)
