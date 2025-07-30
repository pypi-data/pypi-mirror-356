# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from millionways import Millionways, AsyncMillionways
from tests.utils import assert_matches_type
from millionways.types import GetCallRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGetCall:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Millionways) -> None:
        get_call = client.get_call.retrieve(
            call_id="callId",
            api_key="apiKey",
        )
        assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Millionways) -> None:
        response = client.get_call.with_raw_response.retrieve(
            call_id="callId",
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        get_call = response.parse()
        assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Millionways) -> None:
        with client.get_call.with_streaming_response.retrieve(
            call_id="callId",
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            get_call = response.parse()
            assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Millionways) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.get_call.with_raw_response.retrieve(
                call_id="",
                api_key="apiKey",
            )


class TestAsyncGetCall:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMillionways) -> None:
        get_call = await async_client.get_call.retrieve(
            call_id="callId",
            api_key="apiKey",
        )
        assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMillionways) -> None:
        response = await async_client.get_call.with_raw_response.retrieve(
            call_id="callId",
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        get_call = await response.parse()
        assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMillionways) -> None:
        async with async_client.get_call.with_streaming_response.retrieve(
            call_id="callId",
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            get_call = await response.parse()
            assert_matches_type(GetCallRetrieveResponse, get_call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMillionways) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.get_call.with_raw_response.retrieve(
                call_id="",
                api_key="apiKey",
            )
