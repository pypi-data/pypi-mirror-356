# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast

import httpx

from ..types import categorize_audio_create_params, categorize_audio_create_for_user_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.categorize_audio_create_response import CategorizeAudioCreateResponse
from ..types.categorize_audio_create_for_user_response import CategorizeAudioCreateForUserResponse

__all__ = ["CategorizeAudioResource", "AsyncCategorizeAudioResource"]


class CategorizeAudioResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CategorizeAudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return CategorizeAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CategorizeAudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return CategorizeAudioResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        api_key: str,
        file: FileTypes | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CategorizeAudioCreateResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Audio Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/categorize-audio",
            body=maybe_transform(body, categorize_audio_create_params.CategorizeAudioCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"api_key": api_key}, categorize_audio_create_params.CategorizeAudioCreateParams),
            ),
            cast_to=CategorizeAudioCreateResponse,
        )

    def create_for_user(
        self,
        user_id: str,
        *,
        api_key: str,
        file: FileTypes | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CategorizeAudioCreateForUserResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Audio Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            f"/categorize-audio/{user_id}",
            body=maybe_transform(body, categorize_audio_create_for_user_params.CategorizeAudioCreateForUserParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"api_key": api_key}, categorize_audio_create_for_user_params.CategorizeAudioCreateForUserParams
                ),
            ),
            cast_to=CategorizeAudioCreateForUserResponse,
        )


class AsyncCategorizeAudioResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCategorizeAudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncCategorizeAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCategorizeAudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mwe1/millionways-python-sdk#with_streaming_response
        """
        return AsyncCategorizeAudioResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        api_key: str,
        file: FileTypes | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CategorizeAudioCreateResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Audio Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/categorize-audio",
            body=await async_maybe_transform(body, categorize_audio_create_params.CategorizeAudioCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, categorize_audio_create_params.CategorizeAudioCreateParams
                ),
            ),
            cast_to=CategorizeAudioCreateResponse,
        )

    async def create_for_user(
        self,
        user_id: str,
        *,
        api_key: str,
        file: FileTypes | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CategorizeAudioCreateForUserResponse:
        """
        Generate millionways emotionally-smart AI Classification based on Audio Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            f"/categorize-audio/{user_id}",
            body=await async_maybe_transform(
                body, categorize_audio_create_for_user_params.CategorizeAudioCreateForUserParams
            ),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"api_key": api_key}, categorize_audio_create_for_user_params.CategorizeAudioCreateForUserParams
                ),
            ),
            cast_to=CategorizeAudioCreateForUserResponse,
        )


class CategorizeAudioResourceWithRawResponse:
    def __init__(self, categorize_audio: CategorizeAudioResource) -> None:
        self._categorize_audio = categorize_audio

        self.create = to_raw_response_wrapper(
            categorize_audio.create,
        )
        self.create_for_user = to_raw_response_wrapper(
            categorize_audio.create_for_user,
        )


class AsyncCategorizeAudioResourceWithRawResponse:
    def __init__(self, categorize_audio: AsyncCategorizeAudioResource) -> None:
        self._categorize_audio = categorize_audio

        self.create = async_to_raw_response_wrapper(
            categorize_audio.create,
        )
        self.create_for_user = async_to_raw_response_wrapper(
            categorize_audio.create_for_user,
        )


class CategorizeAudioResourceWithStreamingResponse:
    def __init__(self, categorize_audio: CategorizeAudioResource) -> None:
        self._categorize_audio = categorize_audio

        self.create = to_streamed_response_wrapper(
            categorize_audio.create,
        )
        self.create_for_user = to_streamed_response_wrapper(
            categorize_audio.create_for_user,
        )


class AsyncCategorizeAudioResourceWithStreamingResponse:
    def __init__(self, categorize_audio: AsyncCategorizeAudioResource) -> None:
        self._categorize_audio = categorize_audio

        self.create = async_to_streamed_response_wrapper(
            categorize_audio.create,
        )
        self.create_for_user = async_to_streamed_response_wrapper(
            categorize_audio.create_for_user,
        )
