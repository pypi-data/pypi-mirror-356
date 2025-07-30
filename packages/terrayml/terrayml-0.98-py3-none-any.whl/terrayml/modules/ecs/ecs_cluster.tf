resource "aws_ecs_cluster" "this" {
  for_each      = { for key, value in var.ecs_cluster_list : value.name => value }

  name = "${var.common.project_name}-${var.common.environment}-${each.value.name}-cluster"
  tags = var.common.default_tags
}
resource "aws_ecs_cluster_capacity_providers" "this" {
  for_each      = { for key, value in var.ecs_cluster_list : value.name => value }

  cluster_name         = aws_ecs_cluster.this[each.value.name].name
  capacity_providers   = [ for provider in each.value.capacity_providers: aws_ecs_capacity_provider.ecs_capacity_provider[provider].name ]

  default_capacity_provider_strategy {
    base              = each.value.default_capacity_provider_strategy.base
    weight            = each.value.default_capacity_provider_strategy.weight
    capacity_provider = aws_ecs_capacity_provider.ecs_capacity_provider[each.value.default_capacity_provider_strategy.provider].name
  }
}