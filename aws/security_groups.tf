
# Create a Security Group for an EC2 instance
resource "aws_security_group" "instance" {
  name = "terraform-example-instance"

  ingress {
    from_port    = 8080  # Instance will listen on 8080 for ELB
    to_port      = 8080
    protocol     = "tcp"
    cidr_blocks  = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create a Security Group for an ELB
resource "aws_security_group" "elb" {
  name = "terraform-example-elb"

  ingress {
    from_port    = 80  # ELB listens on 80 from the internet
    to_port      = 80
    protocol     = "tcp"
    cidr_blocks  = ["0.0.0.0/0"]
  }

  egress {
    from_port    = 0
    to_port      = 0
    protocol     = "-1"
    cidr_blocks  = ["0.0.0.0/0"]
  }
}