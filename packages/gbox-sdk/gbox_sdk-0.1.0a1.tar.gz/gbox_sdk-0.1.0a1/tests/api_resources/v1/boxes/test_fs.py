# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gbox_sdk import GboxClient, AsyncGboxClient
from tests.utils import assert_matches_type
from gbox_sdk.types.v1.boxes import (
    FListResponse,
    FReadResponse,
    FWriteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: GboxClient) -> None:
        f = client.v1.boxes.fs.list(
            id="id",
            path="path",
        )
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: GboxClient) -> None:
        f = client.v1.boxes.fs.list(
            id="id",
            path="path",
            depth=0,
        )
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: GboxClient) -> None:
        response = client.v1.boxes.fs.with_raw_response.list(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = response.parse()
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: GboxClient) -> None:
        with client.v1.boxes.fs.with_streaming_response.list(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = response.parse()
            assert_matches_type(FListResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.fs.with_raw_response.list(
                id="",
                path="path",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_read(self, client: GboxClient) -> None:
        f = client.v1.boxes.fs.read(
            id="id",
            path="path",
        )
        assert_matches_type(FReadResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_read(self, client: GboxClient) -> None:
        response = client.v1.boxes.fs.with_raw_response.read(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = response.parse()
        assert_matches_type(FReadResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_read(self, client: GboxClient) -> None:
        with client.v1.boxes.fs.with_streaming_response.read(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = response.parse()
            assert_matches_type(FReadResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_read(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.fs.with_raw_response.read(
                id="",
                path="path",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_write(self, client: GboxClient) -> None:
        f = client.v1.boxes.fs.write(
            id="id",
            content="content",
            path="path",
        )
        assert_matches_type(FWriteResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_write(self, client: GboxClient) -> None:
        response = client.v1.boxes.fs.with_raw_response.write(
            id="id",
            content="content",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = response.parse()
        assert_matches_type(FWriteResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_write(self, client: GboxClient) -> None:
        with client.v1.boxes.fs.with_streaming_response.write(
            id="id",
            content="content",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = response.parse()
            assert_matches_type(FWriteResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_write(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.fs.with_raw_response.write(
                id="",
                content="content",
                path="path",
            )


class TestAsyncFs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGboxClient) -> None:
        f = await async_client.v1.boxes.fs.list(
            id="id",
            path="path",
        )
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGboxClient) -> None:
        f = await async_client.v1.boxes.fs.list(
            id="id",
            path="path",
            depth=0,
        )
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.fs.with_raw_response.list(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = await response.parse()
        assert_matches_type(FListResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.fs.with_streaming_response.list(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = await response.parse()
            assert_matches_type(FListResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.fs.with_raw_response.list(
                id="",
                path="path",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_read(self, async_client: AsyncGboxClient) -> None:
        f = await async_client.v1.boxes.fs.read(
            id="id",
            path="path",
        )
        assert_matches_type(FReadResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_read(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.fs.with_raw_response.read(
            id="id",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = await response.parse()
        assert_matches_type(FReadResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_read(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.fs.with_streaming_response.read(
            id="id",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = await response.parse()
            assert_matches_type(FReadResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_read(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.fs.with_raw_response.read(
                id="",
                path="path",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_write(self, async_client: AsyncGboxClient) -> None:
        f = await async_client.v1.boxes.fs.write(
            id="id",
            content="content",
            path="path",
        )
        assert_matches_type(FWriteResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_write(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.fs.with_raw_response.write(
            id="id",
            content="content",
            path="path",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        f = await response.parse()
        assert_matches_type(FWriteResponse, f, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_write(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.fs.with_streaming_response.write(
            id="id",
            content="content",
            path="path",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            f = await response.parse()
            assert_matches_type(FWriteResponse, f, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_write(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.fs.with_raw_response.write(
                id="",
                content="content",
                path="path",
            )
