from unittest.mock import patch, mock_open
from config_joker.sources.yamlfile import YamlFileSource


class TestYamlFileSourceGetValue:
    def test_load_from_file(self):
        file_data = 'config:\n  key: value'
        with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
            yaml_source = YamlFileSource(file_path='path')
        assert yaml_source._data == {'config': {'key': 'value'}}