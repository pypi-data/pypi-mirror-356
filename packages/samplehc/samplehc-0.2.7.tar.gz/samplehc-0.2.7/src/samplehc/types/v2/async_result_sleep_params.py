# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AsyncResultSleepParams", "Variant0", "Variant1"]


class Variant0(TypedDict, total=False):
    delay: Required[float]
    """The number of milliseconds to wait before completing the async result."""

    result: Dict[str, object]
    """Optional object that will be returned as the result once the delay has elapsed."""


class Variant1(TypedDict, total=False):
    resume_at: Required[Annotated[str, PropertyInfo(alias="resumeAt")]]
    """An ISO-8601 string specifying when the async result should be completed."""

    result: Dict[str, object]
    """Optional object that will be returned as the result at the specified time."""


AsyncResultSleepParams: TypeAlias = Union[Variant0, Variant1]
