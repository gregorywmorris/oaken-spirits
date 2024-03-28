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

# Allow inbound SSH for EC2 instances
resource "aws_security_group_rule" "allow_ssh_in" {
  description       = "Allow SSH"
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["98.25.41.64/32"]
  security_group_id = aws_security_group.default.id
}

# Allow all outbound traffic
resource "aws_security_group_rule" "allow_all_out" {
  description       = "Allow outbound traffic"
  type              = "egress"
  from_port         = "0"
  to_port           = "0"
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.default.id
}

# Allow inbound MySQL connections
resource "aws_security_group_rule" "allow_mysql_in" {
  description              = "Allow inbound MySQL connections"
  type                     = "ingress"
  from_port                = "3306"
  to_port                  = "3306"
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.default.id
  security_group_id        = aws_security_group.rds_sg.id
}


# EC2 instances

resource "aws_instance" "database" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
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
  }
}

resource "aws_instance" "kafka" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
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
  }
}


resource "aws_instance" "api" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
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
  }

  provisioner "file" {
    source      = "app/mysql-api/"
    destination = "/usr/lib/oaken"
  }
}

resource "aws_instance" "shipping" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
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
  }

    provisioner "file" {
    source      = "app/shipping/"
    destination = "/usr/lib/oaken"
  }
}

resource "aws_instance" "accounting" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"
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
  }

    provisioner "file" {
    source      = "app/accounting/"
    destination = "/usr/lib/oaken"
  }
}