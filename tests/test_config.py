import pytest

from config_joker.config import Config, Source, SourceResponse, RequiredKeyNotFound


def build_default_config() -> Config:
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
        
    def test_find_required_value_with_type_convertion(self):
        config = build_default_config()
        assert config.required(key='key', value_type=int) == 1

    def test_find_required_value_whithout_response_from_sources(self):
        config = build_default_config()
        with pytest.raises(RequiredKeyNotFound):
            config.required(key='made_up_key')
