# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chat_result_generate_params
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
from ..types.chat_result_generate_response import ChatResultGenerateResponse

__all__ = ["ChatResultResource", "AsyncChatResultResource"]


class ChatResultResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ChatResultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return ChatResultResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: chat_result_generate_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: chat_result_generate_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatResultGenerateResponse:
        """
        Generate emotionally intelligent chatbot response based on user input with given
        Result

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
            "/chat-result",
            body=maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                chat_result_generate_params.ChatResultGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, chat_result_generate_params.ChatResultGenerateParams),
            ),
            cast_to=ChatResultGenerateResponse,
        )


class AsyncChatResultResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncChatResultResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: chat_result_generate_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: chat_result_generate_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatResultGenerateResponse:
        """
        Generate emotionally intelligent chatbot response based on user input with given
        Result

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
            "/chat-result",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                chat_result_generate_params.ChatResultGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, chat_result_generate_params.ChatResultGenerateParams
                ),
            ),
            cast_to=ChatResultGenerateResponse,
        )


class ChatResultResourceWithRawResponse:
    def __init__(self, chat_result: ChatResultResource) -> None:
        self._chat_result = chat_result

        self.generate = to_raw_response_wrapper(
            chat_result.generate,
        )


class AsyncChatResultResourceWithRawResponse:
    def __init__(self, chat_result: AsyncChatResultResource) -> None:
        self._chat_result = chat_result

        self.generate = async_to_raw_response_wrapper(
            chat_result.generate,
        )


class ChatResultResourceWithStreamingResponse:
    def __init__(self, chat_result: ChatResultResource) -> None:
        self._chat_result = chat_result

        self.generate = to_streamed_response_wrapper(
            chat_result.generate,
        )


class AsyncChatResultResourceWithStreamingResponse:
    def __init__(self, chat_result: AsyncChatResultResource) -> None:
        self._chat_result = chat_result

        self.generate = async_to_streamed_response_wrapper(
            chat_result.generate,
        )
