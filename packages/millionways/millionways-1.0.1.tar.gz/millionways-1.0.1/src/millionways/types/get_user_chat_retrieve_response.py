# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "GetUserChatRetrieveResponse",
    "User",
    "UserChatCall",
    "UserChatCallResult",
    "UserChatCallResultEmotions",
    "UserChatCallResultMotives",
    "UserChatCallResultPreferences",
]


class UserChatCallResultEmotions(BaseModel):
    approach: Optional[float] = None
    """Approach in percent between 0 and 100."""

    avoidance: Optional[float] = None
    """Avoidance in percent between 0 and 100."""


class UserChatCallResultMotives(BaseModel):
    achievement: Optional[float] = None
    """Achievement motive in percent between 0 and 100."""

    contact: Optional[float] = None
    """Contact motive in percent between 0 and 100."""

    power: Optional[float] = None
    """Power motive in percent between 0 and 100."""


class UserChatCallResultPreferences(BaseModel):
    analytical: Optional[float] = None
    """Analytical Orientation in percent between 0 and 100."""

    detail: Optional[float] = None
    """Orientation towards Details in percent between 0 and 100."""

    external: Optional[float] = None
    """External Orientation in percent between 0 and 100."""

    goal: Optional[float] = None
    """Goal-Orientation in percent between 0 and 100."""

    holistic: Optional[float] = None
    """Holistic Orientation in percent between 0 and 100."""

    internal: Optional[float] = None
    """Internal Orientation in percent between 0 and 100."""

    path: Optional[float] = None
    """Path-Orientation in percent between 0 and 100."""

    realization: Optional[float] = None
    """Orientation towards Realization in percent between 0 and 100."""


class UserChatCallResult(BaseModel):
    emotions: Optional[UserChatCallResultEmotions] = None

    motives: Optional[UserChatCallResultMotives] = None

    preferences: Optional[UserChatCallResultPreferences] = None


class UserChatCall(BaseModel):
    messages: Optional[List[object]] = None
    """
    history of messages between user with the role 'user' and chatbot with the role
    'assistant'
    """

    result: Optional[UserChatCallResult] = None


class User(BaseModel):
    chat_calls: Optional[List[UserChatCall]] = FieldInfo(alias="chatCalls", default=None)

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)
    """Date of last update"""

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)
    """User id"""


class GetUserChatRetrieveResponse(BaseModel):
    user: Optional[User] = None
