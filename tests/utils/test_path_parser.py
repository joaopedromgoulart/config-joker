import pytest

from typing import Union

from config_joker.utils.parser import path_parser, transform_splited_by_brackets, flatten, dict_extractor



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