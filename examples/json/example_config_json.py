from config_joker import Config, JsonFileSource


def example():
    config = Config(
        sources=[
            JsonFileSource(
                file_path='./examples/json/config.json',
                config_path='external_config_key[0].config'
            )
        ]
    )
    print(config.required(key='external_key[0]key'))


if __name__== '__main__':
    example()