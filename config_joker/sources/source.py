from pydantic import BaseModel
from typing import Any
from abc import ABC, abstractmethod


class SourceResponse(BaseModel):
    exists: bool
    value: Any


class Source(ABC):
    @abstractmethod
    def get_value(self, key: str) -> SourceResponse:
        'Get the value in the source using the key'
