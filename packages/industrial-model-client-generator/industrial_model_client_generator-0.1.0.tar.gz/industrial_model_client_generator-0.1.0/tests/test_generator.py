from industrial_model_client_generator import InstanceSpaceConfig, generate


def test_generator() -> None:
    client_name = "Testing"
    instance_space_configs = [
        InstanceSpaceConfig(
            view_or_space_external_id="FRP-COR-ALL-DML", instance_spaces_prefix="FRP-"
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="UMG-COR-ALL-DMD",
            instance_spaces=["UMG-COR-ALL-DAT"],
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="EDG-COR-ALL-DMD",
            instance_spaces=["REF-COR-ALL-DAT"],
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="Equipment", instance_spaces_prefix="SAP-"
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="FunctionalLocation",
            instance_spaces_prefix="SAP-",
        ),
    ]

    generate(
        client_name, instance_space_configs=instance_space_configs, output_path="output"
    )
