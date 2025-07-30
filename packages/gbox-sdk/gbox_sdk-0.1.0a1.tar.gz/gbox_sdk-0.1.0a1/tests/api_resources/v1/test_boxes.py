# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gbox_sdk import GboxClient, AsyncGboxClient
from tests.utils import assert_matches_type
from gbox_sdk.types.v1 import (
    LinuxBox,
    AndroidBox,
    BoxListResponse,
    BoxStopResponse,
    BoxStartResponse,
    BoxCreateResponse,
    BoxRunCodeResponse,
    BoxRetrieveResponse,
    BoxExecuteCommandsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBoxes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_overload_1(self, client: GboxClient) -> None:
        box = client.v1.boxes.create(
            type="linux",
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: GboxClient) -> None:
        box = client.v1.boxes.create(
            type="linux",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_overload_1(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.create(
            type="linux",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_overload_1(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.create(
            type="linux",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxCreateResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_overload_2(self, client: GboxClient) -> None:
        box = client.v1.boxes.create(
            type="android",
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: GboxClient) -> None:
        box = client.v1.boxes.create(
            type="android",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_overload_2(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.create(
            type="android",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_overload_2(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.create(
            type="android",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxCreateResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: GboxClient) -> None:
        box = client.v1.boxes.retrieve(
            "id",
        )
        assert_matches_type(BoxRetrieveResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxRetrieveResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxRetrieveResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: GboxClient) -> None:
        box = client.v1.boxes.list(
            page=0,
            page_size=0,
        )
        assert_matches_type(BoxListResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.list(
            page=0,
            page_size=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxListResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.list(
            page=0,
            page_size=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxListResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_android(self, client: GboxClient) -> None:
        box = client.v1.boxes.create_android(
            type="android",
        )
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_android_with_all_params(self, client: GboxClient) -> None:
        box = client.v1.boxes.create_android(
            type="android",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_android(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.create_android(
            type="android",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_android(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.create_android(
            type="android",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(AndroidBox, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_linux(self, client: GboxClient) -> None:
        box = client.v1.boxes.create_linux(
            type="linux",
        )
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_linux_with_all_params(self, client: GboxClient) -> None:
        box = client.v1.boxes.create_linux(
            type="linux",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_linux(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.create_linux(
            type="linux",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_linux(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.create_linux(
            type="linux",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(LinuxBox, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_commands(self, client: GboxClient) -> None:
        box = client.v1.boxes.execute_commands(
            id="id",
            commands=["ls", "-l"],
        )
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_commands_with_all_params(self, client: GboxClient) -> None:
        box = client.v1.boxes.execute_commands(
            id="id",
            commands=["ls", "-l"],
            envs={},
            api_timeout="30s",
            working_dir="workingDir",
        )
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_execute_commands(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.execute_commands(
            id="id",
            commands=["ls", "-l"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_execute_commands(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.execute_commands(
            id="id",
            commands=["ls", "-l"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_execute_commands(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.with_raw_response.execute_commands(
                id="",
                commands=["ls", "-l"],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_run_code(self, client: GboxClient) -> None:
        box = client.v1.boxes.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        )
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_run_code_with_all_params(self, client: GboxClient) -> None:
        box = client.v1.boxes.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
            argv=["string"],
            envs={},
            api_timeout="timeout",
            working_dir="workingDir",
        )
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_run_code(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_run_code(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxRunCodeResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_run_code(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.with_raw_response.run_code(
                id="",
                code='print("Hello, World!")',
                type="bash",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_start(self, client: GboxClient) -> None:
        box = client.v1.boxes.start(
            "id",
        )
        assert_matches_type(BoxStartResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_start(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.start(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxStartResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_start(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.start(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxStartResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_start(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.with_raw_response.start(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_stop(self, client: GboxClient) -> None:
        box = client.v1.boxes.stop(
            "id",
        )
        assert_matches_type(BoxStopResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_stop(self, client: GboxClient) -> None:
        response = client.v1.boxes.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = response.parse()
        assert_matches_type(BoxStopResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_stop(self, client: GboxClient) -> None:
        with client.v1.boxes.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = response.parse()
            assert_matches_type(BoxStopResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_stop(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.with_raw_response.stop(
                "",
            )


class TestAsyncBoxes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create(
            type="linux",
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create(
            type="linux",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.create(
            type="linux",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.create(
            type="linux",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxCreateResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create(
            type="android",
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create(
            type="android",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.create(
            type="android",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxCreateResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.create(
            type="android",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxCreateResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.retrieve(
            "id",
        )
        assert_matches_type(BoxRetrieveResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxRetrieveResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxRetrieveResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.list(
            page=0,
            page_size=0,
        )
        assert_matches_type(BoxListResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.list(
            page=0,
            page_size=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxListResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.list(
            page=0,
            page_size=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxListResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_android(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create_android(
            type="android",
        )
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_android_with_all_params(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create_android(
            type="android",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_android(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.create_android(
            type="android",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(AndroidBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_android(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.create_android(
            type="android",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(AndroidBox, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_linux(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create_linux(
            type="linux",
        )
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_linux_with_all_params(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.create_linux(
            type="linux",
            config={
                "envs": {},
                "expires_in": "expiresIn",
                "labels": {},
            },
        )
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_linux(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.create_linux(
            type="linux",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(LinuxBox, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_linux(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.create_linux(
            type="linux",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(LinuxBox, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_commands(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.execute_commands(
            id="id",
            commands=["ls", "-l"],
        )
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_commands_with_all_params(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.execute_commands(
            id="id",
            commands=["ls", "-l"],
            envs={},
            api_timeout="30s",
            working_dir="workingDir",
        )
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_execute_commands(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.execute_commands(
            id="id",
            commands=["ls", "-l"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_execute_commands(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.execute_commands(
            id="id",
            commands=["ls", "-l"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxExecuteCommandsResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_execute_commands(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.with_raw_response.execute_commands(
                id="",
                commands=["ls", "-l"],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_run_code(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        )
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_run_code_with_all_params(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
            argv=["string"],
            envs={},
            api_timeout="timeout",
            working_dir="workingDir",
        )
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_run_code(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxRunCodeResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_run_code(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.run_code(
            id="id",
            code='print("Hello, World!")',
            type="bash",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxRunCodeResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_run_code(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.with_raw_response.run_code(
                id="",
                code='print("Hello, World!")',
                type="bash",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_start(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.start(
            "id",
        )
        assert_matches_type(BoxStartResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.start(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxStartResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.start(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxStartResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_start(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.with_raw_response.start(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_stop(self, async_client: AsyncGboxClient) -> None:
        box = await async_client.v1.boxes.stop(
            "id",
        )
        assert_matches_type(BoxStopResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.with_raw_response.stop(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        box = await response.parse()
        assert_matches_type(BoxStopResponse, box, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.with_streaming_response.stop(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            box = await response.parse()
            assert_matches_type(BoxStopResponse, box, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_stop(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.with_raw_response.stop(
                "",
            )
