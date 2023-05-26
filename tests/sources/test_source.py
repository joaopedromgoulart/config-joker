import pytest

from typing import Optional
from config_joker.sources.source import ConfigStructure, SourceAsDict


class MockSource(SourceAsDict):
    def __init__(self,
                 full_source_data: str,
                 file_path: str,
                 config_path: str = None,
                 config_scructure: Optional[ConfigStructure] = None,
                 key_name: Optional[str] = None,
                 value_name: Optional[str] = None) -> None:
        self._full_source_data = full_source_data
        super().__init__(file_path, config_path, config_scructure, key_name, value_name)
    
    def _load_from_file(self, path: str) -> dict:
        return self._full_source_data


def setup_source(inputs_to_update: Optional[dict] = None) -> MockSource:
    default_config = {
        'full_source_data': {'key': 'value'},
        'file_path': 'path'
        }
    if inputs_to_update:
        default_config.update(inputs_to_update)
    return MockSource(**default_config)


class TestSourceAsDict:
    def test_get_existing_key(self):
        yaml_source = setup_source()
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

    def test_get_non_existing_key(self):
        yaml_source = setup_source()
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
        yaml_source = setup_source({'full_source_data':return_value})
        result = yaml_source.get_value(key='key1.key2[1]')
        assert result.value == 'value'
        assert result.exists == True

    def test_get_existing_neasted_dict_config(self):
        return_value =  {
            'config_key': {
                'key': 'value'
            }
        }
        yaml_source = setup_source({'full_source_data':return_value, 'config_path': 'config_key'})
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
        yaml_source = setup_source({'full_source_data':return_value, 'config_path': 'config_key[1]'})
        result = yaml_source.get_value(key='key')
        assert result.value == 'value'
        assert result.exists == True

class TestSourceAsDictConfigStructure:
    @pytest.mark.parametrize(
            'input_update',
            [
                {},
                {'key_name': 'any-key'},
                {'value_name': 'any-value'},
            ]
    )
    def test_missing_keyname_or_valuename(self, input_update):
        source_inputs = {'config_scructure': ConfigStructure.LIST_OF_DICTS}
        source_inputs.update(input_update)
        with pytest.raises(KeyError):
            _ = setup_source(source_inputs)

    def test_conversion_ok(self):
        source_inputs = {
            'config_scructure': ConfigStructure.LIST_OF_DICTS,
            'key_name': 'name',
            'value_name': 'value',
            'full_source_data': [{
                'name': 'key1',
                'value': 'value1'
            }]
        }
        source = setup_source(source_inputs)
        assert source._data == {'key1': 'value1'}
