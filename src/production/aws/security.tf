
# ###################
# Generate key pair #
#####################
resource "tls_private_key" "oaken-key" {
  algorithm = "RSA"
  rsa_bits  = 1024
}

output "private_key_pem" {
  value = tls_private_key.oaken-key.private_key_pem
  sensitive = true
}

output "public_key_openssh" {
  value     = substr(tls_private_key.oaken-key.public_key_openssh, 0, 255)
  sensitive = true
}

resource "aws_key_pair" "oaken_pair" {
  key_name   = "oaken-pair"  # Name for your key pair
  public_key = tls_private_key.oaken-key.public_key_openssh
}

##################
# Access control #
##################

## Security groups
resource "aws_security_group" "default_sg" {
  name        = "default_sg"
  description = "Default security group"
}

resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "RDS security group"
}

## Seccurity rules

# Allow inbound SSH for EC2 instances
resource "aws_security_group_rule" "allow_ssh_in" {
  description       = "Allow SSH"
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["98.25.41.64/32"]
  security_group_id = aws_security_group.default_sg.id
}

# Kafka
resource "aws_security_group_rule" "kafka_rule" {
  description       = "kafka_rule"
  type              = "ingress"
  from_port         = 9092
  to_port           = 9092
  protocol          = "tcp"
  cidr_blocks       = ["98.25.41.64/32"]
  security_group_id = aws_security_group.default_sg.id
}

resource "aws_security_group_rule" "allow_from_instances" {
  description              = "Allow access to port 9092 from instances within the VPC"
  type                     = "ingress"
  from_port                = 9092
  to_port                  = 9092
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.default_sg.id  # Allow access from instances within the same security group
  security_group_id        = aws_security_group.default_sg.id
}

# Allow all outbound traffic
resource "aws_security_group_rule" "allow_all_out" {
  description       = "Allow outbound traffic"
  type              = "egress"
  from_port         = "0"
  to_port           = "0"
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.default_sg.id
}

# Allow inbound MySQL connections
resource "aws_security_group_rule" "allow_mysql_in" {
  description              = "Allow inbound MySQL connections"
  type                     = "ingress"
  from_port                = "3306"
  to_port                  = "3306"
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.default_sg.id
  security_group_id        = aws_security_group.rds_sg.id
}

