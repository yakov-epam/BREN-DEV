resource "aws_ecr_repository" "project_ecr" {
  name                 = "${local.config["project_name"]}-repository"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "project_ecs" {
  name = "${local.config["project_name"]}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "project_task_definition" {
  count  = length(local.config["services"])
  family = "service"
  container_definitions = jsonencode([
    {
      name      = local.config["services"][count.index]["name"]
      image     = "${aws_ecr_repository.project_ecr.repository_url}:${local.config["services"][count.index]["ecr_image_tag"]}"
      cpu       = local.config["services"][count.index]["cpu"]
      memory    = local.config["services"][count.index]["ram"]
      essential = local.config["services"][count.index]["essential"]
      portMappings = [
        {
          containerPort = local.config["services"][count.index]["container_port"]
          hostPort      = local.config["services"][count.index]["host_port"]
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "project_ecs_service" {
  count           = length(local.config["services"])
  name            = local.config["services"][count.index]["name"]
  cluster         = aws_ecs_cluster.project_ecs.id
  task_definition = aws_ecs_task_definition.project_task_definition[count.index].arn
  desired_count   = local.config["services"][count.index]["desired_count"]
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [for subnet in aws_subnet.project_private_subnets : subnet.id]
    security_groups = [
      aws_security_group.project_sg.id,
      aws_security_group.project_dev_sg.id
    ]
  }
}
