from industrial_model_client_generator import generate
from industrial_model_client_generator.config import Config


def test_generator() -> None:
    generate()


def test_config_init() -> None:
    config = Config.from_config()
    assert config is not None
    print(config)
