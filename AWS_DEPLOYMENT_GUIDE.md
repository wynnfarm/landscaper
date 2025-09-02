# AWS Deployment Guide - Cheapest Option

## 💰 Cost Analysis

### **Option 1: Single EC2 Instance (Recommended)**

**Monthly Cost: ~$15-25**

| Component              | Cost/Month  | Notes           |
| ---------------------- | ----------- | --------------- |
| **t3.micro EC2**       | $8.47       | 1 vCPU, 1GB RAM |
| **EBS Storage (20GB)** | $1.80       | gp3 storage     |
| **Data Transfer**      | $0.09/GB    | First 1GB free  |
| **Route 53 Hosted Zone** | $0.50    | If using domain |
| **Domain Registration** | $1.00     | ~$12/year       |
| **Total**              | **~$10-15** | + taxes         |

### **Option 2: Serverless (More Scalable)**

**Monthly Cost: ~$10-20**

| Component           | Cost/Month  | Notes          |
| ------------------- | ----------- | -------------- |
| **Lambda**          | $0.20       | 1M requests    |
| **API Gateway**     | $3.50       | 1M requests    |
| **RDS db.t3.micro** | $12.41      | PostgreSQL     |
| **S3 + CloudFront** | $0.50       | Static hosting |
| **Total**           | **~$16-20** | + taxes        |

## 🚀 Quick Deployment Steps

### 1. Prerequisites

```bash
# Install Terraform
brew install terraform

# Install AWS CLI
brew install awscli

# Configure AWS credentials
aws configure
```

### 2. Domain Setup (Optional)

```bash
# Run the automated deployment script
./deploy_to_aws.sh

# Or manually set up domain:
# 1. Register domain in AWS Route 53 (~$12/year)
# 2. Create hosted zone
# 3. Create SSL certificate
```

### 3. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Deploy Application

```bash
# SSH into the instance
ssh -i ~/.ssh/id_rsa ubuntu@<EC2_PUBLIC_IP>

# Clone your repository
cd /opt/landscaper
git clone https://github.com/wynnfarm/landscaper.git .

# Create environment file
cp .env.template .env
# Edit .env with your secure credentials

# Deploy the application
./deploy.sh
```

## 🔧 Configuration

### Environment Variables

Create `/opt/landscaper/.env` on the EC2 instance:

```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password_here
DB_PASSWORD=your_secure_db_password_here

# Application Security
SECRET_KEY=your_secure_secret_key_here

# pgAdmin Configuration (for development)
PGADMIN_PASSWORD=your_secure_pgadmin_password_here
```

### Domain Setup (Optional)

1. Point your domain to the EC2 public IP
2. Update nginx configuration with your domain
3. Add SSL certificate with Let's Encrypt

## 📊 Monitoring & Maintenance

### View Logs

```bash
# Application logs
docker-compose logs -f

# System logs
sudo journalctl -u landscaper -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
```

### Backup Database

```bash
# Create backup
docker exec landscaper-database pg_dump -U landscaper_user landscaper > backup.sql

# Restore backup
docker exec -i landscaper-database psql -U landscaper_user landscaper < backup.sql
```

### Update Application

```bash
# SSH into instance and run
cd /opt/landscaper
git pull origin main
./deploy.sh
```

## 🛡️ Security Considerations

1. **Change default passwords** in `.env` file
2. **Restrict SSH access** to your IP only
3. **Enable AWS CloudWatch** for monitoring
4. **Set up automated backups** for database
5. **Use AWS Secrets Manager** for production

## 💡 Cost Optimization Tips

1. **Use Spot Instances** for non-critical workloads (save 60-90%)
2. **Reserved Instances** for predictable workloads (save 30-60%)
3. **Monitor usage** with AWS Cost Explorer
4. **Set up billing alerts** to avoid surprises
5. **Use AWS Free Tier** for first 12 months

## 🔄 Alternative: GitHub Actions Deployment

For automated deployments, create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.4
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/landscaper
            git pull origin main
            ./deploy.sh
```
