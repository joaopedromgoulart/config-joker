from yaml import safe_load

from config_joker.sources.source import Source, SourceResponse
from config_joker.utils.parser import dict_extractor


class YamlFileSource(Source):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._data = safe_load(self._file_path)

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
