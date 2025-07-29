from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class TestWebhookResponse:
    state: int
    result: list

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> TestWebhookResponse:
        return cls(state=data["state"], result=data["result"])