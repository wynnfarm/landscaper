# Variable definitions
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1" # Cheapest region
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro" # Cheapest instance
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "landscaper"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "" # Set this to your domain
}

variable "certificate_arn" {
  description = "SSL certificate ARN from AWS Certificate Manager"
  type        = string
  default     = "" # Set this after creating certificate
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}
