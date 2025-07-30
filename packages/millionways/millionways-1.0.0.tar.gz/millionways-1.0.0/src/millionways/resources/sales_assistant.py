# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import sales_assistant_generate_insights_params
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
from ..types.sales_assistant_generate_insights_response import SalesAssistantGenerateInsightsResponse

__all__ = ["SalesAssistantResource", "AsyncSalesAssistantResource"]


class SalesAssistantResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SalesAssistantResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SalesAssistantResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SalesAssistantResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return SalesAssistantResourceWithStreamingResponse(self)

    def generate_insights(
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
    ) -> SalesAssistantGenerateInsightsResponse:
        """
        Generate millionways emotionally-intelligent AI sales insights based on Text
        Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/sales-assistant",
            body=maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                sales_assistant_generate_insights_params.SalesAssistantGenerateInsightsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, sales_assistant_generate_insights_params.SalesAssistantGenerateInsightsParams
                ),
            ),
            cast_to=SalesAssistantGenerateInsightsResponse,
        )


class AsyncSalesAssistantResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSalesAssistantResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSalesAssistantResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSalesAssistantResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncSalesAssistantResourceWithStreamingResponse(self)

    async def generate_insights(
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
    ) -> SalesAssistantGenerateInsightsResponse:
        """
        Generate millionways emotionally-intelligent AI sales insights based on Text
        Input.

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/sales-assistant",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                sales_assistant_generate_insights_params.SalesAssistantGenerateInsightsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, sales_assistant_generate_insights_params.SalesAssistantGenerateInsightsParams
                ),
            ),
            cast_to=SalesAssistantGenerateInsightsResponse,
        )


class SalesAssistantResourceWithRawResponse:
    def __init__(self, sales_assistant: SalesAssistantResource) -> None:
        self._sales_assistant = sales_assistant

        self.generate_insights = to_raw_response_wrapper(
            sales_assistant.generate_insights,
        )


class AsyncSalesAssistantResourceWithRawResponse:
    def __init__(self, sales_assistant: AsyncSalesAssistantResource) -> None:
        self._sales_assistant = sales_assistant

        self.generate_insights = async_to_raw_response_wrapper(
            sales_assistant.generate_insights,
        )


class SalesAssistantResourceWithStreamingResponse:
    def __init__(self, sales_assistant: SalesAssistantResource) -> None:
        self._sales_assistant = sales_assistant

        self.generate_insights = to_streamed_response_wrapper(
            sales_assistant.generate_insights,
        )


class AsyncSalesAssistantResourceWithStreamingResponse:
    def __init__(self, sales_assistant: AsyncSalesAssistantResource) -> None:
        self._sales_assistant = sales_assistant

        self.generate_insights = async_to_streamed_response_wrapper(
            sales_assistant.generate_insights,
        )
