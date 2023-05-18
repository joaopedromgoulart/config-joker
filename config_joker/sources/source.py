from typing import Any
from abc import ABC, abstractmethod

from dataclasses import dataclass
from config_joker.utils.parser import dict_extractor


@dataclass
class SourceResponse:
    exists: bool
    value: Any


class Source(ABC):
    @abstractmethod
    def get_value(self, key: str) -> SourceResponse:
        'Get the value in the source using the key'


class SourceAsDict(Source):
    def __init__(self, file_path: str, config_path: str = None) -> None:
        self._file_contents = self._load_from_file(file_path)
        if config_path:
            self._data = dict_extractor(path=config_path, data=self._file_contents)
        else:
            self._data = self._file_contents

    def _load_from_file(self, path: str) -> dict:
        raise NotImplementedError()

    def get_value(self, key: str) -> SourceResponse:
        try:
            response = dict_extractor(path=key, data=self._data)
            return SourceResponse(
                exists=True,
                value=response
            )
        except KeyError:
            return SourceResponse(
                exists=False,
                value=None
            )