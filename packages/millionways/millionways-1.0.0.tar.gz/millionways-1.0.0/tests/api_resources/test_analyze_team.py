# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from millionways import Millionways, AsyncMillionways
from tests.utils import assert_matches_type
from millionways.types import AnalyzeTeamCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnalyzeTeam:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Millionways) -> None:
        analyze_team = client.analyze_team.create(
            api_key="apiKey",
        )
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Millionways) -> None:
        analyze_team = client.analyze_team.create(
            api_key="apiKey",
            language="en",
            text="I am feeling good today and I want to go outside and meet some people.",
        )
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Millionways) -> None:
        response = client.analyze_team.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze_team = response.parse()
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Millionways) -> None:
        with client.analyze_team.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze_team = response.parse()
            assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAnalyzeTeam:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncMillionways) -> None:
        analyze_team = await async_client.analyze_team.create(
            api_key="apiKey",
        )
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncMillionways) -> None:
        analyze_team = await async_client.analyze_team.create(
            api_key="apiKey",
            language="en",
            text="I am feeling good today and I want to go outside and meet some people.",
        )
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncMillionways) -> None:
        response = await async_client.analyze_team.with_raw_response.create(
            api_key="apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze_team = await response.parse()
        assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncMillionways) -> None:
        async with async_client.analyze_team.with_streaming_response.create(
            api_key="apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze_team = await response.parse()
            assert_matches_type(AnalyzeTeamCreateResponse, analyze_team, path=["response"])

        assert cast(Any, response.is_closed) is True
