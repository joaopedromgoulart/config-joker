import pytest
import os

from unittest import mock
from config_joker.sources.environment import EnvironmentSource


class TestEnvironmentSource:
    @mock.patch.dict(os.environ, {"rigth_key": "value"})
    @pytest.mark.parametrize(
        'key, expected_value, exists',
        [
            ('rigth_key', 'value', True),
            ('wrong_key', None, False)
        ]
    )
    def test_existing_key(self, key, expected_value, exists):
        environment_source = EnvironmentSource()
        source_response = environment_source.get_value(key)
        assert source_response.value == expected_value
        assert source_response.exists == exists
    