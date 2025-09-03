# Terraform Infrastructure for Landscaper App

This directory contains the Terraform configuration for deploying the Landscaper application to AWS.

## 📁 File Structure

```
terraform/
├── main.tf                    # Main infrastructure configuration
├── variables.tf               # Variable definitions
├── outputs.tf                 # Output values
├── user_data.sh              # EC2 instance setup script
├── terraform.tfvars           # Your specific values (create this)
└── terraform.tfvars.example  # Template for terraform.tfvars
```

## 🚀 Quick Start

### 1. Create your variables file

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 2. Deploy infrastructure

```bash
# From project root
./terraform-manager.sh deploy

# Or manually
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Destroy infrastructure

```bash
# From project root
./terraform-manager.sh destroy

# Or manually
cd terraform
terraform destroy
```

## 🔧 Configuration

### Variables (terraform.tfvars)

```hcl
# Required
aws_region = "us-east-1"
instance_type = "t3.micro"
app_name = "landscaper"

# Optional (for domain setup)
domain_name = "your-domain.com"
certificate_arn = "arn:aws:acm:..."

# Optional (advanced)
environment = "dev"
vpc_cidr = "10.0.0.0/16"
subnet_cidr = "10.0.1.0/24"
```

### Outputs

- `public_ip` - EC2 instance public IP
- `app_url` - Application URL
- `ssh_command` - SSH command to connect
- `deployment_info` - Summary of deployment

## 🛡️ Security

- **SSH Key**: Uses `~/.ssh/id_rsa.pub`
- **Security Groups**: Minimal required ports (22, 80, 443, 5000)
- **VPC**: Isolated network with internet gateway
- **SSL**: Automatic Let's Encrypt certificates

## 💰 Cost Estimation

**Monthly costs (estimated):**

- EC2 t3.micro: ~$8.47
- EBS Storage (20GB): ~$1.80
- Data Transfer: ~$0.09/GB
- Route 53 Hosted Zone: ~$0.50 (if using domain)
- **Total: ~$10-15/month**

## 🔄 State Management

Terraform state is stored locally in `terraform/.terraform/terraform.tfstate`.

**⚠️ Important:** Never commit the `.tfstate` file to version control!

## 📋 Commands Reference

```bash
# Initialize
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy everything
terraform destroy

# Show current state
terraform show

# List outputs
terraform output

# Validate configuration
terraform validate
```

## 🆘 Troubleshooting

### Common Issues:

1. **AWS credentials not configured**: Run `aws configure`
2. **SSH key not found**: Run `ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa`
3. **Permission denied**: Check file permissions on scripts
4. **Domain not resolving**: Wait 5-10 minutes for DNS propagation

### Useful Commands:

```bash
# Check AWS credentials
aws sts get-caller-identity

# Test SSH connection
ssh -i ~/.ssh/id_rsa ubuntu@<PUBLIC_IP>

# View application logs
docker-compose logs -f
```
