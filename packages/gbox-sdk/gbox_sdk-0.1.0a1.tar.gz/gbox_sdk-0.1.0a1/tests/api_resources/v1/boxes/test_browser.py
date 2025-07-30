# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gbox_sdk import GboxClient, AsyncGboxClient
from tests.utils import assert_matches_type
from gbox_sdk.types.v1.boxes import BrowserConnectURLResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBrowser:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_cdp_url(self, client: GboxClient) -> None:
        browser = client.v1.boxes.browser.cdp_url(
            "id",
        )
        assert_matches_type(str, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cdp_url(self, client: GboxClient) -> None:
        response = client.v1.boxes.browser.with_raw_response.cdp_url(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = response.parse()
        assert_matches_type(str, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cdp_url(self, client: GboxClient) -> None:
        with client.v1.boxes.browser.with_streaming_response.cdp_url(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = response.parse()
            assert_matches_type(str, browser, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cdp_url(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.browser.with_raw_response.cdp_url(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_connect_url(self, client: GboxClient) -> None:
        browser = client.v1.boxes.browser.connect_url(
            "id",
        )
        assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_connect_url(self, client: GboxClient) -> None:
        response = client.v1.boxes.browser.with_raw_response.connect_url(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = response.parse()
        assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_connect_url(self, client: GboxClient) -> None:
        with client.v1.boxes.browser.with_streaming_response.connect_url(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = response.parse()
            assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_connect_url(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.browser.with_raw_response.connect_url(
                "",
            )


class TestAsyncBrowser:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_cdp_url(self, async_client: AsyncGboxClient) -> None:
        browser = await async_client.v1.boxes.browser.cdp_url(
            "id",
        )
        assert_matches_type(str, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cdp_url(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.browser.with_raw_response.cdp_url(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = await response.parse()
        assert_matches_type(str, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cdp_url(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.browser.with_streaming_response.cdp_url(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = await response.parse()
            assert_matches_type(str, browser, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cdp_url(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.browser.with_raw_response.cdp_url(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_connect_url(self, async_client: AsyncGboxClient) -> None:
        browser = await async_client.v1.boxes.browser.connect_url(
            "id",
        )
        assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_connect_url(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.browser.with_raw_response.connect_url(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = await response.parse()
        assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_connect_url(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.browser.with_streaming_response.connect_url(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = await response.parse()
            assert_matches_type(BrowserConnectURLResponse, browser, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_connect_url(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.browser.with_raw_response.connect_url(
                "",
            )
