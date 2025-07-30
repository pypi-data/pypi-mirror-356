# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import get_user_analysis_retrieve_params
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
from ..types.get_user_analysis_retrieve_response import GetUserAnalysisRetrieveResponse

__all__ = ["GetUserAnalysisResource", "AsyncGetUserAnalysisResource"]


class GetUserAnalysisResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GetUserAnalysisResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return GetUserAnalysisResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GetUserAnalysisResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return GetUserAnalysisResourceWithStreamingResponse(self)

    def retrieve(
        self,
        user_id: str,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetUserAnalysisRetrieveResponse:
        """
        Get user analysis by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            f"/get-user-analysis/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, get_user_analysis_retrieve_params.GetUserAnalysisRetrieveParams
                ),
            ),
            cast_to=GetUserAnalysisRetrieveResponse,
        )


class AsyncGetUserAnalysisResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGetUserAnalysisResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncGetUserAnalysisResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGetUserAnalysisResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncGetUserAnalysisResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        user_id: str,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetUserAnalysisRetrieveResponse:
        """
        Get user analysis by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            f"/get-user-analysis/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, get_user_analysis_retrieve_params.GetUserAnalysisRetrieveParams
                ),
            ),
            cast_to=GetUserAnalysisRetrieveResponse,
        )


class GetUserAnalysisResourceWithRawResponse:
    def __init__(self, get_user_analysis: GetUserAnalysisResource) -> None:
        self._get_user_analysis = get_user_analysis

        self.retrieve = to_raw_response_wrapper(
            get_user_analysis.retrieve,
        )


class AsyncGetUserAnalysisResourceWithRawResponse:
    def __init__(self, get_user_analysis: AsyncGetUserAnalysisResource) -> None:
        self._get_user_analysis = get_user_analysis

        self.retrieve = async_to_raw_response_wrapper(
            get_user_analysis.retrieve,
        )


class GetUserAnalysisResourceWithStreamingResponse:
    def __init__(self, get_user_analysis: GetUserAnalysisResource) -> None:
        self._get_user_analysis = get_user_analysis

        self.retrieve = to_streamed_response_wrapper(
            get_user_analysis.retrieve,
        )


class AsyncGetUserAnalysisResourceWithStreamingResponse:
    def __init__(self, get_user_analysis: AsyncGetUserAnalysisResource) -> None:
        self._get_user_analysis = get_user_analysis

        self.retrieve = async_to_streamed_response_wrapper(
            get_user_analysis.retrieve,
        )
