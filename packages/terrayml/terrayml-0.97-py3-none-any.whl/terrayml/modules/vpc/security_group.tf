locals {
  security_groups = flatten([
      for vpc_key, vpc in var.vpc_list: [
        for security_group_key, security_group in vpc.security_groups: {
          vpc_key = vpc_key
          vpc_name = vpc.vpc_name
          vpc_id = aws_vpc.this[vpc.vpc_name].id

          security_group_key = security_group_key
          security_group_name = security_group.security_group_name
        }
      ]
    ])

}

resource "aws_security_group" "this" {
    for_each = tomap({
        for security_group in local.security_groups: "${security_group.vpc_name}.${security_group.security_group_name}" => security_group
    })
    
    name   = "${each.value.security_group_name}-${var.common.environment}"
    vpc_id = each.value.vpc_id
    tags = merge(var.common.default_tags, {
        Name = "${each.value.security_group_name}-${var.common.environment}"
    })
}

resource "aws_vpc_security_group_egress_rule" "this" {
  for_each = tomap({
        for security_group in local.security_groups: "${security_group.vpc_name}.${security_group.security_group_name}" => security_group
    })
  security_group_id = aws_security_group.this["${each.value.vpc_name}.${each.value.security_group_name}"].id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}