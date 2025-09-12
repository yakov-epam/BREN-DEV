# Main security group
resource "aws_security_group" "project_sg" {
  vpc_id                 = aws_vpc.project_vpc.id
  name                   = "${local.config["project_name"]}-main-sg"
  revoke_rules_on_delete = true

  tags = {
    Name = "${local.config["project_name"]}-main-sg"
  }
}

resource "aws_vpc_security_group_egress_rule" "project_sg_egress" {
  security_group_id = aws_security_group.project_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_vpc_security_group_ingress_rule" "project_sg_ingress_https_ipv4" {
  security_group_id = aws_security_group.project_sg.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 80
  cidr_ipv4         = aws_vpc.project_vpc.cidr_block
}

resource "aws_vpc_security_group_ingress_rule" "project_sg_ingress_https_ipv6" {
  security_group_id = aws_security_group.project_sg.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 80
  cidr_ipv6         = aws_vpc.project_vpc.ipv6_cidr_block
}

resource "aws_vpc_security_group_ingress_rule" "project_sg_ingress_http_ipv4" {
  security_group_id = aws_security_group.project_sg.id
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_ipv4         = aws_vpc.project_vpc.cidr_block
}

resource "aws_vpc_security_group_ingress_rule" "project_sg_ingress_http_ipv6" {
  security_group_id = aws_security_group.project_sg.id
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_ipv6         = aws_vpc.project_vpc.ipv6_cidr_block
}

# Dev ingress security group - to allow DB connections from exact IPs later, manually
resource "aws_security_group" "project_dev_sg" {
  vpc_id = aws_vpc.project_vpc.id
  name   = "${local.config["project_name"]}-dev-sg"

  tags = {
    Name = "${local.config["project_name"]}-dev-sg"
  }
}

# Load balancers
resource "aws_alb" "project_alb" {
  count              = length(local.config["services"])
  name               = "${local.config["services"][count.index]["name"]}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups = [
    aws_security_group.project_sg.id,
    aws_security_group.project_dev_sg.id
  ]
  subnets                    = [for subnet in aws_subnet.project_public_subnets : subnet.id]
  enable_deletion_protection = true
}

resource "aws_lb_target_group" "project_alb_tg_http" {
  count    = length(local.config["services"])
  name     = "${local.config["services"][count.index]["name"]}-alb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.project_vpc.id

  health_check {
    path                = local.config["services"][count.index]["healthcheck_path"]
    protocol            = "HTTP"
    matcher             = "200"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 10
    interval            = 30
  }
}

resource "aws_lb_listener" "project_alb_listener" {
  load_balancer_arn = aws_alb.project_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.project_alb_tg_http.arn
  }
}
