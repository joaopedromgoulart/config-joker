import json

from config_joker.sources.source import Source, SourceResponse
from config_joker.utils.parser import dict_extractor


class JsonFileSource(Source):
    def __init__(self, file_path: str, config_path: str = None) -> None:
        with open(file_path) as f:
            self._file_contents = json.load(f)
        if config_path:
            self._data = dict_extractor(path=config_path, data=self._file_contents)
        else:
            self._data = self._file_contents

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
