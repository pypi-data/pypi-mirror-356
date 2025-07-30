variable "common" {
  description = "common variables"
}

variable "capacity_provider_list" {
    type = list(object({
        name = string
        auto_scaling_group = object({
            min_size = number
            max_size = number
            desired_capacity = number
            private_vpc_subnets = list(string)
            launch_template = object({
                instance_type =  string
                allowed_actions = list(string)
                allowed_resources = list(string)
                ebs = object({
                    volume_size = number
                    volume_type = string
                })
                security_groups = list(string)
                ecs_cluster = string
            })
            managed_scaling = object({
              target_capacity = number
              minimum_scaling_step_size = number
              maximum_scaling_step_size = number
              instance_warmup_period = number
            })
        })
    }))
    description = "ECS Capacity Provider list"
}

variable "ecs_cluster_list" {
    type = list(object({
        name = string
        type = string
        capacity_providers = list(string)
        default_capacity_provider_strategy = object({
            base = number
            weight = number
            provider = string
        })
    }))
    description = "ECS cluster list"
}
variable "task_definition_list" {
    type = list(object({
        name = string
        required_compatibilities = list(string)
        network_mode = string
        cpu = number
        memory = number
        runtime_platform = object({
            system_family = string
            cpu_architecture = string
        })
        task_execution_role = object({
          allowed_actions = list(string)
          allowed_resources = list(string)
        })
        container_definitions = list(object({
            name = string
            image = string
            cpu = number
            memory = number
            essential = string
            port_mappings = list(object({
                containerPort = number
                hostPort = number
            }))
            environment = list(object({
                name = string
                value = string
            }))
        }))
    }))
    description = "ECS Task Definition list"
}

variable "application_load_balancer_list" {
    type = list(object({
        name = string
        public_subnets = list(string)
        security_groups = list(string)
        target_groups = list(object({
            name = string
            port = number
            protocol = string
            vpc_id = string
            target_type = string
            health_check = object({
              path = string
              port = number
              protocol = string
              matcher = string
            })
        }))
        listeners = list(object({
            port = number
            protocol = string
            default_action = object({
              type = string
              target_group = string
            })
            rules = list(object({
                target_group = string
                priority = number
                path_patterns = list(string)
            }))
        }))
    }))
    description = "ECS Load Balancer list"
}
variable "services_list" {
    type = list(object({
        name = string
        cluster = string
        task_definition = string
        desired_count = number
        force_delete = string
        force_new_deployment = string
        private_vpc_subnets = list(string)
        security_groups = list(string)
        load_balancer = object({
          alb_name = string
          target_group = string
          container_name = string
          container_port = number
        })
        capacity_provider_strategy = object({
          provider = string
          weight = number
        })
    }))
    description = "ECS Services list"
}