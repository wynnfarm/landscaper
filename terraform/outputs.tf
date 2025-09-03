# Output values
output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = var.domain_name != "" ? aws_eip.app[0].public_ip : aws_instance.app.public_ip
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app.id
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${var.domain_name != "" ? aws_eip.app[0].public_ip : aws_instance.app.public_ip}"
}

output "app_url" {
  description = "Application URL"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "http://${aws_instance.app.public_ip}"
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the subnet"
  value       = aws_subnet.main.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.app.id
}

output "deployment_info" {
  description = "Deployment information"
  value = {
    environment            = var.environment
    region                 = var.aws_region
    instance_type          = var.instance_type
    domain_name            = var.domain_name != "" ? var.domain_name : "IP only"
    estimated_monthly_cost = "$10-15"
  }
}
