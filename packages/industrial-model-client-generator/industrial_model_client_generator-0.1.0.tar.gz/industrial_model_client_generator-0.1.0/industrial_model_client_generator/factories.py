import os
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import Any

import yaml
from cognite.client import CogniteClient
from dotenv import load_dotenv
from industrial_model import DataModelId


@lru_cache
def _get_env_variables() -> dict[str, Any]:
    load_dotenv(override=True)
    file_path = Path(f"{os.path.dirname(__file__)}/cognite-sdk-config.yaml")
    env_sub_template = Template(file_path.read_text())
    file_env_parsed = env_sub_template.substitute(dict(os.environ))

    value = yaml.safe_load(file_env_parsed)

    assert isinstance(value, dict)
    return value


def generate_cognite_client() -> CogniteClient:
    value = _get_env_variables()
    return CogniteClient.load(value["cognite"])


def generate_data_model_id() -> DataModelId:
    value = _get_env_variables()
    return DataModelId.model_validate(value["data_model"])
