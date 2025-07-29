# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ModelListResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    input_token_price: Optional[float] = None

    is_active: Optional[bool] = None

    name: Optional[str] = None

    object: Optional[str] = None

    output_token_price: Optional[float] = None


class ModelListResponse(BaseModel):
    data: Optional[List[Data]] = None

    object: Optional[str] = None
