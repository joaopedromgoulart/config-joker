from unittest import mock
from config_joker.sources.yamlfile import YamlFileSource


class TestYamlFileSourceGetValue:
    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_existing_key(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {'key': 'value'}
        yaml_source = YamlFileSource(file_path='path')
        mock_yaml_file.assert_called_with('path')
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_non_existing_key(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {'key': 'value'}
        yaml_source = YamlFileSource(file_path='path')
        mock_yaml_file.assert_called_with('path')
        result = yaml_source.get_value(key='made_up_key')
        assert result.value == None
        assert result.exists == False
