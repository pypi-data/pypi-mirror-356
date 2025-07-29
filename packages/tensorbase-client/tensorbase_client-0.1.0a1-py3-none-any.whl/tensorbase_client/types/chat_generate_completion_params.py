# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatGenerateCompletionParams", "Message"]


class ChatGenerateCompletionParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]

    model: Required[str]

    max_tokens: int

    stream: bool

    temperature: float

    tool_choice: str

    tools: Iterable[object]


class Message(TypedDict, total=False):
    content: str

    name: str

    role: Literal["system", "user", "assistant", "tool"]

    tool_calls: Iterable[object]
