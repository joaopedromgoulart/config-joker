from typing import Any
from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class SourceResponse:
    exists: bool
    value: Any


class Source(ABC):
    @abstractmethod
    def get_value(self, key: str) -> SourceResponse:
        'Get the value in the source using the key'

s = SourceResponse(**{"exists": True, "value": "1"})