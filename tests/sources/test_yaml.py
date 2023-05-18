from unittest import mock
from config_joker.sources.yamlfile import YamlFileSource


class TestYamlFileSourceGetValue:
    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_existing_key(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {'key': 'value'}
        with mock.patch('builtins.open', mock.MagicMock()):
            yaml_source = YamlFileSource(file_path='path')
        mock_yaml_file.assert_called()
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_non_existing_key(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {'key': 'value'}
        with mock.patch('builtins.open', mock.MagicMock()):
            yaml_source = YamlFileSource(file_path='path')
        mock_yaml_file.assert_called()
        result = yaml_source.get_value(key='made_up_key')
        assert result.value == None
        assert result.exists == False

    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_existing_complex_key_key(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {
            'key1': {
                'key2': [
                    '', 'value'
                ]
            }
        }
        with mock.patch('builtins.open', mock.MagicMock()):
            yaml_source = YamlFileSource(file_path='path')
        mock_yaml_file.assert_called()
        result = yaml_source.get_value(key='key1.key2[1]')
        assert result.value == 'value'
        assert result.exists == True
    
    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_existing_neasted_dict_config(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {
            'config_key': {
                'key': 'value'
            }
        }
        with mock.patch('builtins.open', mock.MagicMock()):
            yaml_source = YamlFileSource(file_path='path', config_path='config_key')
        mock_yaml_file.assert_called()
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True
    
    @mock.patch('config_joker.sources.yamlfile.safe_load')
    def test_get_existing_neasted_dict_and_list_config(self, mock_yaml_file: mock.MagicMock):
        mock_yaml_file.return_value =  {
            'config_key': [
                {},
                {
                    'key': 'value'
                }
            ]
        }
        with mock.patch('builtins.open', mock.MagicMock()):
            yaml_source = YamlFileSource(file_path='path', config_path='config_key[1]')
        mock_yaml_file.assert_called()
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True
