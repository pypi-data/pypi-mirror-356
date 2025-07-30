# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import create_user_create_params
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
from ..types.create_user_create_response import CreateUserCreateResponse

__all__ = ["CreateUserResource", "AsyncCreateUserResource"]


class CreateUserResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CreateUserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return CreateUserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreateUserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return CreateUserResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateUserCreateResponse:
        """
        Create a new user

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/create-user",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, create_user_create_params.CreateUserCreateParams),
            ),
            cast_to=CreateUserCreateResponse,
        )


class AsyncCreateUserResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCreateUserResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncCreateUserResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreateUserResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncCreateUserResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        api_key: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateUserCreateResponse:
        """
        Create a new user

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/create-user",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, create_user_create_params.CreateUserCreateParams
                ),
            ),
            cast_to=CreateUserCreateResponse,
        )


class CreateUserResourceWithRawResponse:
    def __init__(self, create_user: CreateUserResource) -> None:
        self._create_user = create_user

        self.create = to_raw_response_wrapper(
            create_user.create,
        )


class AsyncCreateUserResourceWithRawResponse:
    def __init__(self, create_user: AsyncCreateUserResource) -> None:
        self._create_user = create_user

        self.create = async_to_raw_response_wrapper(
            create_user.create,
        )


class CreateUserResourceWithStreamingResponse:
    def __init__(self, create_user: CreateUserResource) -> None:
        self._create_user = create_user

        self.create = to_streamed_response_wrapper(
            create_user.create,
        )


class AsyncCreateUserResourceWithStreamingResponse:
    def __init__(self, create_user: AsyncCreateUserResource) -> None:
        self._create_user = create_user

        self.create = async_to_streamed_response_wrapper(
            create_user.create,
        )
