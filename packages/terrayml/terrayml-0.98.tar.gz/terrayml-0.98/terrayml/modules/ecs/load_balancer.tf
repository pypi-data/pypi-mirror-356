
locals {
  alb_target_groups = flatten([
    for load_balancer_key, load_balancer in var.application_load_balancer_list: [
      for target_group_key, target_group in load_balancer.target_groups: {
        load_balancer_key = load_balancer_key
        load_balancer_name = load_balancer.name

        target_group_key = target_group_key
        name = target_group.name
        port = target_group.port
        protocol = target_group.protocol
        vpc_id = target_group.vpc_id
        target_type = target_group.target_type
        health_check = target_group.health_check
      }
    ]
  ])
  alb_listeners = flatten([
    for load_balancer_key, load_balancer in var.application_load_balancer_list: [
      for listener_key, listener in load_balancer.listeners: {
        load_balancer_key = load_balancer_key
        load_balancer_name = load_balancer.name

        listener_key = listener_key
        port = listener.port
        protocol = listener.protocol
        default_action = listener.default_action
        rules = listener.rules
      }
    ]
  ])
  alb_listener_rules = flatten([
    for alb in var.application_load_balancer_list : [
      for listener in alb.listeners : [
        for rule in listener.rules : {
          load_balancer_name = alb.name
          listener_port      = listener.port
          target_group_name  = rule.target_group
          priority           = rule.priority
          path_patterns      = rule.path_patterns
        }
      ]
    ]
  ])

}


resource "aws_alb" "ecs_alb" {
  for_each      = { for key, value in var.application_load_balancer_list : value.name => value }
  name                       = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ecs-alb"
  load_balancer_type         = "application"
  subnets                    = each.value.public_subnets
  security_groups            = each.value.security_groups
  enable_deletion_protection = false
  internal                   = false
  enable_http2               = true # Enable HTTP/2 for better performance

  tags = var.common.default_tags
}

resource "aws_alb_target_group" "ecs_container_target_group" {
  for_each = tomap({
    for target_group in local.alb_target_groups: "${target_group.load_balancer_name}.${target_group.name}" => target_group
  })
  name        = "${var.common.project_code}-${var.common.environment}-${each.value.name}-tg"
  port        = each.value.port
  protocol    = each.value.protocol
  vpc_id      = each.value.vpc_id
  target_type = each.value.target_type

  health_check {
    path     = each.value.health_check.path
    port     = each.value.health_check.port
    protocol = each.value.health_check.protocol
    matcher  = each.value.health_check.matcher
  }
}

resource "aws_alb_listener" "this" {
  for_each = tomap({
    for listener in local.alb_listeners: "${listener.load_balancer_name}.${tostring(listener.port)}" => listener
  })

  load_balancer_arn = aws_alb.ecs_alb[each.value.load_balancer_name].arn
  port              = each.value.port
  protocol          = each.value.protocol

  default_action {
    type             = each.value.default_action.type
    target_group_arn = aws_alb_target_group.ecs_container_target_group["${each.value.load_balancer_name}.${each.value.default_action.target_group}"].arn
  }
}

resource "aws_lb_listener_rule" "this" {
  for_each = tomap({
    for listener_rule in local.alb_listener_rules: "${listener_rule.load_balancer_name}.${tostring(listener_rule.priority)}" => listener_rule
  })
  listener_arn = aws_alb_listener.this["${each.value.load_balancer_name}.${tostring(each.value.listener_port)}"].arn
  priority     = each.value.priority

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.ecs_container_target_group["${each.value.load_balancer_name}.${each.value.target_group_name}"].arn
  }

  condition {
    path_pattern {
      values = each.value.path_patterns
    }
  }
}