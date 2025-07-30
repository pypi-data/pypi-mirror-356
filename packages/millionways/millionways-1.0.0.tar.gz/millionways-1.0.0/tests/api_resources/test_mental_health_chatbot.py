# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from millionways import Millionways, AsyncMillionways
from tests.utils import assert_matches_type
from millionways.types import (
    MentalHealthChatbotGenerateResponseResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMentalHealthChatbot:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_response(self, client: Millionways) -> None:
        mental_health_chatbot = client.mental_health_chatbot.generate_response(
            api_key="apiKey",
        )
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_response_with_all_params(self, client: Millionways) -> None:
        mental_health_chatbot = client.mental_health_chatbot.generate_response(
            api_key="apiKey",
            language="en",
            levels={
                "level1": 20,
                "level2": 20,
                "level3": 20,
                "level4": 20,
                "level5": 20,
            },
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                },
                {
                    "role": "assistant",
                    "content": "Hi, how are you?",
                },
            ],
            result={
                "emotions": {
                    "approach": 50,
                    "avoidance": 50,
                },
                "motives": {
                    "achievement": 0,
                    "contact": 100,
                    "power": 0,
                },
                "preferences": {
                    "analytical": 50,
                    "detail": 50,
                    "external": 100,
                    "goal": 100,
                    "holistic": 50,
                    "internal": 0,
                    "path": 0,
                    "realization": 50,
                },
            },
        )
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_response(self, client: Millionways) -> None:
        response = client.mental_health_chatbot.with_raw_response.generate_response(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mental_health_chatbot = response.parse()
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_response(self, client: Millionways) -> None:
        with client.mental_health_chatbot.with_streaming_response.generate_response(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mental_health_chatbot = response.parse()
            assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMentalHealthChatbot:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_response(self, async_client: AsyncMillionways) -> None:
        mental_health_chatbot = await async_client.mental_health_chatbot.generate_response(
            api_key="apiKey",
        )
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_response_with_all_params(self, async_client: AsyncMillionways) -> None:
        mental_health_chatbot = await async_client.mental_health_chatbot.generate_response(
            api_key="apiKey",
            language="en",
            levels={
                "level1": 20,
                "level2": 20,
                "level3": 20,
                "level4": 20,
                "level5": 20,
            },
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                },
                {
                    "role": "assistant",
                    "content": "Hi, how are you?",
                },
            ],
            result={
                "emotions": {
                    "approach": 50,
                    "avoidance": 50,
                },
                "motives": {
                    "achievement": 0,
                    "contact": 100,
                    "power": 0,
                },
                "preferences": {
                    "analytical": 50,
                    "detail": 50,
                    "external": 100,
                    "goal": 100,
                    "holistic": 50,
                    "internal": 0,
                    "path": 0,
                    "realization": 50,
                },
            },
        )
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_response(self, async_client: AsyncMillionways) -> None:
        response = await async_client.mental_health_chatbot.with_raw_response.generate_response(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mental_health_chatbot = await response.parse()
        assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_response(self, async_client: AsyncMillionways) -> None:
        async with async_client.mental_health_chatbot.with_streaming_response.generate_response(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mental_health_chatbot = await response.parse()
            assert_matches_type(MentalHealthChatbotGenerateResponseResponse, mental_health_chatbot, path=["response"])

        assert cast(Any, response.is_closed) is True
