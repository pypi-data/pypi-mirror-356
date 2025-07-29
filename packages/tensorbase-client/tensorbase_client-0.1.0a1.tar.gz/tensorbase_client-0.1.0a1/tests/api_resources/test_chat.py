# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from tensorbase_client import Tensorbase, AsyncTensorbase
from tensorbase_client.types import ChatGenerateCompletionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_completion(self, client: Tensorbase) -> None:
        chat = client.chat.generate_completion(
            messages=[{}],
            model="model",
        )
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_completion_with_all_params(self, client: Tensorbase) -> None:
        chat = client.chat.generate_completion(
            messages=[
                {
                    "content": "content",
                    "name": "name",
                    "role": "system",
                    "tool_calls": [{}],
                }
            ],
            model="model",
            max_tokens=0,
            stream=True,
            temperature=0,
            tool_choice="tool_choice",
            tools=[{}],
        )
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_completion(self, client: Tensorbase) -> None:
        response = client.chat.with_raw_response.generate_completion(
            messages=[{}],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_completion(self, client: Tensorbase) -> None:
        with client.chat.with_streaming_response.generate_completion(
            messages=[{}],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_completion(self, async_client: AsyncTensorbase) -> None:
        chat = await async_client.chat.generate_completion(
            messages=[{}],
            model="model",
        )
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_completion_with_all_params(self, async_client: AsyncTensorbase) -> None:
        chat = await async_client.chat.generate_completion(
            messages=[
                {
                    "content": "content",
                    "name": "name",
                    "role": "system",
                    "tool_calls": [{}],
                }
            ],
            model="model",
            max_tokens=0,
            stream=True,
            temperature=0,
            tool_choice="tool_choice",
            tools=[{}],
        )
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_completion(self, async_client: AsyncTensorbase) -> None:
        response = await async_client.chat.with_raw_response.generate_completion(
            messages=[{}],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_completion(self, async_client: AsyncTensorbase) -> None:
        async with async_client.chat.with_streaming_response.generate_completion(
            messages=[{}],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatGenerateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True
