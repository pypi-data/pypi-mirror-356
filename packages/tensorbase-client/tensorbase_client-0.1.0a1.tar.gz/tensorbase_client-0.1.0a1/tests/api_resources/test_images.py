# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from tensorbase_client import Tensorbase, AsyncTensorbase
from tensorbase_client.types import ImageGenerateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate(self, client: Tensorbase) -> None:
        image = client.images.generate(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_with_all_params(self, client: Tensorbase) -> None:
        image = client.images.generate(
            model="model",
            prompt="prompt",
            n=0,
            response_format="response_format",
            size="size",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate(self, client: Tensorbase) -> None:
        response = client.images.with_raw_response.generate(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate(self, client: Tensorbase) -> None:
        with client.images.with_streaming_response.generate(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImageGenerateResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncImages:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate(self, async_client: AsyncTensorbase) -> None:
        image = await async_client.images.generate(
            model="model",
            prompt="prompt",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncTensorbase) -> None:
        image = await async_client.images.generate(
            model="model",
            prompt="prompt",
            n=0,
            response_format="response_format",
            size="size",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncTensorbase) -> None:
        response = await async_client.images.with_raw_response.generate(
            model="model",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncTensorbase) -> None:
        async with async_client.images.with_streaming_response.generate(
            model="model",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImageGenerateResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True
