# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["GetUserRetrieveResponse", "User"]


class User(BaseModel):
    api_id: Optional[str] = FieldInfo(alias="_id", default=None)
    """User id"""

    api_calls: Optional[List[str]] = FieldInfo(alias="apiCalls", default=None)
    """Array containing the IDs of all API Calls associated with this User"""

    created_at: Optional[str] = FieldInfo(alias="createdAt", default=None)
    """Date of creation"""

    customer_id: Optional[str] = FieldInfo(alias="customerId", default=None)
    """Customer ID that the User belongs to"""

    updated_at: Optional[str] = FieldInfo(alias="updatedAt", default=None)
    """Date of last update"""


class GetUserRetrieveResponse(BaseModel):
    user: Optional[User] = None
