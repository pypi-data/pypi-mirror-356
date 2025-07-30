# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from millionways import Millionways, AsyncMillionways
from tests.utils import assert_matches_type
from millionways.types import CreateUserCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCreateUser:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Millionways) -> None:
        create_user = client.create_user.create(
            api_key="apiKey",
        )
        assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Millionways) -> None:
        response = client.create_user.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        create_user = response.parse()
        assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Millionways) -> None:
        with client.create_user.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            create_user = response.parse()
            assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCreateUser:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncMillionways) -> None:
        create_user = await async_client.create_user.create(
            api_key="apiKey",
        )
        assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMillionways) -> None:
        response = await async_client.create_user.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        create_user = await response.parse()
        assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMillionways) -> None:
        async with async_client.create_user.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            create_user = await response.parse()
            assert_matches_type(CreateUserCreateResponse, create_user, path=["response"])

        assert cast(Any, response.is_closed) is True
