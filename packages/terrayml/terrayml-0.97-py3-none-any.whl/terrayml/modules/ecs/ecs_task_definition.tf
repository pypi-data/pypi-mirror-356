resource "aws_ecs_task_definition" "this" {
  for_each      = { for key, value in var.task_definition_list : value.name => value }

  family                   = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  requires_compatibilities = each.value.required_compatibilities
  execution_role_arn       = aws_iam_role.ecs_task_execution_role[each.value.name].arn
  network_mode             = each.value.network_mode
  cpu                      = tostring(each.value.cpu)
  memory                   = tostring(each.value.memory)
  
  runtime_platform {
    operating_system_family = each.value.runtime_platform.system_family
    cpu_architecture        = each.value.runtime_platform.cpu_architecture
  }

  container_definitions = jsonencode([
    for container_definition in each.value.container_definitions : {
      name      = "${var.common.project_code}-${var.common.environment}-${container_definition.name}"
      image     = container_definition.image
      cpu       = container_definition.cpu
      memory    = container_definition.memory
      essential = container_definition.essential == "TRUE" ? true : false
      environment = container_definition.environment
      portMappings = container_definition.port_mappings
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_task_log_group[each.value.name].name
          "awslogs-region"        = var.common.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
  tags = var.common.default_tags
}

resource "aws_cloudwatch_log_group" "ecs_task_log_group" {
  for_each      = { for key, value in var.task_definition_list : value.name => value }
  name = "/ecs/${var.common.project_code}-${var.common.environment}-${each.value.name}-logs"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  for_each = { for key, value in var.task_definition_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ECSTaskExRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "ecs_task_execution_role_policy" {
  for_each = { for key, value in var.task_definition_list : value.name => value }

  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ECSTaskExPolicy"
  policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = each.value.task_execution_role.allowed_actions,
          Resource = each.value.task_execution_role.allowed_resources,
        }
      ]
    })

}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attach" {
  for_each = { for key, value in var.task_definition_list : value.name => value }

  role       = aws_iam_role.ecs_task_execution_role[each.value.name].name
  policy_arn = aws_iam_policy.ecs_task_execution_role_policy[each.value.name].arn
}