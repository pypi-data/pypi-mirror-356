# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "CategorizeAudioCreateResponse",
    "CandidateTexts",
    "CandidateTextsMotives",
    "CandidateTextsPreferences",
    "Levels",
    "Responses",
    "ResponsesMotives",
    "ResponsesPreferences",
    "Result",
    "ResultEmotions",
    "ResultMotives",
    "ResultPreferences",
]


class CandidateTextsMotives(BaseModel):
    achievement: Optional[str] = None
    """Achievement motive response"""

    contact: Optional[str] = None
    """Contact motive response"""

    power: Optional[str] = None
    """Power motive response"""


class CandidateTextsPreferences(BaseModel):
    action: Optional[str] = None
    """Action response"""

    attitude: Optional[str] = None
    """Attitude response"""

    energy: Optional[str] = None
    """Energy response"""

    focus: Optional[str] = None
    """Focus response"""


class CandidateTexts(BaseModel):
    emotions: Optional[str] = None
    """Emotions response"""

    levels: Optional[str] = None
    """Levels response"""

    motives: Optional[CandidateTextsMotives] = None

    preferences: Optional[CandidateTextsPreferences] = None


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


class ResponsesMotives(BaseModel):
    achievement: Optional[str] = None
    """Achievement motive response"""

    contact: Optional[str] = None
    """Contact motive response"""

    power: Optional[str] = None
    """Power motive response"""


class ResponsesPreferences(BaseModel):
    action: Optional[str] = None
    """Action response"""

    attitude: Optional[str] = None
    """Attitude response"""

    energy: Optional[str] = None
    """Energy response"""

    focus: Optional[str] = None
    """Focus response"""


class Responses(BaseModel):
    emotions: Optional[str] = None
    """Emotions response"""

    levels: Optional[str] = None
    """Levels response"""

    motives: Optional[ResponsesMotives] = None

    preferences: Optional[ResponsesPreferences] = None


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


class CategorizeAudioCreateResponse(BaseModel):
    candidate_texts: Optional[CandidateTexts] = FieldInfo(alias="candidateTexts", default=None)

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    levels: Optional[Levels] = None

    responses: Optional[Responses] = None

    result: Optional[Result] = None

    text: Optional[str] = None
    """Text transcribed from audio input"""
