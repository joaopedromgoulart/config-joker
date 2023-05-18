from config_joker import Config, YamlFileSource

def example():
    config_x = Config(
        sources=[
            YamlFileSource(
                file_path='./examples/yaml/config.yaml',
                config_path='external_config_key[0].config_x'
            )
        ]
    )
    print(config_x.required(key='external_key[0]key_x'))
