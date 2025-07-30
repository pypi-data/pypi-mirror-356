# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "MentalHealthChatbotGenerateResponseResponse",
    "Levels",
    "Result",
    "ResultEmotions",
    "ResultMotives",
    "ResultPreferences",
]


class Levels(BaseModel):
    level1: Optional[float] = None
    """Intuition Intrinsic"""

    level2: Optional[float] = None
    """Intuition Extrinsic"""

    level3: Optional[float] = None
    """External managing of frustration"""

    level4: Optional[float] = None
    """Analytical / Intentional feelings"""

    level5: Optional[float] = None
    """Negative emotions"""


class ResultEmotions(BaseModel):
    approach: Optional[float] = None
    """Approach in percent between 0 and 100."""

    avoidance: Optional[float] = None
    """Avoidance in percent between 0 and 100."""


class ResultMotives(BaseModel):
    achievement: Optional[float] = None
    """Achievement motive in percent between 0 and 100."""

    contact: Optional[float] = None
    """Contact motive in percent between 0 and 100."""

    power: Optional[float] = None
    """Power motive in percent between 0 and 100."""


class ResultPreferences(BaseModel):
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


class Result(BaseModel):
    emotions: Optional[ResultEmotions] = None

    motives: Optional[ResultMotives] = None

    preferences: Optional[ResultPreferences] = None


class MentalHealthChatbotGenerateResponseResponse(BaseModel):
    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    levels: Optional[Levels] = None

    response: Optional[str] = None
    """response from chatbot"""

    result: Optional[Result] = None
