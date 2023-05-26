import pytest

from typing import Union

from config_joker.utils.parser import (path_parser, transform_splited_by_brackets, flatten, dict_extractor,
                                       parse_list_of_dicts, MissingKeyNameInListOfDicts)



@pytest.mark.parametrize('value, expected_response', (['a', 'a'], ['1', 1]))
def test_transform_splited_by_brackets(value: str, expected_response: Union[int, str]):
    assert transform_splited_by_brackets(value=value) == expected_response


@pytest.mark.parametrize(
        'lst, expected_output_lst', 
        [
            ([['1', '2'], 1], ['1', '2', 1]),
            ([1], [1]),
        ]
)
def test_flatten(lst: list, expected_output_lst: list):
    assert flatten(lst) == expected_output_lst


def test_path_parser_dot_only_strings():
    assert path_parser(path='p1.p2.p3') == ['p1', 'p2', 'p3']


def test_path_parser_dot_only_list_pos():
    assert path_parser(path='[0][1][2]') == [0, 1, 2]


def test_path_parser_dot_string_and_list_pos():
    assert path_parser(path='a[1].b') == ['a', 1, 'b']

def test_dict_extractor():
    source_data = {
        'key1': [
            {},
            {'key2': 'value'}
        ]
    }
    assert dict_extractor(path='key1[1].key2', data=source_data) == 'value'

class TestListOfDictsParser:
    def test_data_ok(self):
        data = [{'key_name': 'key1', 'value_name': 'value1'}]
        parsed_response = parse_list_of_dicts(data=data, k_name='key_name', v_name='value_name')
        assert parsed_response == {'key1': 'value1'}

    def test_data_missing_keyname(self):
        data = [{'wrong-name': 'key1', 'value_name': 'value1'}]
        with pytest.raises(MissingKeyNameInListOfDicts):
            _ = parse_list_of_dicts(data=data, k_name='key_name', v_name='value_name')
        
    def test_wrong_data_type(self):
        data = 'wrong-type'
        with pytest.raises(TypeError):
            _ = parse_list_of_dicts(data=data, k_name='key_name', v_name='value_name')
