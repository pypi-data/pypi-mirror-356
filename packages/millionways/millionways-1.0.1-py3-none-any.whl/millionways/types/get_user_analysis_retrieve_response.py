# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "GetUserAnalysisRetrieveResponse",
    "User",
    "UserTextCall",
    "UserTextCallResult",
    "UserTextCallResultEmotions",
    "UserTextCallResultMotives",
    "UserTextCallResultPreferences",
]


class UserTextCallResultEmotions(BaseModel):
    approach: Optional[float] = None
    """Approach in percent between 0 and 100."""

    avoidance: Optional[float] = None
    """Avoidance in percent between 0 and 100."""


class UserTextCallResultMotives(BaseModel):
    achievement: Optional[float] = None
    """Achievement motive in percent between 0 and 100."""

    contact: Optional[float] = None
    """Contact motive in percent between 0 and 100."""

    power: Optional[float] = None
    """Power motive in percent between 0 and 100."""


class UserTextCallResultPreferences(BaseModel):
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


class UserTextCallResult(BaseModel):
    emotions: Optional[UserTextCallResultEmotions] = None

    motives: Optional[UserTextCallResultMotives] = None

    preferences: Optional[UserTextCallResultPreferences] = None


class UserTextCall(BaseModel):
    result: Optional[UserTextCallResult] = None

    text: Optional[str] = None
    """Text transcribed from audio input"""


class User(BaseModel):
    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    text_calls: Optional[List[UserTextCall]] = FieldInfo(alias="textCalls", default=None)

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)
    """Date of last update"""

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)
    """User id"""


class GetUserAnalysisRetrieveResponse(BaseModel):
    user: Optional[User] = None
