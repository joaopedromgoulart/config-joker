from config_joker.sources.source import Source, SourceResponse
from typing import List, Any, Callable


class RequiredKeyNotFound(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f'Could not find the key "{key}"')


class Config:
    def __init__(self, sources: List[Source]) -> None:
        self._sources = sources

    def _get(self, key: str) -> SourceResponse:
        'Iters in the list of sources until it finds the key in one of them.'
        for source in self._sources:
            result = source.get_value(key=key)
            if result.exists:
                return result
        return result

    def required(self, key: str, value_type: Callable = None) -> Any:
        source_response = self._get(key=key)
        if not source_response.exists:
            raise RequiredKeyNotFound(key=key)
        result = source_response.value
        if value_type:
            result = value_type(result)
        return result

    def optional(self, key: str, value_type: Callable = None, default: Any = None) -> Any:
        source_response = self._get(key=key)
        if not source_response.exists:
            return default
        result = source_response.value
        if value_type:
            result = value_type(result)
        return result
