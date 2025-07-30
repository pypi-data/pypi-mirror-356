# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ChatStreamGenerateResponseParams",
    "Levels",
    "Result",
    "ResultEmotions",
    "ResultMotives",
    "ResultPreferences",
]


class ChatStreamGenerateResponseParams(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]

    language: str
    """language parameter, defaults to en"""

    levels: Levels

    messages: Iterable[object]
    """
    history of messages between user with the role 'user' and chatbot with the role
    'assistant'
    """

    result: Result


class Levels(TypedDict, total=False):
    level1: float
    """Intuition Intrinsic"""

    level2: float
    """Intuition Extrinsic"""

    level3: float
    """External managing of frustration"""

    level4: float
    """Analytical / Intentional feelings"""

    level5: float
    """Negative emotions"""


class ResultEmotions(TypedDict, total=False):
    approach: float
    """Approach in percent between 0 and 100."""

    avoidance: float
    """Avoidance in percent between 0 and 100."""


class ResultMotives(TypedDict, total=False):
    achievement: float
    """Achievement motive in percent between 0 and 100."""

    contact: float
    """Contact motive in percent between 0 and 100."""

    power: float
    """Power motive in percent between 0 and 100."""


class ResultPreferences(TypedDict, total=False):
    analytical: float
    """Analytical Orientation in percent between 0 and 100."""

    detail: float
    """Orientation towards Details in percent between 0 and 100."""

    external: float
    """External Orientation in percent between 0 and 100."""

    goal: float
    """Goal-Orientation in percent between 0 and 100."""

    holistic: float
    """Holistic Orientation in percent between 0 and 100."""

    internal: float
    """Internal Orientation in percent between 0 and 100."""

    path: float
    """Path-Orientation in percent between 0 and 100."""

    realization: float
    """Orientation towards Realization in percent between 0 and 100."""


class Result(TypedDict, total=False):
    emotions: ResultEmotions

    motives: ResultMotives

    preferences: ResultPreferences
