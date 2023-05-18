from config_joker import Config, YamlFileSource


def example():
    config = Config(
        sources=[
            YamlFileSource(
                file_path='./examples/yaml/config.yaml',
                config_path='external_config_key[0].config'
            )
        ]
    )
    print(config.required(key='external_key[0]key'))


if __name__== '__main__':
    example()