import pytest
from unittest.mock import patch

from config_joker.config import (Config, Source, SourceResponse, RequiredKeyNotFound,
                                 ValueNotConvertable)


def build_default_config(source_data: dict = None) -> Config:
    source_data if source_data else {'key': '1'}
    return Config(
            sources=[
                MockSource(dict_source={'key': '1'})
            ]
        )


class MockSource(Source):
    def __init__(self, dict_source: dict) -> None:
        self._source_data = dict_source
    
    def get_value(self, key: str) -> SourceResponse:
        try:
            return SourceResponse(
                exists=True,
                value=self._source_data[key]
            )
        except KeyError:
            return SourceResponse(
                exists=False,
                value=None
            )


class TestCastBool:
    @pytest.mark.parametrize(
        'text_value, expected_result',
        [
            ('True', True),
            ('TRUE', True),
            ('true', True),
            ('1', True),
            ('False', False),
            ('FALSE', False),
            ('false', False),
            ('0', False),
        ]
    )
    def test_cast_int_to_bool_ok(self, text_value: str, expected_result: str):
        config = build_default_config()
        assert config._cast_bool(text_value) == expected_result

    def test_cast_int_to_bool_nok(self):
        config = build_default_config()
        with pytest.raises(ValueNotConvertable):
            _ = config._cast_bool('wrog-string')

    def test_required_bool(self):
        config = build_default_config(source_data={'key': 'True'})
        assert config.required(key='key', value_type=bool) == True

    def test_optional_bool(self):
        config = build_default_config(source_data={'key': 'True'})
        assert config.optional(key='key', value_type=bool) == True


class TestConvertValue:
    @pytest.mark.parametrize(
            'value, value_type, result',
            [
                ('True', bool, 'fake-return'),
                ('True', str, 'True'),
                (0, bool, False)
            ]
    )
    def test_convert_values(self, value, value_type, result):
        with patch.object(Config, '_cast_bool') as mock_cast_bool:
            mock_cast_bool.return_value = 'fake-return'
            config = build_default_config()
            assert config._convert_value(value=value, value_type=value_type) == result
            if value_type == bool and value == True:
                mock_cast_bool.assert_awaited_with('True')


class TestConfigGet:
    def test_get_findig_value(self):
        config = build_default_config()
        result = config._get(key='key')
        assert result.exists
        assert result.value == '1'
    
    def test_get_not_finding_value(self):
        config = build_default_config()
        result = config._get(key='made_up_key')
        assert not result.exists
        assert result.value is None

    def test_get_key_from_first_source(self):
        config = Config(
            sources=[
                MockSource(dict_source={'key': 'value1'}),
                MockSource(dict_source={'key': 'value2'})
            ]
        )
        result = config._get(key='key')
        assert result.exists
        assert result.value == 'value1'

    def test_get_key_from_last_source(self):
        config = Config(
            sources=[
                MockSource(dict_source={'other_key': 'value1'}),
                MockSource(dict_source={'other_key': 'value2'}),
                MockSource(dict_source={'key': 'value3'})
            ]
        )
        result = config._get(key='key')
        assert result.exists
        assert result.value == 'value3'


class TestConfigRequired:
    def test_find_required_value_with_no_type_selection(self):
        config = build_default_config()
        assert config.required(key='key') == '1'
        
    def test_find_required_value_with_type_selection(self):
        config = build_default_config()
        assert config.required(key='key', value_type=int) == 1

    def test_dont_find_required_value(self):
        config = build_default_config()
        with pytest.raises(RequiredKeyNotFound):
            config.required(key='made_up_key')


class TestConfigOptional:
    def test_find_optional_value_with_no_type_selection(self):
        config = build_default_config()
        assert config.optional(key='key') == '1'

    def test_find_optional_value_with_type_selection(self):
        config = build_default_config()
        assert config.optional(key='key', value_type=int) == 1

    def test_dont_find_optional_value_without_default(self):
        config = build_default_config()
        assert config.optional(key='made_up_key') == None

    def test_dont_find_optional_value_with_default(self):
        config = build_default_config()
        assert config.optional(key='made_up_key', default='value') == 'value'

    def test_dont_find_optional_value_with_default_and_type_selection(self):
        'The type selection cant impact in the default response'
        config = build_default_config()
        assert config.optional(key='made_up_key', value_type=int ,default='1') == '1'
