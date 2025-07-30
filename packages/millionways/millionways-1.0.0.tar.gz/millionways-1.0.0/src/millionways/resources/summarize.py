# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import summarize_create_params
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
from ..types.summarize_create_response import SummarizeCreateResponse

__all__ = ["SummarizeResource", "AsyncSummarizeResource"]


class SummarizeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SummarizeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SummarizeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SummarizeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return SummarizeResourceWithStreamingResponse(self)

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
    ) -> SummarizeCreateResponse:
        """
        Generate millionways emotionally-intelligent AI summary based on Text Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/summarize",
            body=maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                summarize_create_params.SummarizeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, summarize_create_params.SummarizeCreateParams),
            ),
            cast_to=SummarizeCreateResponse,
        )


class AsyncSummarizeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSummarizeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSummarizeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSummarizeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncSummarizeResourceWithStreamingResponse(self)

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
    ) -> SummarizeCreateResponse:
        """
        Generate millionways emotionally-intelligent AI summary based on Text Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/summarize",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                summarize_create_params.SummarizeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"api_key": api_key}, summarize_create_params.SummarizeCreateParams),
            ),
            cast_to=SummarizeCreateResponse,
        )


class SummarizeResourceWithRawResponse:
    def __init__(self, summarize: SummarizeResource) -> None:
        self._summarize = summarize

        self.create = to_raw_response_wrapper(
            summarize.create,
        )


class AsyncSummarizeResourceWithRawResponse:
    def __init__(self, summarize: AsyncSummarizeResource) -> None:
        self._summarize = summarize

        self.create = async_to_raw_response_wrapper(
            summarize.create,
        )


class SummarizeResourceWithStreamingResponse:
    def __init__(self, summarize: SummarizeResource) -> None:
        self._summarize = summarize

        self.create = to_streamed_response_wrapper(
            summarize.create,
        )


class AsyncSummarizeResourceWithStreamingResponse:
    def __init__(self, summarize: AsyncSummarizeResource) -> None:
        self._summarize = summarize

        self.create = async_to_streamed_response_wrapper(
            summarize.create,
        )
