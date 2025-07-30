resource "aws_ecs_service" "this" {
  for_each      = { for key, value in var.services_list : value.name => value }

  name            = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  cluster         = aws_ecs_cluster.this[each.value.cluster].id
  task_definition = aws_ecs_task_definition.this[each.value.task_definition].arn
  desired_count   = each.value.desired_count
  force_delete    = each.value.force_delete == "TRUE" ? true : false
  force_new_deployment = each.value.force_new_deployment == "TRUE" ? true : false

  network_configuration {
    subnets         = each.value.private_vpc_subnets
    security_groups = each.value.security_groups
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.ecs_container_target_group["${each.value.load_balancer.alb_name}.${each.value.load_balancer.target_group}"].arn
    container_name   = "${var.common.project_code}-${var.common.environment}-${each.value.load_balancer.container_name}"
    container_port   = each.value.load_balancer.container_port
  }
  capacity_provider_strategy {
    capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider[each.value.capacity_provider_strategy.provider].name
    weight = each.value.capacity_provider_strategy.weight
  }

  tags = var.common.default_tags
}