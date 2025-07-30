# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import categorize_text_classify_params, categorize_text_classify_by_user_params
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
from ..types.categorize_text_classify_response import CategorizeTextClassifyResponse
from ..types.categorize_text_classify_by_user_response import CategorizeTextClassifyByUserResponse

__all__ = ["CategorizeTextResource", "AsyncCategorizeTextResource"]


class CategorizeTextResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CategorizeTextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return CategorizeTextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CategorizeTextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return CategorizeTextResourceWithStreamingResponse(self)

    def classify(
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
    ) -> CategorizeTextClassifyResponse:
        """
        Generate millionways emotionally-intelligent AI Classification based on Text
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
            "/categorize-text",
            body=maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                categorize_text_classify_params.CategorizeTextClassifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, categorize_text_classify_params.CategorizeTextClassifyParams
                ),
            ),
            cast_to=CategorizeTextClassifyResponse,
        )

    def classify_by_user(
        self,
        user_id: str,
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
    ) -> CategorizeTextClassifyByUserResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Text Input by
        User with userId

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            f"/categorize-text/{user_id}",
            body=maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                categorize_text_classify_by_user_params.CategorizeTextClassifyByUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, categorize_text_classify_by_user_params.CategorizeTextClassifyByUserParams
                ),
            ),
            cast_to=CategorizeTextClassifyByUserResponse,
        )


class AsyncCategorizeTextResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCategorizeTextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncCategorizeTextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCategorizeTextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncCategorizeTextResourceWithStreamingResponse(self)

    async def classify(
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
    ) -> CategorizeTextClassifyResponse:
        """
        Generate millionways emotionally-intelligent AI Classification based on Text
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
            "/categorize-text",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                categorize_text_classify_params.CategorizeTextClassifyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, categorize_text_classify_params.CategorizeTextClassifyParams
                ),
            ),
            cast_to=CategorizeTextClassifyResponse,
        )

    async def classify_by_user(
        self,
        user_id: str,
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
    ) -> CategorizeTextClassifyByUserResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Text Input by
        User with userId

        Args:
          language: language parameter, defaults to en

          text: text input to be classified

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._post(
            f"/categorize-text/{user_id}",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "text": text,
                },
                categorize_text_classify_by_user_params.CategorizeTextClassifyByUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, categorize_text_classify_by_user_params.CategorizeTextClassifyByUserParams
                ),
            ),
            cast_to=CategorizeTextClassifyByUserResponse,
        )


class CategorizeTextResourceWithRawResponse:
    def __init__(self, categorize_text: CategorizeTextResource) -> None:
        self._categorize_text = categorize_text

        self.classify = to_raw_response_wrapper(
            categorize_text.classify,
        )
        self.classify_by_user = to_raw_response_wrapper(
            categorize_text.classify_by_user,
        )


class AsyncCategorizeTextResourceWithRawResponse:
    def __init__(self, categorize_text: AsyncCategorizeTextResource) -> None:
        self._categorize_text = categorize_text

        self.classify = async_to_raw_response_wrapper(
            categorize_text.classify,
        )
        self.classify_by_user = async_to_raw_response_wrapper(
            categorize_text.classify_by_user,
        )


class CategorizeTextResourceWithStreamingResponse:
    def __init__(self, categorize_text: CategorizeTextResource) -> None:
        self._categorize_text = categorize_text

        self.classify = to_streamed_response_wrapper(
            categorize_text.classify,
        )
        self.classify_by_user = to_streamed_response_wrapper(
            categorize_text.classify_by_user,
        )


class AsyncCategorizeTextResourceWithStreamingResponse:
    def __init__(self, categorize_text: AsyncCategorizeTextResource) -> None:
        self._categorize_text = categorize_text

        self.classify = async_to_streamed_response_wrapper(
            categorize_text.classify,
        )
        self.classify_by_user = async_to_streamed_response_wrapper(
            categorize_text.classify_by_user,
        )
