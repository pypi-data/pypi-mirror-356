# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["SalesAssistantGenerateInsightsResponse"]


class SalesAssistantGenerateInsightsResponse(BaseModel):
    assist: Optional[str] = None
    """Assisted advice for the sales rep."""

    conversion: Optional[float] = None
    """Score between 0 and 100 assessing the likelihood of the customer conversion."""

    interests: Optional[str] = None
    """Customer's interests and preferences."""

    response: Optional[str] = None
    """Recommended response for what to say next in the conversation."""

    stay_away_from: Optional[str] = None
    """Customer's dislikes or things they want to avoid."""
