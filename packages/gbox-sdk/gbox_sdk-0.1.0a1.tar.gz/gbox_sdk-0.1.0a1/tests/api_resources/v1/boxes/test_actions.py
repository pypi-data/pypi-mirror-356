# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gbox_sdk import GboxClient, AsyncGboxClient
from tests.utils import assert_matches_type
from gbox_sdk.types.v1.boxes import (
    ActionResult,
    ActionScreenshotResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestActions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_click(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.click(
            id="id",
            type={},
            x=100,
            y=100,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_click_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.click(
            id="id",
            type={},
            x=100,
            y=100,
            button="left",
            double=True,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_click(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.click(
            id="id",
            type={},
            x=100,
            y=100,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_click(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.click(
            id="id",
            type={},
            x=100,
            y=100,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_click(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.click(
                id="",
                type={},
                x=100,
                y=100,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_drag(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_drag_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
            duration="duration",
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_drag(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_drag(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_drag(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.drag(
                id="",
                path=[
                    {
                        "x": 100,
                        "y": 100,
                    },
                    {
                        "x": 200,
                        "y": 200,
                    },
                ],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_move(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.move(
            id="id",
            type={},
            x=200,
            y=300,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_move_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.move(
            id="id",
            type={},
            x=200,
            y=300,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_move(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.move(
            id="id",
            type={},
            x=200,
            y=300,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_move(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.move(
            id="id",
            type={},
            x=200,
            y=300,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_move(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.move(
                id="",
                type={},
                x=200,
                y=300,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_press(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.press(
            id="id",
            keys=["Enter"],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_press_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.press(
            id="id",
            keys=["Enter"],
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_press(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.press(
            id="id",
            keys=["Enter"],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_press(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.press(
            id="id",
            keys=["Enter"],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_press(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.press(
                id="",
                keys=["Enter"],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_screenshot(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.screenshot(
            id="id",
        )
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_screenshot_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.screenshot(
            id="id",
            clip={
                "height": 0,
                "width": 0,
                "x": 0,
                "y": 0,
            },
            output_format="base64",
            type="png",
        )
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_screenshot(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.screenshot(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_screenshot(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.screenshot(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionScreenshotResponse, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_screenshot(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.screenshot(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_scroll(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_scroll_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_scroll(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_scroll(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_scroll(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.scroll(
                id="",
                scroll_x=0,
                scroll_y=100,
                type={},
                x=100,
                y=100,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_touch(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_touch_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    },
                    "actions": [{}],
                }
            ],
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_touch(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_touch(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_touch(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.touch(
                id="",
                points=[
                    {
                        "start": {
                            "x": 0,
                            "y": 0,
                        }
                    }
                ],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_type(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.type(
            id="id",
            text="Hello World",
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_type_with_all_params(self, client: GboxClient) -> None:
        action = client.v1.boxes.actions.type(
            id="id",
            text="Hello World",
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_type(self, client: GboxClient) -> None:
        response = client.v1.boxes.actions.with_raw_response.type(
            id="id",
            text="Hello World",
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_type(self, client: GboxClient) -> None:
        with client.v1.boxes.actions.with_streaming_response.type(
            id="id",
            text="Hello World",
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_type(self, client: GboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v1.boxes.actions.with_raw_response.type(
                id="",
                text="Hello World",
                type={},
            )


class TestAsyncActions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_click(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.click(
            id="id",
            type={},
            x=100,
            y=100,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_click_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.click(
            id="id",
            type={},
            x=100,
            y=100,
            button="left",
            double=True,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_click(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.click(
            id="id",
            type={},
            x=100,
            y=100,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_click(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.click(
            id="id",
            type={},
            x=100,
            y=100,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_click(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.click(
                id="",
                type={},
                x=100,
                y=100,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_drag(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_drag_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
            duration="duration",
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_drag(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_drag(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.drag(
            id="id",
            path=[
                {
                    "x": 100,
                    "y": 100,
                },
                {
                    "x": 200,
                    "y": 200,
                },
            ],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_drag(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.drag(
                id="",
                path=[
                    {
                        "x": 100,
                        "y": 100,
                    },
                    {
                        "x": 200,
                        "y": 200,
                    },
                ],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_move(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.move(
            id="id",
            type={},
            x=200,
            y=300,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_move_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.move(
            id="id",
            type={},
            x=200,
            y=300,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_move(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.move(
            id="id",
            type={},
            x=200,
            y=300,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_move(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.move(
            id="id",
            type={},
            x=200,
            y=300,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_move(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.move(
                id="",
                type={},
                x=200,
                y=300,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_press(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.press(
            id="id",
            keys=["Enter"],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_press_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.press(
            id="id",
            keys=["Enter"],
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_press(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.press(
            id="id",
            keys=["Enter"],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_press(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.press(
            id="id",
            keys=["Enter"],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_press(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.press(
                id="",
                keys=["Enter"],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_screenshot(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.screenshot(
            id="id",
        )
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_screenshot_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.screenshot(
            id="id",
            clip={
                "height": 0,
                "width": 0,
                "x": 0,
                "y": 0,
            },
            output_format="base64",
            type="png",
        )
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_screenshot(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.screenshot(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionScreenshotResponse, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_screenshot(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.screenshot(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionScreenshotResponse, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_screenshot(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.screenshot(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_scroll(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_scroll_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_scroll(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_scroll(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.scroll(
            id="id",
            scroll_x=0,
            scroll_y=100,
            type={},
            x=100,
            y=100,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_scroll(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.scroll(
                id="",
                scroll_x=0,
                scroll_y=100,
                type={},
                x=100,
                y=100,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_touch(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_touch_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    },
                    "actions": [{}],
                }
            ],
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_touch(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_touch(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.touch(
            id="id",
            points=[
                {
                    "start": {
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_touch(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.touch(
                id="",
                points=[
                    {
                        "start": {
                            "x": 0,
                            "y": 0,
                        }
                    }
                ],
                type={},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_type(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.type(
            id="id",
            text="Hello World",
            type={},
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_type_with_all_params(self, async_client: AsyncGboxClient) -> None:
        action = await async_client.v1.boxes.actions.type(
            id="id",
            text="Hello World",
            type={},
            output_format="base64",
        )
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_type(self, async_client: AsyncGboxClient) -> None:
        response = await async_client.v1.boxes.actions.with_raw_response.type(
            id="id",
            text="Hello World",
            type={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(ActionResult, action, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_type(self, async_client: AsyncGboxClient) -> None:
        async with async_client.v1.boxes.actions.with_streaming_response.type(
            id="id",
            text="Hello World",
            type={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(ActionResult, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_type(self, async_client: AsyncGboxClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v1.boxes.actions.with_raw_response.type(
                id="",
                text="Hello World",
                type={},
            )
