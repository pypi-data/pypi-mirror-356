# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from millionways import Millionways, AsyncMillionways
from tests.utils import assert_matches_type
from millionways.types import (
    CategorizeAudioCreateResponse,
    CategorizeAudioCreateForUserResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCategorizeAudio:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Millionways) -> None:
        categorize_audio = client.categorize_audio.create(
            api_key="apiKey",
        )
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Millionways) -> None:
        categorize_audio = client.categorize_audio.create(
            api_key="apiKey",
            file=b"raw file contents",
        )
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Millionways) -> None:
        response = client.categorize_audio.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        categorize_audio = response.parse()
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Millionways) -> None:
        with client.categorize_audio.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            categorize_audio = response.parse()
            assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_for_user(self, client: Millionways) -> None:
        categorize_audio = client.categorize_audio.create_for_user(
            user_id="userId",
            api_key="apiKey",
        )
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_for_user_with_all_params(self, client: Millionways) -> None:
        categorize_audio = client.categorize_audio.create_for_user(
            user_id="userId",
            api_key="apiKey",
            file=b"raw file contents",
        )
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_for_user(self, client: Millionways) -> None:
        response = client.categorize_audio.with_raw_response.create_for_user(
            user_id="userId",
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        categorize_audio = response.parse()
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_for_user(self, client: Millionways) -> None:
        with client.categorize_audio.with_streaming_response.create_for_user(
            user_id="userId",
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            categorize_audio = response.parse()
            assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_for_user(self, client: Millionways) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.categorize_audio.with_raw_response.create_for_user(
                user_id="",
                api_key="apiKey",
            )


class TestAsyncCategorizeAudio:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncMillionways) -> None:
        categorize_audio = await async_client.categorize_audio.create(
            api_key="apiKey",
        )
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMillionways) -> None:
        categorize_audio = await async_client.categorize_audio.create(
            api_key="apiKey",
            file=b"raw file contents",
        )
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMillionways) -> None:
        response = await async_client.categorize_audio.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        categorize_audio = await response.parse()
        assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMillionways) -> None:
        async with async_client.categorize_audio.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            categorize_audio = await response.parse()
            assert_matches_type(CategorizeAudioCreateResponse, categorize_audio, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_for_user(self, async_client: AsyncMillionways) -> None:
        categorize_audio = await async_client.categorize_audio.create_for_user(
            user_id="userId",
            api_key="apiKey",
        )
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_for_user_with_all_params(self, async_client: AsyncMillionways) -> None:
        categorize_audio = await async_client.categorize_audio.create_for_user(
            user_id="userId",
            api_key="apiKey",
            file=b"raw file contents",
        )
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_for_user(self, async_client: AsyncMillionways) -> None:
        response = await async_client.categorize_audio.with_raw_response.create_for_user(
            user_id="userId",
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        categorize_audio = await response.parse()
        assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_for_user(self, async_client: AsyncMillionways) -> None:
        async with async_client.categorize_audio.with_streaming_response.create_for_user(
            user_id="userId",
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            categorize_audio = await response.parse()
            assert_matches_type(CategorizeAudioCreateForUserResponse, categorize_audio, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_for_user(self, async_client: AsyncMillionways) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.categorize_audio.with_raw_response.create_for_user(
                user_id="",
                api_key="apiKey",
            )
