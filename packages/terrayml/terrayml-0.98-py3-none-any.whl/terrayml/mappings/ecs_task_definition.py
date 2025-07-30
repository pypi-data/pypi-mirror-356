def generate_mappings(config_key, config_value, other_reference_mappings):
    container_definitions = []
    runtime_platform = {
        "system_family": config_value["runtime-platform"]["system-family"],
        "cpu_architecture": config_value["runtime-platform"]["cpu-architecture"],
    }
    task_execution_role = {
        "allowed_actions": config_value["task-execution-role"]["allowed-actions"],
        "allowed_resources": config_value["task-execution-role"]["allowed-resources"],
    }

    for container_definition in config_value["container-definitions"]:
        port_mappings = []
        environment = []
        for port_mapping in container_definition["port_mappings"]:
            port_mappings.append(
                {
                    "containerPort": port_mapping["container-port"],
                    "hostPort": port_mapping["host-port"],
                }
            )

        for name, value in container_definition.get("variables", {}).items():
            environment.append({"name": name, "value": value})

        container_definitions.append(
            {
                "name": container_definition["name"],
                "image": container_definition["image"],
                "cpu": container_definition["cpu"],
                "memory": container_definition["memory"],
                "essential": str(container_definition["essential"]).upper(),
                "port_mappings": port_mappings,
                "environment": environment,
            }
        )

    return {
        "ECS_TASK_DEFINITION_NAME": config_key,
        "ECS_TASK_DEFINITION_REQUIRED_COMPATIBILITIES": config_value[
            "required-compatibilities"
        ],
        "ECS_TASK_DEFINITION_NETWORK_MODE": config_value["network-mode"],
        "ECS_TASK_DEFINITION_CPU": config_value["cpu"],
        "ECS_TASK_DEFINITION_MEMORY": config_value["memory"],
        "ECS_TASK_DEFINITION_RUNTIME_PLATFORM": runtime_platform,
        "ECS_TASK_DEFINITION_TASK_EXECUTION_ROLE": task_execution_role,
        "ECS_TASK_DEFINITION_CONTAINER_DEFINITIONS": container_definitions,
    }
