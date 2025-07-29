# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional

from .._models import BaseModel

__all__ = ["ChatGenerateCompletionResponse", "Choice"]


class Choice(BaseModel):
    finish_reason: Optional[str] = None

    index: Optional[int] = None

    message: Optional[object] = None


class ChatGenerateCompletionResponse(BaseModel):
    id: Optional[str] = None

    choices: Optional[List[Choice]] = None

    created: Optional[int] = None

    model: Optional[str] = None

    object: Optional[str] = None

    usage: Optional[builtins.object] = None
