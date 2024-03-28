# Oaken Spirits
/*
Variable set in variables.tf

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


# EC2 instances

resource "aws_instance" "database" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = var.environment == "development" ? "t2.micro" : "t2.small"
  vpc_security_group_ids  = [
                              aws_security_group.default_sg.id,
                              aws_security_group.rds_sg.id
                            ]
  key_name               = "oaken-pair"
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y mysql-server

              # Start the MySQL service
              systemctl start mysql

              # Enable MySQL service to start on boot
              systemctl enable mysql

              # Execute MySQL commands to create user and grant privileges
              mysql <<EOF_MYSQL
              CREATE DATABASE IF NOT EXISTS oaken;
              CREATE USER 'mysql'@'localhost' IDENTIFIED BY 'mysql';
              GRANT ALL PRIVILEGES ON *.* TO 'mysql'@'localhost';
              FLUSH PRIVILEGES;
              EOF_MYSQL

              # Clean up apt cache
              apt-get clean
              EOF

  tags = {
    Name = "oaken-database"
    Environment = var.environment
  }
}

resource "aws_instance" "kafka" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = var.environment == "development" ? "t2.micro" : "t2.small"
  vpc_security_group_ids  = [aws_security_group.default_sg.id]
  key_name                = "oaken-pair"
  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install net-tools
              apt-get install -y default-jre
              apt-get install -y zookeeperd

              # Download and extract Kafka binary package
              wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
              tar -xzf kafka_2.13-3.7.0.tgz

              # Clean up
              apt-get clean
              EOF

  tags = {
    Name = "oaken-kafka"
    Environment = var.environment
  }
}


resource "aws_instance" "api" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = var.environment == "development" ? "t2.micro" : "t2.small"
  vpc_security_group_ids  = [aws_security_group.default_sg.id]
  key_name                = "oaken-pair"
  user_data = <<-EOF
              #!/bin/bash
                apt-get update
                apt-get install -y pkg-config
                pip install kafka-python mysql-connector-python
                mkdir -p /app
                apt-get clean
              EOF
  tags = {
    Name = "oaken-mysql-api"
    Environment = var.environment
  }
}

resource "aws_instance" "shipping" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = var.environment == "development" ? "t2.micro" : "t2.small"
  vpc_security_group_ids  = [aws_security_group.default_sg.id]
  key_name                = "oaken-pair"
  user_data = <<-EOF
              #!/bin/bash
                apt-get update
                apt-get install -y pkg-config
                pip install kafka-python mysql-connector-python
                mkdir -p /app
                apt-get clean
              EOF
  tags = {
    Name = "oaken-shipping"
    Environment = var.environment
  }
}

resource "aws_instance" "accounting" {
  ami                     = data.aws_ami.ubuntu.id
  instance_type           = var.environment == "development" ? "t2.micro" : "t2.small"
  vpc_security_group_ids  = [aws_security_group.default_sg.id]
  key_name                = "oaken-pair"
  user_data = <<-EOF
              #!/bin/bash
                apt-get update
                apt-get install -y pkg-config
                pip install kafka-python mysql-connector-python
                mkdir -p /app
                apt-get clean
              EOF
  tags = {
    Name = "oaken-accounting"
    Environment = var.environment
  }
}