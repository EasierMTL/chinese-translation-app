provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "dev_access" {
  name        = "${var.name}_dev_access"
  description = "Allow SSH access and outbound access for package installations."
  ingress {
    from_port   = var.ssh_port
    to_port     = var.ssh_port
    protocol    = "tcp"
    cidr_blocks = var.allow_ssh_from_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "http" {
  name        = "${var.name}_http"
  description = "Allow HTTP in-bound traffic"
  ingress {
    from_port   = var.http_port
    to_port     = var.http_port
    protocol    = "tcp"
    cidr_blocks = var.allow_http_from_cidrs
  }
}

resource "aws_instance" "main_server" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.dev_access.id, aws_security_group.http.id]

  user_data = format(file("instance_scripts/deploy_normal.sh"), var.use_quantized)

  tags = {
    Name = var.name
  }
}

output "public_ip" {
  value       = aws_instance.main_server.public_ip
  description = "The public IP of the server"
}
output "instance_id" {
  value       = aws_instance.main_server.id
  description = "The ID of the server"
}
