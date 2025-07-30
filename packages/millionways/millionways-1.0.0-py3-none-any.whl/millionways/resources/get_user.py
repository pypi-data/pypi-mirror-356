# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import get_user_list_params, get_user_retrieve_params
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
from ..types.get_user_list_response import GetUserListResponse
from ..types.get_user_retrieve_response import GetUserRetrieveResponse

__all__ = ["GetUserResource", "AsyncGetUserResource"]


class GetUserResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GetUserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return GetUserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GetUserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return GetUserResourceWithStreamingResponse(self)

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
    ) -> GetUserRetrieveResponse:
        """
        Get user by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            f"/get-user/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, get_user_retrieve_params.GetUserRetrieveParams),
            ),
            cast_to=GetUserRetrieveResponse,
        )

    def list(
        self,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetUserListResponse:
        """
        Get all users

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/get-users",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, get_user_list_params.GetUserListParams),
            ),
            cast_to=GetUserListResponse,
        )


class AsyncGetUserResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGetUserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncGetUserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGetUserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncGetUserResourceWithStreamingResponse(self)

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
    ) -> GetUserRetrieveResponse:
        """
        Get user by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            f"/get-user/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"api_key": api_key}, get_user_retrieve_params.GetUserRetrieveParams),
            ),
            cast_to=GetUserRetrieveResponse,
        )

    async def list(
        self,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GetUserListResponse:
        """
        Get all users

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/get-users",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"api_key": api_key}, get_user_list_params.GetUserListParams),
            ),
            cast_to=GetUserListResponse,
        )


class GetUserResourceWithRawResponse:
    def __init__(self, get_user: GetUserResource) -> None:
        self._get_user = get_user

        self.retrieve = to_raw_response_wrapper(
            get_user.retrieve,
        )
        self.list = to_raw_response_wrapper(
            get_user.list,
        )


class AsyncGetUserResourceWithRawResponse:
    def __init__(self, get_user: AsyncGetUserResource) -> None:
        self._get_user = get_user

        self.retrieve = async_to_raw_response_wrapper(
            get_user.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            get_user.list,
        )


class GetUserResourceWithStreamingResponse:
    def __init__(self, get_user: GetUserResource) -> None:
        self._get_user = get_user

        self.retrieve = to_streamed_response_wrapper(
            get_user.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            get_user.list,
        )


class AsyncGetUserResourceWithStreamingResponse:
    def __init__(self, get_user: AsyncGetUserResource) -> None:
        self._get_user = get_user

        self.retrieve = async_to_streamed_response_wrapper(
            get_user.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            get_user.list,
        )
