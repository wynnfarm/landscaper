#!/bin/bash
# Complete AWS Deployment Script with Domain Setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if required tools are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed. Install with: brew install terraform"
        exit 1
    fi
    
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Install with: brew install awscli"
        exit 1
    fi
    
    if ! aws sts get-caller-identity --output table &> /dev/null; then
        print_error "AWS credentials not configured. Run: aws configure"
        exit 1
    fi
    
    print_success "All prerequisites met!"
}

# Domain setup
setup_domain() {
    print_status "Setting up domain configuration..."
    
    read -p "Do you want to use a custom domain? (y/n): " use_domain
    
    if [[ $use_domain =~ ^[Yy]$ ]]; then
        read -p "Enter your domain name (e.g., landscaper-app.com): " domain_name
        
        if [[ -z "$domain_name" ]]; then
            print_error "Domain name cannot be empty"
            exit 1
        fi
        
        print_status "Domain setup options:"
        echo "1. AWS Route 53 (recommended, ~$12/year)"
        echo "2. External registrar (Namecheap, GoDaddy, etc.)"
        read -p "Choose domain provider (1 or 2): " domain_provider
        
        case $domain_provider in
            1)
                print_status "Setting up AWS Route 53 domain..."
                print_warning "Please register your domain in AWS Console first:"
                print_warning "AWS Console → Route 53 → Registered domains → Register Domain"
                print_warning "Search for: $domain_name"
                read -p "Press Enter after registering the domain..."
                ;;
            2)
                print_status "Setting up external domain..."
                print_warning "Please register your domain with your preferred registrar"
                print_warning "You'll need to point nameservers to AWS Route 53"
                read -p "Press Enter after registering the domain..."
                ;;
            *)
                print_error "Invalid choice"
                exit 1
                ;;
        esac
        
        # Create hosted zone in Route 53
        print_status "Creating Route 53 hosted zone..."
        aws route53 create-hosted-zone --name "$domain_name" --caller-reference "$(date +%s)"
        
        # Get nameservers
        zone_id=$(aws route53 list-hosted-zones --query "HostedZones[?Name=='$domain_name.'].Id" --output text | cut -d'/' -f3)
        nameservers=$(aws route53 get-hosted-zone --id "$zone_id" --query "DelegationSet.NameServers" --output text)
        
        print_success "Hosted zone created!"
        print_warning "Update your domain's nameservers to:"
        echo "$nameservers"
        
        # Create SSL certificate
        print_status "Creating SSL certificate..."
        certificate_arn=$(aws acm request-certificate \
            --domain-name "$domain_name" \
            --subject-alternative-names "www.$domain_name" \
            --validation-method DNS \
            --query 'CertificateArn' --output text)
        
        print_success "SSL certificate requested!"
        print_warning "Certificate ARN: $certificate_arn"
        print_warning "You'll need to validate the certificate in AWS Console"
        
        # Update terraform variables
        cat > terraform/terraform.tfvars <<EOF
domain_name = "$domain_name"
certificate_arn = "$certificate_arn"
EOF
        
    else
        print_status "Proceeding without custom domain..."
        domain_name=""
    fi
}

# Deploy infrastructure
deploy_infrastructure() {
    print_status "Deploying AWS infrastructure..."
    
    cd terraform
    
    print_status "Initializing Terraform..."
    terraform init
    
    print_status "Planning deployment..."
    terraform plan
    
    read -p "Proceed with deployment? (y/n): " proceed
    
    if [[ $proceed =~ ^[Yy]$ ]]; then
        print_status "Applying Terraform configuration..."
        terraform apply -auto-approve
        
        # Get outputs
        public_ip=$(terraform output -raw public_ip)
        app_url=$(terraform output -raw app_url)
        
        print_success "Infrastructure deployed successfully!"
        print_success "Public IP: $public_ip"
        print_success "Application URL: $app_url"
        
        # Save outputs for later use
        echo "PUBLIC_IP=$public_ip" > ../.env.deployment
        echo "APP_URL=$app_url" >> ../.env.deployment
        
    else
        print_warning "Deployment cancelled"
        exit 0
    fi
    
    cd ..
}

# Deploy application
deploy_application() {
    print_status "Deploying application to EC2 instance..."
    
    source .env.deployment
    
    print_status "Waiting for EC2 instance to be ready..."
    sleep 60
    
    print_status "SSH into instance and deploying application..."
    
    # Create deployment script
    cat > deploy_app.sh <<EOF
#!/bin/bash
set -e

echo "Deploying Landscaper application..."

# Clone repository
cd /opt/landscaper
if [ -d ".git" ]; then
    git pull origin main
else
    git clone https://github.com/wynnfarm/landscaper.git .
fi

# Create environment file
if [ ! -f ".env" ]; then
    cp .env.template .env
    echo "Please edit .env file with your credentials"
    echo "Then run: ./deploy.sh"
else
    ./deploy.sh
fi
EOF
    
    # Copy deployment script to EC2
    scp -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no deploy_app.sh ubuntu@$PUBLIC_IP:/tmp/
    
    # Execute deployment
    ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@$PUBLIC_IP "chmod +x /tmp/deploy_app.sh && /tmp/deploy_app.sh"
    
    print_success "Application deployment initiated!"
    print_warning "You may need to manually configure the .env file on the EC2 instance"
    print_success "Access your application at: $APP_URL"
}

# Main deployment flow
main() {
    echo "🚀 Landscaper AWS Deployment Script"
    echo "=================================="
    
    check_prerequisites
    setup_domain
    deploy_infrastructure
    deploy_application
    
    print_success "Deployment complete!"
    print_status "Next steps:"
    echo "1. SSH into your EC2 instance"
    echo "2. Configure .env file with your credentials"
    echo "3. Run: ./deploy.sh"
    echo "4. Access your application"
}

# Run main function
main "$@"
