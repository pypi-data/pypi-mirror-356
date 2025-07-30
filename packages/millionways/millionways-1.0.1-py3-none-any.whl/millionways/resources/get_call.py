# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import get_call_retrieve_params
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
from ..types.get_call_retrieve_response import GetCallRetrieveResponse

__all__ = ["GetCallResource", "AsyncGetCallResource"]


class GetCallResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GetCallResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return GetCallResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GetCallResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return GetCallResourceWithStreamingResponse(self)

    def retrieve(
        self,
        call_id: str,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetCallRetrieveResponse:
        """
        Get call by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return self._get(
            f"/get-call/{call_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, get_call_retrieve_params.GetCallRetrieveParams),
            ),
            cast_to=GetCallRetrieveResponse,
        )


class AsyncGetCallResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGetCallResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncGetCallResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGetCallResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncGetCallResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        call_id: str,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetCallRetrieveResponse:
        """
        Get call by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return await self._get(
            f"/get-call/{call_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"api_key": api_key}, get_call_retrieve_params.GetCallRetrieveParams),
            ),
            cast_to=GetCallRetrieveResponse,
        )


class GetCallResourceWithRawResponse:
    def __init__(self, get_call: GetCallResource) -> None:
        self._get_call = get_call

        self.retrieve = to_raw_response_wrapper(
            get_call.retrieve,
        )


class AsyncGetCallResourceWithRawResponse:
    def __init__(self, get_call: AsyncGetCallResource) -> None:
        self._get_call = get_call

        self.retrieve = async_to_raw_response_wrapper(
            get_call.retrieve,
        )


class GetCallResourceWithStreamingResponse:
    def __init__(self, get_call: GetCallResource) -> None:
        self._get_call = get_call

        self.retrieve = to_streamed_response_wrapper(
            get_call.retrieve,
        )


class AsyncGetCallResourceWithStreamingResponse:
    def __init__(self, get_call: AsyncGetCallResource) -> None:
        self._get_call = get_call

        self.retrieve = async_to_streamed_response_wrapper(
            get_call.retrieve,
        )
