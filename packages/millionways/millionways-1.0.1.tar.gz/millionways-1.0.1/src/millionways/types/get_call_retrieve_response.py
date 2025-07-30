# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "GetCallRetrieveResponse",
    "Call",
    "CallLevels",
    "CallResponses",
    "CallResponsesMotives",
    "CallResponsesPreferences",
    "CallResult",
    "CallResultEmotions",
    "CallResultMotives",
    "CallResultPreferences",
]


class CallLevels(BaseModel):
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


class CallResponsesMotives(BaseModel):
    achievement: Optional[str] = None
    """Achievement motive response"""

    contact: Optional[str] = None
    """Contact motive response"""

    power: Optional[str] = None
    """Power motive response"""


class CallResponsesPreferences(BaseModel):
    action: Optional[str] = None
    """Action response"""

    attitude: Optional[str] = None
    """Attitude response"""

    energy: Optional[str] = None
    """Energy response"""

    focus: Optional[str] = None
    """Focus response"""


class CallResponses(BaseModel):
    emotions: Optional[str] = None
    """Emotions response"""

    motives: Optional[CallResponsesMotives] = None

    preferences: Optional[CallResponsesPreferences] = None


class CallResultEmotions(BaseModel):
    approach: Optional[float] = None
    """Approach in percent between 0 and 100."""

    avoidance: Optional[float] = None
    """Avoidance in percent between 0 and 100."""


class CallResultMotives(BaseModel):
    achievement: Optional[float] = None
    """Achievement motive in percent between 0 and 100."""

    contact: Optional[float] = None
    """Contact motive in percent between 0 and 100."""

    power: Optional[float] = None
    """Power motive in percent between 0 and 100."""


class CallResultPreferences(BaseModel):
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


class CallResult(BaseModel):
    emotions: Optional[CallResultEmotions] = None

    motives: Optional[CallResultMotives] = None

    preferences: Optional[CallResultPreferences] = None


class Call(BaseModel):
    api_id: Optional[str] = FieldInfo(alias="_id", default=None)
    """Call id"""

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    customer_id: Optional[str] = FieldInfo(alias="customerId", default=None)
    """Customer ID that the Call belongs to"""

    language: Optional[str] = None
    """Language used for the Call"""

    levels: Optional[CallLevels] = None

    responses: Optional[CallResponses] = None

    result: Optional[CallResult] = None

    text: Optional[str] = None
    """Text input"""

    type: Optional[str] = None
    """Type of the call"""

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)
    """Date of last update"""

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)
    """User ID that the Call belongs to"""


class GetCallRetrieveResponse(BaseModel):
    call: Optional[Call] = None
