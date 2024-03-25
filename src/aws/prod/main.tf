# Oaken Spirits
/*

*/

data "aws_ami" "ubuntu" {
  most_recent = true

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

resource "aws_instance" "server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "development" ? "t2.micro" : "t2.small"

  tags = {
    Name = "HelloWorld"
  }
}