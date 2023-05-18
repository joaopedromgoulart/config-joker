from unittest.mock import patch, mock_open
from config_joker.sources.jsonfile import JsonFileSource


class TestJsonFileSourceGetValue:
    def test_load_from_file(self):
        file_data = """{"config":  {"key": "value"}}"""
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
            json_source = JsonFileSource(file_path='path')
        assert json_source._data == {'config': {'key': 'value'}}