# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CategorizeTextClassifyByUserParams"]


class CategorizeTextClassifyByUserParams(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]

    language: str
    """language parameter, defaults to en"""

    text: str
    """text input to be classified"""
