resource "aws_ecs_capacity_provider" "ecs_capacity_provider" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-cp"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.ecs_asg[each.value.name].arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      status                    = "ENABLED"
      target_capacity           = each.value.auto_scaling_group.managed_scaling.target_capacity
      minimum_scaling_step_size = each.value.auto_scaling_group.managed_scaling.minimum_scaling_step_size
      maximum_scaling_step_size = each.value.auto_scaling_group.managed_scaling.maximum_scaling_step_size
      instance_warmup_period    = each.value.auto_scaling_group.managed_scaling.instance_warmup_period
    }
  }

}


resource "aws_autoscaling_group" "ecs_asg" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name                 = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ecs-asg"
  max_size             = each.value.auto_scaling_group.max_size
  min_size             = each.value.auto_scaling_group.min_size
  desired_capacity     = each.value.auto_scaling_group.desired_capacity
  vpc_zone_identifier  = each.value.auto_scaling_group.private_vpc_subnets
  force_delete         = true

  launch_template {
    id      = aws_launch_template.ecs_launch_template[each.value.name].id
    version = "$Latest"
  }
  tag {
    key                 = "Name"
    value               = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ecs-asg"
    propagate_at_launch = true
  }

}

resource "aws_launch_template" "ecs_launch_template" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name          = "${var.common.project_code}-${var.common.environment}-${each.value.name}-ecs-ec2-lt"
  image_id      = data.aws_ami.amazon_linux2.id
  instance_type = each.value.auto_scaling_group.launch_template.instance_type

  instance_initiated_shutdown_behavior = "terminate"

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      delete_on_termination = true
      volume_size           = each.value.auto_scaling_group.launch_template.ebs.volume_size
      volume_type           = each.value.auto_scaling_group.launch_template.ebs.volume_type
      encrypted             = true
    }
  }
  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_instance_profile[each.value.name].name
  }

  lifecycle {
    create_before_destroy = true
  }

  user_data = base64encode(<<-EOF
      #!/bin/bash
      echo ECS_CLUSTER=${aws_ecs_cluster.this[each.value.auto_scaling_group.launch_template.ecs_cluster].name} >> /etc/ecs/ecs.config;
      EOF
  )

  vpc_security_group_ids = each.value.auto_scaling_group.launch_template.security_groups

  tags = var.common.default_tags
}
