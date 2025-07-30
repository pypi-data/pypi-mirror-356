# str(value.get("mutable", True)).upper()


def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "ECS_CLUSTER_NAME": config_key,
        "ECS_CLUSTER_TYPE": config_value["type"],
        "ECS_CLUSTER_CAPACITY_PROVIDERS": config_value["capacity-providers"],
        "ECS_DEFAULT_CAPACITY_PROVIDER_STRATEGY": config_value["default-strategy"],
    }
