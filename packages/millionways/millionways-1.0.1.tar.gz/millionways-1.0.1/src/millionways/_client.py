# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    chat,
    get_call,
    get_user,
    summarize,
    chat_result,
    chat_stream,
    create_user,
    analyze_team,
    get_user_chats,
    categorize_text,
    sales_assistant,
    categorize_audio,
    get_user_analysis,
    mental_health_chatbot,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Millionways",
    "AsyncMillionways",
    "Client",
    "AsyncClient",
]


class Millionways(SyncAPIClient):
    get_call: get_call.GetCallResource
    get_user_analysis: get_user_analysis.GetUserAnalysisResource
    get_user_chats: get_user_chats.GetUserChatsResource
    create_user: create_user.CreateUserResource
    categorize_text: categorize_text.CategorizeTextResource
    analyze_team: analyze_team.AnalyzeTeamResource
    categorize_audio: categorize_audio.CategorizeAudioResource
    chat: chat.ChatResource
    chat_result: chat_result.ChatResultResource
    mental_health_chatbot: mental_health_chatbot.MentalHealthChatbotResource
    chat_stream: chat_stream.ChatStreamResource
    sales_assistant: sales_assistant.SalesAssistantResource
    summarize: summarize.SummarizeResource
    get_user: get_user.GetUserResource
    with_raw_response: MillionwaysWithRawResponse
    with_streaming_response: MillionwaysWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Millionways client instance.

        This automatically infers the `api_key` argument from the `MILLIONWAYS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("MILLIONWAYS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("MILLIONWAYS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.millionways.org"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.get_call = get_call.GetCallResource(self)
        self.get_user_analysis = get_user_analysis.GetUserAnalysisResource(self)
        self.get_user_chats = get_user_chats.GetUserChatsResource(self)
        self.create_user = create_user.CreateUserResource(self)
        self.categorize_text = categorize_text.CategorizeTextResource(self)
        self.analyze_team = analyze_team.AnalyzeTeamResource(self)
        self.categorize_audio = categorize_audio.CategorizeAudioResource(self)
        self.chat = chat.ChatResource(self)
        self.chat_result = chat_result.ChatResultResource(self)
        self.mental_health_chatbot = mental_health_chatbot.MentalHealthChatbotResource(self)
        self.chat_stream = chat_stream.ChatStreamResource(self)
        self.sales_assistant = sales_assistant.SalesAssistantResource(self)
        self.summarize = summarize.SummarizeResource(self)
        self.get_user = get_user.GetUserResource(self)
        self.with_raw_response = MillionwaysWithRawResponse(self)
        self.with_streaming_response = MillionwaysWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncMillionways(AsyncAPIClient):
    get_call: get_call.AsyncGetCallResource
    get_user_analysis: get_user_analysis.AsyncGetUserAnalysisResource
    get_user_chats: get_user_chats.AsyncGetUserChatsResource
    create_user: create_user.AsyncCreateUserResource
    categorize_text: categorize_text.AsyncCategorizeTextResource
    analyze_team: analyze_team.AsyncAnalyzeTeamResource
    categorize_audio: categorize_audio.AsyncCategorizeAudioResource
    chat: chat.AsyncChatResource
    chat_result: chat_result.AsyncChatResultResource
    mental_health_chatbot: mental_health_chatbot.AsyncMentalHealthChatbotResource
    chat_stream: chat_stream.AsyncChatStreamResource
    sales_assistant: sales_assistant.AsyncSalesAssistantResource
    summarize: summarize.AsyncSummarizeResource
    get_user: get_user.AsyncGetUserResource
    with_raw_response: AsyncMillionwaysWithRawResponse
    with_streaming_response: AsyncMillionwaysWithStreamedResponse

    # client options
    api_key: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncMillionways client instance.

        This automatically infers the `api_key` argument from the `MILLIONWAYS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("MILLIONWAYS_API_KEY")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("MILLIONWAYS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.millionways.org"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.get_call = get_call.AsyncGetCallResource(self)
        self.get_user_analysis = get_user_analysis.AsyncGetUserAnalysisResource(self)
        self.get_user_chats = get_user_chats.AsyncGetUserChatsResource(self)
        self.create_user = create_user.AsyncCreateUserResource(self)
        self.categorize_text = categorize_text.AsyncCategorizeTextResource(self)
        self.analyze_team = analyze_team.AsyncAnalyzeTeamResource(self)
        self.categorize_audio = categorize_audio.AsyncCategorizeAudioResource(self)
        self.chat = chat.AsyncChatResource(self)
        self.chat_result = chat_result.AsyncChatResultResource(self)
        self.mental_health_chatbot = mental_health_chatbot.AsyncMentalHealthChatbotResource(self)
        self.chat_stream = chat_stream.AsyncChatStreamResource(self)
        self.sales_assistant = sales_assistant.AsyncSalesAssistantResource(self)
        self.summarize = summarize.AsyncSummarizeResource(self)
        self.get_user = get_user.AsyncGetUserResource(self)
        self.with_raw_response = AsyncMillionwaysWithRawResponse(self)
        self.with_streaming_response = AsyncMillionwaysWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected the api_key to be set. Or for the `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class MillionwaysWithRawResponse:
    def __init__(self, client: Millionways) -> None:
        self.get_call = get_call.GetCallResourceWithRawResponse(client.get_call)
        self.get_user_analysis = get_user_analysis.GetUserAnalysisResourceWithRawResponse(client.get_user_analysis)
        self.get_user_chats = get_user_chats.GetUserChatsResourceWithRawResponse(client.get_user_chats)
        self.create_user = create_user.CreateUserResourceWithRawResponse(client.create_user)
        self.categorize_text = categorize_text.CategorizeTextResourceWithRawResponse(client.categorize_text)
        self.analyze_team = analyze_team.AnalyzeTeamResourceWithRawResponse(client.analyze_team)
        self.categorize_audio = categorize_audio.CategorizeAudioResourceWithRawResponse(client.categorize_audio)
        self.chat = chat.ChatResourceWithRawResponse(client.chat)
        self.chat_result = chat_result.ChatResultResourceWithRawResponse(client.chat_result)
        self.mental_health_chatbot = mental_health_chatbot.MentalHealthChatbotResourceWithRawResponse(
            client.mental_health_chatbot
        )
        self.chat_stream = chat_stream.ChatStreamResourceWithRawResponse(client.chat_stream)
        self.sales_assistant = sales_assistant.SalesAssistantResourceWithRawResponse(client.sales_assistant)
        self.summarize = summarize.SummarizeResourceWithRawResponse(client.summarize)
        self.get_user = get_user.GetUserResourceWithRawResponse(client.get_user)


class AsyncMillionwaysWithRawResponse:
    def __init__(self, client: AsyncMillionways) -> None:
        self.get_call = get_call.AsyncGetCallResourceWithRawResponse(client.get_call)
        self.get_user_analysis = get_user_analysis.AsyncGetUserAnalysisResourceWithRawResponse(client.get_user_analysis)
        self.get_user_chats = get_user_chats.AsyncGetUserChatsResourceWithRawResponse(client.get_user_chats)
        self.create_user = create_user.AsyncCreateUserResourceWithRawResponse(client.create_user)
        self.categorize_text = categorize_text.AsyncCategorizeTextResourceWithRawResponse(client.categorize_text)
        self.analyze_team = analyze_team.AsyncAnalyzeTeamResourceWithRawResponse(client.analyze_team)
        self.categorize_audio = categorize_audio.AsyncCategorizeAudioResourceWithRawResponse(client.categorize_audio)
        self.chat = chat.AsyncChatResourceWithRawResponse(client.chat)
        self.chat_result = chat_result.AsyncChatResultResourceWithRawResponse(client.chat_result)
        self.mental_health_chatbot = mental_health_chatbot.AsyncMentalHealthChatbotResourceWithRawResponse(
            client.mental_health_chatbot
        )
        self.chat_stream = chat_stream.AsyncChatStreamResourceWithRawResponse(client.chat_stream)
        self.sales_assistant = sales_assistant.AsyncSalesAssistantResourceWithRawResponse(client.sales_assistant)
        self.summarize = summarize.AsyncSummarizeResourceWithRawResponse(client.summarize)
        self.get_user = get_user.AsyncGetUserResourceWithRawResponse(client.get_user)


class MillionwaysWithStreamedResponse:
    def __init__(self, client: Millionways) -> None:
        self.get_call = get_call.GetCallResourceWithStreamingResponse(client.get_call)
        self.get_user_analysis = get_user_analysis.GetUserAnalysisResourceWithStreamingResponse(
            client.get_user_analysis
        )
        self.get_user_chats = get_user_chats.GetUserChatsResourceWithStreamingResponse(client.get_user_chats)
        self.create_user = create_user.CreateUserResourceWithStreamingResponse(client.create_user)
        self.categorize_text = categorize_text.CategorizeTextResourceWithStreamingResponse(client.categorize_text)
        self.analyze_team = analyze_team.AnalyzeTeamResourceWithStreamingResponse(client.analyze_team)
        self.categorize_audio = categorize_audio.CategorizeAudioResourceWithStreamingResponse(client.categorize_audio)
        self.chat = chat.ChatResourceWithStreamingResponse(client.chat)
        self.chat_result = chat_result.ChatResultResourceWithStreamingResponse(client.chat_result)
        self.mental_health_chatbot = mental_health_chatbot.MentalHealthChatbotResourceWithStreamingResponse(
            client.mental_health_chatbot
        )
        self.chat_stream = chat_stream.ChatStreamResourceWithStreamingResponse(client.chat_stream)
        self.sales_assistant = sales_assistant.SalesAssistantResourceWithStreamingResponse(client.sales_assistant)
        self.summarize = summarize.SummarizeResourceWithStreamingResponse(client.summarize)
        self.get_user = get_user.GetUserResourceWithStreamingResponse(client.get_user)


class AsyncMillionwaysWithStreamedResponse:
    def __init__(self, client: AsyncMillionways) -> None:
        self.get_call = get_call.AsyncGetCallResourceWithStreamingResponse(client.get_call)
        self.get_user_analysis = get_user_analysis.AsyncGetUserAnalysisResourceWithStreamingResponse(
            client.get_user_analysis
        )
        self.get_user_chats = get_user_chats.AsyncGetUserChatsResourceWithStreamingResponse(client.get_user_chats)
        self.create_user = create_user.AsyncCreateUserResourceWithStreamingResponse(client.create_user)
        self.categorize_text = categorize_text.AsyncCategorizeTextResourceWithStreamingResponse(client.categorize_text)
        self.analyze_team = analyze_team.AsyncAnalyzeTeamResourceWithStreamingResponse(client.analyze_team)
        self.categorize_audio = categorize_audio.AsyncCategorizeAudioResourceWithStreamingResponse(
            client.categorize_audio
        )
        self.chat = chat.AsyncChatResourceWithStreamingResponse(client.chat)
        self.chat_result = chat_result.AsyncChatResultResourceWithStreamingResponse(client.chat_result)
        self.mental_health_chatbot = mental_health_chatbot.AsyncMentalHealthChatbotResourceWithStreamingResponse(
            client.mental_health_chatbot
        )
        self.chat_stream = chat_stream.AsyncChatStreamResourceWithStreamingResponse(client.chat_stream)
        self.sales_assistant = sales_assistant.AsyncSalesAssistantResourceWithStreamingResponse(client.sales_assistant)
        self.summarize = summarize.AsyncSummarizeResourceWithStreamingResponse(client.summarize)
        self.get_user = get_user.AsyncGetUserResourceWithStreamingResponse(client.get_user)


Client = Millionways

AsyncClient = AsyncMillionways
