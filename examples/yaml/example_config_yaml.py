from config_joker import Config, YamlFileSource, ConfigStructure


def example_1():
    config = Config(
        sources=[
            YamlFileSource(
                file_path='./examples/yaml/config.yaml',
                config_path='external_config_key[0].config'
            )
        ]
    )
    print(config.required(key='external_key[0]key'))

def example_2():
    'Getting values from a list of dicts'
    config = Config(
        sources=[
            YamlFileSource(
                file_path='./examples/yaml/config.yaml',
                config_path='external_config_key[1].config',
                config_scructure=ConfigStructure.LIST_OF_DICTS,
                key_name='name',
                value_name='value'
            )
        ]
    )
    print(config.required(key='key1'))


if __name__== '__main__':
    example_2()