# Oaken Spirits
/*
EC2 Instances
1. Database
  - MySQL
  - with EBS
1. Kafka
1. MySQL API
1. Shipping
1. Accounting
}
*/

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region                   = "us-east-1"
  profile                  = "eb-cli"
}

variable "environment" {
  type = string
  default = test
}

data "aws_ami" "ubuntu" {
  most_recent   = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "kafka" {
  ami           = data.aws_ami.ubuntu.id
  # instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
  instance_type = "t3.micro"

  tags = {
    Name = "oaken"
  }
}

resource "aws_instance" "database" {
  ami           = data.aws_ami.ubuntu.id
  # instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
  instance_type = "t3.micro"

  tags = {
    Name = "oaken"
  }
}

resource "aws_instance" "api" {
  ami           = data.aws_ami.ubuntu.id
  # instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
  instance_type = "t2.micro"

  tags = {
    Name = "oaken"
  }

  provisioner "file" {
    source      = "app/mysql-api/"
    destination = "/usr/lib/oaken"
  }
}

resource "aws_instance" "shipping" {
  ami           = data.aws_ami.ubuntu.id
  # instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
  instance_type = "t2.micro"

  tags = {
    Name = "oaken"
  }

    provisioner "file" {
    source      = "app/shipping/"
    destination = "/usr/lib/oaken"
  }
}

resource "aws_instance" "accounting" {
  ami           = data.aws_ami.ubuntu.id
  # instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
  instance_type = "t2.micro"

  tags = {
    Name = "oaken"
  }

    provisioner "file" {
    source      = "app/accounting/"
    destination = "/usr/lib/oaken"
  }
}