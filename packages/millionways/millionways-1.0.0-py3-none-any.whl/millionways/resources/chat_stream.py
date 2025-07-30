# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chat_stream_generate_response_params
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
from ..types.chat_stream_generate_response_response import ChatStreamGenerateResponseResponse

__all__ = ["ChatStreamResource", "AsyncChatStreamResource"]


class ChatStreamResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatStreamResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ChatStreamResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatStreamResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return ChatStreamResourceWithStreamingResponse(self)

    def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: chat_stream_generate_response_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: chat_stream_generate_response_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatStreamGenerateResponseResponse:
        """
        Generate emotionally intelligent chatbot streamed response based on user input
        with given Result

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
            "/chat-stream",
            body=maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                chat_stream_generate_response_params.ChatStreamGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, chat_stream_generate_response_params.ChatStreamGenerateResponseParams
                ),
            ),
            cast_to=ChatStreamGenerateResponseResponse,
        )


class AsyncChatStreamResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatStreamResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncChatStreamResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatStreamResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncChatStreamResourceWithStreamingResponse(self)

    async def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: chat_stream_generate_response_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: chat_stream_generate_response_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatStreamGenerateResponseResponse:
        """
        Generate emotionally intelligent chatbot streamed response based on user input
        with given Result

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
            "/chat-stream",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                chat_stream_generate_response_params.ChatStreamGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, chat_stream_generate_response_params.ChatStreamGenerateResponseParams
                ),
            ),
            cast_to=ChatStreamGenerateResponseResponse,
        )


class ChatStreamResourceWithRawResponse:
    def __init__(self, chat_stream: ChatStreamResource) -> None:
        self._chat_stream = chat_stream

        self.generate_response = to_raw_response_wrapper(
            chat_stream.generate_response,
        )


class AsyncChatStreamResourceWithRawResponse:
    def __init__(self, chat_stream: AsyncChatStreamResource) -> None:
        self._chat_stream = chat_stream

        self.generate_response = async_to_raw_response_wrapper(
            chat_stream.generate_response,
        )


class ChatStreamResourceWithStreamingResponse:
    def __init__(self, chat_stream: ChatStreamResource) -> None:
        self._chat_stream = chat_stream

        self.generate_response = to_streamed_response_wrapper(
            chat_stream.generate_response,
        )


class AsyncChatStreamResourceWithStreamingResponse:
    def __init__(self, chat_stream: AsyncChatStreamResource) -> None:
        self._chat_stream = chat_stream

        self.generate_response = async_to_streamed_response_wrapper(
            chat_stream.generate_response,
        )
