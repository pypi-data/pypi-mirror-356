# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import analyze_team_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.analyze_team_create_response import AnalyzeTeamCreateResponse

__all__ = ["AnalyzeTeamResource", "AsyncAnalyzeTeamResource"]


class AnalyzeTeamResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnalyzeTeamResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AnalyzeTeamResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyzeTeamResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AnalyzeTeamResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        text: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeTeamCreateResponse:
        """
        Generate millionways emotionally-intelligent AI Team Classification based on
        Text Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/analyze-team",
            body=maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                analyze_team_create_params.AnalyzeTeamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, analyze_team_create_params.AnalyzeTeamCreateParams),
            ),
            cast_to=AnalyzeTeamCreateResponse,
        )


class AsyncAnalyzeTeamResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnalyzeTeamResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAnalyzeTeamResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyzeTeamResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncAnalyzeTeamResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        text: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeTeamCreateResponse:
        """
        Generate millionways emotionally-intelligent AI Team Classification based on
        Text Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/analyze-team",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                analyze_team_create_params.AnalyzeTeamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, analyze_team_create_params.AnalyzeTeamCreateParams
                ),
            ),
            cast_to=AnalyzeTeamCreateResponse,
        )


class AnalyzeTeamResourceWithRawResponse:
    def __init__(self, analyze_team: AnalyzeTeamResource) -> None:
        self._analyze_team = analyze_team

        self.create = to_raw_response_wrapper(
            analyze_team.create,
        )


class AsyncAnalyzeTeamResourceWithRawResponse:
    def __init__(self, analyze_team: AsyncAnalyzeTeamResource) -> None:
        self._analyze_team = analyze_team

        self.create = async_to_raw_response_wrapper(
            analyze_team.create,
        )


class AnalyzeTeamResourceWithStreamingResponse:
    def __init__(self, analyze_team: AnalyzeTeamResource) -> None:
        self._analyze_team = analyze_team

        self.create = to_streamed_response_wrapper(
            analyze_team.create,
        )


class AsyncAnalyzeTeamResourceWithStreamingResponse:
    def __init__(self, analyze_team: AsyncAnalyzeTeamResource) -> None:
        self._analyze_team = analyze_team

        self.create = async_to_streamed_response_wrapper(
            analyze_team.create,
        )
