# Data source: query the list of availability zones
data "aws_availability_zones" "all" {}


# Create an EC2 instance
resource "aws_instance" "example" {
  ami                   = "ami-785db401"
  instance_type         = "t2.micro"
  vpc_security_group_ids= [aws_security_group.instance.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p "8080" &  # Adjusted to use port 8080
              EOF

  tags = {
    Name = "terraform-example"
  }
}
