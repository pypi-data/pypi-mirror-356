from pathlib import Path

from industrial_model_client_generator import generate
from industrial_model_client_generator.config import Config

config_path = Path("tests/generator-config.yaml")


def test_generator() -> None:
    generate(config_path=config_path)


def test_config_init() -> None:
    config = Config.from_config(config_path=config_path)
    assert config is not None
    print(config)
