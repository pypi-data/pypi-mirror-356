{
    "name": "${ECS_CAPACITY_PROVIDER_NAME}",
    "auto_scaling_group": "${ECS_CAPACITY_PROVIDER_SCALING_GROUP}",
}


def generate_mappings(config_key, config_value, other_reference_mappings):
    auto_scaling_group_yml = config_value["auto-scaling-group"]
    auto_scaling_group = {
        "min_size": int(auto_scaling_group_yml["min-size"]),
        "max_size": int(auto_scaling_group_yml["max-size"]),
        "desired_capacity": auto_scaling_group_yml["desired-capacity"],
        "private_vpc_subnets": auto_scaling_group_yml["private-vpc-subnets"],
        "launch_template": {
            "instance_type": auto_scaling_group_yml["launch-template"]["instance-type"],
            "allowed_actions": auto_scaling_group_yml["launch-template"][
                "allowed-actions"
            ],
            "allowed_resources": auto_scaling_group_yml["launch-template"][
                "allowed-resources"
            ],
            "ebs": {
                "volume_size": int(
                    auto_scaling_group_yml["launch-template"]["ebs"]["volume-size"]
                ),
                "volume_type": auto_scaling_group_yml["launch-template"]["ebs"][
                    "volume-type"
                ],
            },
            "security_groups": auto_scaling_group_yml["launch-template"][
                "security-groups"
            ],
            "ecs_cluster": auto_scaling_group_yml["launch-template"]["ecs-cluster"],
        },
        "managed_scaling": {
            "target_capacity": auto_scaling_group_yml["managed-scaling"][
                "target-capacity"
            ],
            "minimum_scaling_step_size": auto_scaling_group_yml["managed-scaling"][
                "minimum-scaling-step-size"
            ],
            "maximum_scaling_step_size": auto_scaling_group_yml["managed-scaling"][
                "maximum-scaling-step-size"
            ],
            "instance_warmup_period": auto_scaling_group_yml["managed-scaling"][
                "instance-warmup-period"
            ],
        },
    }

    return {
        "ECS_CAPACITY_PROVIDER_NAME": config_key,
        "ECS_CAPACITY_PROVIDER_SCALING_GROUP": auto_scaling_group,
    }
