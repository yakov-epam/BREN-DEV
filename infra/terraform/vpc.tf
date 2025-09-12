# Create a VPC
resource "aws_vpc" "project_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "${local.config["project_name"]}-vpc"
  }
}

# Create VPC subnets
variable "public_subnets" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

resource "aws_subnet" "project_public_subnets" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.project_vpc.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = local.availability_zones[count.index]
  tags = {
    Name = "${local.config["project_name"]}-public-subnet-${count.index + 1}"
  }
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
}

resource "aws_subnet" "project_private_subnets" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.project_vpc.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = local.availability_zones[count.index]
  tags = {
    Name = "${local.config["project_name"]}-private-subnet-${count.index + 1}"
  }
}

# Create internet gateway
resource "aws_internet_gateway" "project_gateway" {
  vpc_id = aws_vpc.project_vpc.id

  tags = {
    Name = "${local.config["project_name"]}-igw"
  }
}

# Create route table / expose public subnets
resource "aws_route_table" "project_route_table" {
  vpc_id = aws_vpc.project_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.project_gateway
  }

  tags = {
    Name = "${local.config["project_name"]}-rt"
  }
}

resource "aws_route_table_association" "project_route_table_association" {
  count          = length(var.public_subnets)
  subnet_id      = aws_subnet.project_public_subnets[count.index].id
  route_table_id = aws_route_table.project_route_table.id
}
