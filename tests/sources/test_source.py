from config_joker.sources.source import SourceAsDict


class MockSource(SourceAsDict):
    def __init__(self, file_path: str, full_source_data: dict, config_path: str = None) -> None:
        self._full_source_data = full_source_data
        super().__init__(file_path, config_path)
    
    def _load_from_file(self, path: str) -> dict:
        return self._full_source_data


class TestSourceAsDict:
    def test_get_existing_key(self):
        yaml_source = MockSource(file_path='path', full_source_data={'key': 'value'})
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

    def test_get_non_existing_key(self):
        yaml_source = MockSource(file_path='path', full_source_data={'key': 'value'})
        result = yaml_source.get_value(key='made_up_key')
        assert result.value == None
        assert result.exists == False

    def test_get_existing_complex_key_key(self):
        return_value =  {
            'key1': {
                'key2': [
                    '', 'value'
                ]
            }
        }
        yaml_source = MockSource(file_path='path', full_source_data=return_value)
        result = yaml_source.get_value(key='key1.key2[1]')
        assert result.value == 'value'
        assert result.exists == True

    def test_get_existing_neasted_dict_config(self):
        return_value =  {
            'config_key': {
                'key': 'value'
            }
        }
        yaml_source = MockSource(file_path='path', full_source_data=return_value, config_path='config_key')
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

    def test_get_existing_neasted_dict_and_list_config(self):
        return_value =  {
            'config_key': [
                {},
                {
                    'key': 'value'
                }
            ]
        }
        yaml_source = MockSource(file_path='path', full_source_data=return_value, config_path='config_key[1]')
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True
