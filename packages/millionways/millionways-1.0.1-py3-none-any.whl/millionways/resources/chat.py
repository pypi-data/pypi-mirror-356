# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chat_generate_response_params, chat_generate_response_for_user_params
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
from ..types.chat_generate_response_response import ChatGenerateResponseResponse
from ..types.chat_generate_response_for_user_response import ChatGenerateResponseForUserResponse

__all__ = ["ChatResource", "AsyncChatResource"]


class ChatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return ChatResourceWithStreamingResponse(self)

    def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatGenerateResponseResponse:
        """
        Generate emotionally intelligent chatbot response based on user input

        Args:
          language: language parameter, defaults to en

          messages: history of messages between user with the role 'user' and chatbot with the role
              'assistant'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/chat",
            body=maybe_transform(
                {
                    "language": language,
                    "messages": messages,
                },
                chat_generate_response_params.ChatGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, chat_generate_response_params.ChatGenerateResponseParams),
            ),
            cast_to=ChatGenerateResponseResponse,
        )

    def generate_response_for_user(
        self,
        user_id: str,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatGenerateResponseForUserResponse:
        """
        Generate emotionally intelligent chatbot response based on user input

        Args:
          language: language parameter, defaults to en

          messages: history of messages between user with the role 'user' and chatbot with the role
              'assistant'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            f"/chat/{user_id}",
            body=maybe_transform(
                {
                    "language": language,
                    "messages": messages,
                },
                chat_generate_response_for_user_params.ChatGenerateResponseForUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, chat_generate_response_for_user_params.ChatGenerateResponseForUserParams
                ),
            ),
            cast_to=ChatGenerateResponseForUserResponse,
        )


class AsyncChatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncChatResourceWithStreamingResponse(self)

    async def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatGenerateResponseResponse:
        """
        Generate emotionally intelligent chatbot response based on user input

        Args:
          language: language parameter, defaults to en

          messages: history of messages between user with the role 'user' and chatbot with the role
              'assistant'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/chat",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "messages": messages,
                },
                chat_generate_response_params.ChatGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, chat_generate_response_params.ChatGenerateResponseParams
                ),
            ),
            cast_to=ChatGenerateResponseResponse,
        )

    async def generate_response_for_user(
        self,
        user_id: str,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatGenerateResponseForUserResponse:
        """
        Generate emotionally intelligent chatbot response based on user input

        Args:
          language: language parameter, defaults to en

          messages: history of messages between user with the role 'user' and chatbot with the role
              'assistant'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._post(
            f"/chat/{user_id}",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "messages": messages,
                },
                chat_generate_response_for_user_params.ChatGenerateResponseForUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, chat_generate_response_for_user_params.ChatGenerateResponseForUserParams
                ),
            ),
            cast_to=ChatGenerateResponseForUserResponse,
        )


class ChatResourceWithRawResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.generate_response = to_raw_response_wrapper(
            chat.generate_response,
        )
        self.generate_response_for_user = to_raw_response_wrapper(
            chat.generate_response_for_user,
        )


class AsyncChatResourceWithRawResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.generate_response = async_to_raw_response_wrapper(
            chat.generate_response,
        )
        self.generate_response_for_user = async_to_raw_response_wrapper(
            chat.generate_response_for_user,
        )


class ChatResourceWithStreamingResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.generate_response = to_streamed_response_wrapper(
            chat.generate_response,
        )
        self.generate_response_for_user = to_streamed_response_wrapper(
            chat.generate_response_for_user,
        )


class AsyncChatResourceWithStreamingResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.generate_response = async_to_streamed_response_wrapper(
            chat.generate_response,
        )
        self.generate_response_for_user = async_to_streamed_response_wrapper(
            chat.generate_response_for_user,
        )
