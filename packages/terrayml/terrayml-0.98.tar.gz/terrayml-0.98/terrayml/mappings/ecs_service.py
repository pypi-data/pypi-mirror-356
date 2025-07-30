def generate_mappings(config_key, config_value, other_reference_mappings):
    load_balancer = {
        "alb_name": config_value["load-balancer"]["alb-name"],
        "target_group": config_value["load-balancer"]["target-group"],
        "container_name": config_value["load-balancer"]["container-name"],
        "container_port": int(config_value["load-balancer"]["container-port"]),
    }

    return {
        "ECS_SERVICE_NAME": config_key,
        "ECS_SERVICE_CLUSTER": config_value["cluster"],
        "ECS_SERVICE_TASK_DEFINITION": config_value["task-definition"],
        "ECS_SERVICE_DESIRED_COUNT": int(config_value["desired-count"]),
        "ECS_SERVICE_FORCE_DELETE": str(config_value["force-delete"]).upper(),
        "ECS_SERVICE_FORCE_NEW_DEPLOYMENT": str(
            config_value["force-new-deployment"]
        ).upper(),
        "ECS_SERVICE_PRIVATE_VPC_SUBNETS": config_value["private-vpc-subnets"],
        "ECS_SERVICE_SECURITY_GROUPS": config_value["security-groups"],
        "ECS_SERVICE_LOAD_BALANCER": load_balancer,
        "ECS_SERVICE_CAPACITY_PROVIDER_STRATEGY": config_value[
            "capacity-provider-strategy"
        ],
    }
