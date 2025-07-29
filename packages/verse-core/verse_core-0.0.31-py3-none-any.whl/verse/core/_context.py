from __future__ import annotations

from typing import Any

from .data_model import DataModel


class Context(DataModel):
    id: str
    data: dict[str, Any] | None = None
