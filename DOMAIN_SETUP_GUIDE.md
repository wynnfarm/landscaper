# Domain Configuration Guide

## 🌐 Domain Setup Options

### **Option 1: AWS Route 53 (Recommended)**
- **Cost**: ~$12/year for domain + $0.50/month for hosted zone
- **Benefits**: Integrated with AWS, easy DNS management
- **Best for**: Production deployments

### **Option 2: External Registrar (Namecheap, GoDaddy, etc.)**
- **Cost**: ~$10-15/year for domain
- **Benefits**: More domain options, often cheaper
- **Best for**: Cost-conscious deployments

## 🚀 Complete Domain Setup Process

### 1. Register Domain Name

#### **AWS Route 53 (Recommended)**
```bash
# Go to AWS Console → Route 53 → Registered domains
# Click "Register Domain"
# Search for available domains like:
# - landscaper-app.com
# - landscaper-pro.com  
# - landscaper-dashboard.com
# - yourcompany-landscaper.com
```

#### **External Registrar (Alternative)**
Popular options:
- **Namecheap**: $8-12/year
- **GoDaddy**: $10-15/year  
- **Google Domains**: $12/year
- **Cloudflare**: $8-12/year

### 2. DNS Configuration

#### **For AWS Route 53:**
```bash
# After domain registration, create hosted zone
# AWS Console → Route 53 → Hosted zones → Create hosted zone
# Domain name: yourdomain.com
# Type: Public hosted zone
```

#### **For External Registrar:**
```bash
# Point nameservers to AWS Route 53
# Get nameservers from AWS Route 53 hosted zone
# Update at your domain registrar
```

### 3. SSL Certificate Setup

#### **AWS Certificate Manager (Free)**
```bash
# AWS Console → Certificate Manager → Request certificate
# Domain name: yourdomain.com
# Subject alternative names: *.yourdomain.com
# Validation method: DNS validation
```

#### **Let's Encrypt (Alternative)**
```bash
# Install certbot on EC2 instance
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 🔧 Updated Infrastructure Configuration
