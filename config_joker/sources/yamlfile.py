from yaml import safe_load

from config_joker.sources.source import Source, SourceResponse


class YamlFileSource(Source):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._data = safe_load(self._file_path)

    def get_value(self, key: str) -> SourceResponse:
        try:
            response = self._data[key]
            return SourceResponse(
                exists=True,
                value=response
            )
        except KeyError:
            return SourceResponse(
                exists=False,
                value=None
            )
