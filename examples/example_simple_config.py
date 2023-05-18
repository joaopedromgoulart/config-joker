
def example_config():
    # preparing environment to run example
    import os
    os.environ['KEY'] = 'VALUE'

    # Running example
    from config_joker import Config, EnvironmentSource

    config = Config(
        sources=[
            EnvironmentSource()
        ]
    )
    print(config.required(key='KEY', value_type=str))


if __name__=='__main__':
    example_config()
