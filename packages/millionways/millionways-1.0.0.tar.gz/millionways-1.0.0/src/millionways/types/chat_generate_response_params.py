# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ChatGenerateResponseParams"]


class ChatGenerateResponseParams(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]

    language: str
    """language parameter, defaults to en"""

    messages: Iterable[object]
    """
    history of messages between user with the role 'user' and chatbot with the role
    'assistant'
    """
