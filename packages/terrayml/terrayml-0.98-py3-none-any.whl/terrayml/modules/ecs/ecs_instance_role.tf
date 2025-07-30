resource "aws_iam_role" "ecs_instance_role" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_ec2_policy_attach" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  role       = aws_iam_role.ecs_instance_role[each.value.name].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}
resource "aws_iam_policy" "ecs_ec2_set_policy" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-policy"
  policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = each.value.auto_scaling_group.launch_template.allowed_actions,
          Resource = each.value.auto_scaling_group.launch_template.allowed_resources,
        }
      ]
    })
}
resource "aws_iam_role_policy_attachment" "ecs_ec2_set_policy_attach" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  role       = aws_iam_role.ecs_instance_role[each.value.name].name
  policy_arn = aws_iam_policy.ecs_ec2_set_policy[each.value.name].arn
}
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  for_each      = { for key, value in var.capacity_provider_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-profile"
  role = aws_iam_role.ecs_instance_role[each.value.name].name
}