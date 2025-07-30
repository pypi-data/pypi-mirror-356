def generate_mappings(config_key, config_value, other_reference_mappings):
    target_groups = []
    listeners = []

    for target_group in config_value["target-groups"]:
        target_groups.append(
            {
                "name": target_group["name"],
                "port": target_group["port"],
                "protocol": target_group["protocol"],
                "vpc_id": target_group["vpc-id"],
                "target_type": target_group["target-type"],
                "health_check": {
                    "path": target_group["health-check"]["path"],
                    "port": int(target_group["health-check"]["port"]),
                    "protocol": target_group["health-check"]["protocol"],
                    "matcher": target_group["health-check"]["matcher"],
                },
            }
        )

    for listener in config_value["listeners"]:
        listener_rules = []
        for rule in listener.get("rules", []):
            listener_rules.append(
                {
                    "target_group": rule["target-group"],
                    "priority": rule["priority"],
                    "path_patterns": rule["path-patterns"],
                }
            )

        listeners.append(
            {
                "port": listener["port"],
                "protocol": listener["protocol"],
                "default_action": {
                    "type": listener["default-action"]["type"],
                    "target_group": listener["default-action"]["target-group"],
                },
                "rules": listener_rules,
            }
        )

    return {
        "ECS_ALB_NAME": config_key,
        "ECS_ALB_PUBLIC_SUBNETS": config_value["public-subnets"],
        "ECS_ALB_SECURITY_GROUPS": config_value["security-groups"],
        "ECS_ALB_TARGET_GROUPS": target_groups,
        "ECS_ALB_LISTENERS": listeners,
    }
