# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CreateUserCreateResponse"]


class CreateUserCreateResponse(BaseModel):
    id: Optional[str] = None
    """User ID"""
