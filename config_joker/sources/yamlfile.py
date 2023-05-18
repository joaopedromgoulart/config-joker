from yaml import safe_load

from config_joker.sources.source import Source, SourceResponse
from config_joker.utils.parser import dict_extractor


class YamlFileSource(Source):
    def __init__(self, file_path: str, config_path: str = None) -> None:
        self._file_path = file_path
        self._file_contents = safe_load(self._file_path)
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
