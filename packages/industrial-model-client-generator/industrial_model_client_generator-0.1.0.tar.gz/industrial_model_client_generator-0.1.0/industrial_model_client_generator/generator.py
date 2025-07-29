import os
import shutil
import subprocess

from cognite.client import CogniteClient
from cognite.client.data_classes.data_modeling import View
from industrial_model import DataModelId
from jinja2 import Environment, FileSystemLoader

from industrial_model_client_generator.factories import (
    generate_cognite_client,
    generate_data_model_id,
)

from .helpers import to_snake
from .models import InstanceSpaceConfig, ViewDefinition


def generate(
    client_name: str,
    instance_space_configs: list[InstanceSpaceConfig] | None = None,
    output_path: str | None = None,
) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_dir + "/templates"))

    instance_space_configs_as_dict = {
        config.view_or_space_external_id: config
        for config in instance_space_configs or []
    }
    view_definitions: list[ViewDefinition] = []

    views = _get_views(
        cognite_client=generate_cognite_client(),
        data_model_id=generate_data_model_id(),
    )
    for view in sorted(views, key=lambda v: v.external_id):
        instance_space_config = instance_space_configs_as_dict.get(
            view.external_id
        ) or instance_space_configs_as_dict.get(view.space)

        view_definitions.append(
            ViewDefinition.from_view(
                view,
                instance_space_config,
            )
        )

    output_path = output_path or to_snake(client_name)

    os.makedirs(output_path, exist_ok=True)
    shutil.rmtree(output_path)

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(output_path + "/models", exist_ok=True)
    with open(f"{output_path}/models/__init__.py", "w") as f:
        f.write("")

    os.makedirs(output_path + "/requests", exist_ok=True)
    with open(f"{output_path}/requests/__init__.py", "w") as f:
        f.write("")

    paths = {
        "__init__.j2": f"{output_path}/__init__.py",
        "clients_facade.j2": f"{output_path}/clients_facade.py",
        "clients_sync.j2": f"{output_path}/clients_sync.py",
        "clients_async.j2": f"{output_path}/clients_async.py",
        "requests_aggregation.j2": f"{output_path}/requests/aggregation.py",
        "requests_base.j2": f"{output_path}/requests/base.py",
        "requests_query.j2": f"{output_path}/requests/query.py",
        "requests_search.j2": f"{output_path}/requests/search.py",
        "models_aggregation.j2": f"{output_path}/models/aggregation.py",
        "models_entity.j2": f"{output_path}/models/entity.py",
        "models_entity_complete.j2": f"{output_path}/models/entity_complete.py",
        "models_search.j2": f"{output_path}/models/search.py",
    }
    for template_name, path in paths.items():
        template = env.get_template(template_name)
        entities_content = template.render(
            {
                "view_definitions": view_definitions,
                "client_name": client_name,
            }
        )

        with open(path, "w") as f:
            f.write(entities_content)

    subprocess.run(["ruff", "format", output_path])
    subprocess.run(["ruff", "check", "--fix", output_path])


def _get_views(cognite_client: CogniteClient, data_model_id: DataModelId) -> list[View]:
    return (
        cognite_client.data_modeling.data_models.retrieve(
            ids=data_model_id.as_tuple(), inline_views=True
        )
        .latest_version()
        .views
    )
