# Basic terraform config
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Load and validate YAML
locals {
  config = merge(
    yamldecode(file("${path.module}/config.yaml"), {
      "aws_region" : "eu-west-2",
      "project_name" : "project"
    })
  )
  availability_zones = [
    "${local.config["aws_region"]}a",
    "${local.config["aws_region"]}b",
    "${local.config["aws_region"]}c",
  ]
}

# Configure the AWS Provider
provider "aws" {
  region = local.config["aws_region"]
}
