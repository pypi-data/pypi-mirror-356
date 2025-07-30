# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import mental_health_chatbot_generate_response_params
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
from ..types.mental_health_chatbot_generate_response_response import MentalHealthChatbotGenerateResponseResponse

__all__ = ["MentalHealthChatbotResource", "AsyncMentalHealthChatbotResource"]


class MentalHealthChatbotResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MentalHealthChatbotResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return MentalHealthChatbotResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MentalHealthChatbotResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return MentalHealthChatbotResourceWithStreamingResponse(self)

    def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: mental_health_chatbot_generate_response_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: mental_health_chatbot_generate_response_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MentalHealthChatbotGenerateResponseResponse:
        """
        Generate emotionally intelligent mental health support chatbot response based on
        user input with given Result

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
            "/mental-health-chatbot",
            body=maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                mental_health_chatbot_generate_response_params.MentalHealthChatbotGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key},
                    mental_health_chatbot_generate_response_params.MentalHealthChatbotGenerateResponseParams,
                ),
            ),
            cast_to=MentalHealthChatbotGenerateResponseResponse,
        )


class AsyncMentalHealthChatbotResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMentalHealthChatbotResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncMentalHealthChatbotResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMentalHealthChatbotResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncMentalHealthChatbotResourceWithStreamingResponse(self)

    async def generate_response(
        self,
        *,
        api_key: str,
        language: str | NotGiven = NOT_GIVEN,
        levels: mental_health_chatbot_generate_response_params.Levels | NotGiven = NOT_GIVEN,
        messages: Iterable[object] | NotGiven = NOT_GIVEN,
        result: mental_health_chatbot_generate_response_params.Result | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MentalHealthChatbotGenerateResponseResponse:
        """
        Generate emotionally intelligent mental health support chatbot response based on
        user input with given Result

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
            "/mental-health-chatbot",
            body=await async_maybe_transform(
                {
                    "language": language,
                    "levels": levels,
                    "messages": messages,
                    "result": result,
                },
                mental_health_chatbot_generate_response_params.MentalHealthChatbotGenerateResponseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key},
                    mental_health_chatbot_generate_response_params.MentalHealthChatbotGenerateResponseParams,
                ),
            ),
            cast_to=MentalHealthChatbotGenerateResponseResponse,
        )


class MentalHealthChatbotResourceWithRawResponse:
    def __init__(self, mental_health_chatbot: MentalHealthChatbotResource) -> None:
        self._mental_health_chatbot = mental_health_chatbot

        self.generate_response = to_raw_response_wrapper(
            mental_health_chatbot.generate_response,
        )


class AsyncMentalHealthChatbotResourceWithRawResponse:
    def __init__(self, mental_health_chatbot: AsyncMentalHealthChatbotResource) -> None:
        self._mental_health_chatbot = mental_health_chatbot

        self.generate_response = async_to_raw_response_wrapper(
            mental_health_chatbot.generate_response,
        )


class MentalHealthChatbotResourceWithStreamingResponse:
    def __init__(self, mental_health_chatbot: MentalHealthChatbotResource) -> None:
        self._mental_health_chatbot = mental_health_chatbot

        self.generate_response = to_streamed_response_wrapper(
            mental_health_chatbot.generate_response,
        )


class AsyncMentalHealthChatbotResourceWithStreamingResponse:
    def __init__(self, mental_health_chatbot: AsyncMentalHealthChatbotResource) -> None:
        self._mental_health_chatbot = mental_health_chatbot

        self.generate_response = async_to_streamed_response_wrapper(
            mental_health_chatbot.generate_response,
        )
