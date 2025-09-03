#!/bin/bash
# Terraform Management Script - Easy Deploy/Destroy/Rebuild

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

# Check if we're in the right directory
check_directory() {
    if [ ! -f "terraform/main.tf" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
}

# Deploy infrastructure
deploy() {
    print_status "🚀 Deploying Landscaper infrastructure..."
    
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
        public_ip=$(terraform output -raw public_ip 2>/dev/null || echo "N/A")
        app_url=$(terraform output -raw app_url 2>/dev/null || echo "N/A")
        
        print_success "Infrastructure deployed successfully!"
        if [ "$public_ip" != "N/A" ]; then
            print_success "Public IP: $public_ip"
        fi
        if [ "$app_url" != "N/A" ]; then
            print_success "Application URL: $app_url"
        fi
        
        # Save outputs for later use
        echo "PUBLIC_IP=$public_ip" > ../.env.deployment
        echo "APP_URL=$app_url" >> ../.env.deployment
        
    else
        print_warning "Deployment cancelled"
    fi
    
    cd ..
}

# Destroy infrastructure
destroy() {
    print_status "🗑️  Destroying Landscaper infrastructure..."
    
    cd terraform
    
    if [ ! -f ".terraform/terraform.tfstate" ]; then
        print_warning "No Terraform state found. Nothing to destroy."
        cd ..
        return
    fi
    
    print_status "Planning destruction..."
    terraform plan -destroy
    
    read -p "Are you sure you want to destroy ALL infrastructure? (y/n): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        print_status "Destroying infrastructure..."
        terraform destroy -auto-approve
        
        print_success "Infrastructure destroyed successfully!"
        print_warning "All data has been permanently deleted!"
        
        # Clean up deployment file
        rm -f ../.env.deployment
        
    else
        print_warning "Destruction cancelled"
    fi
    
    cd ..
}

# Rebuild infrastructure
rebuild() {
    print_status "🔄 Rebuilding Landscaper infrastructure..."
    
    print_warning "This will destroy and recreate all infrastructure!"
    read -p "Continue? (y/n): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        destroy
        deploy
    else
        print_warning "Rebuild cancelled"
    fi
}

# Show status
status() {
    print_status "📊 Infrastructure Status..."
    
    cd terraform
    
    if [ ! -f ".terraform/terraform.tfstate" ]; then
        print_warning "No Terraform state found. Infrastructure not deployed."
        cd ..
        return
    fi
    
    print_status "Current infrastructure:"
    terraform show -json | jq -r '.values.root_module.resources[] | "\(.type).\(.name): \(.values.tags.Name // .name)"' 2>/dev/null || terraform show
    
    # Show outputs
    print_status "Outputs:"
    terraform output
    
    cd ..
}

# Show costs
costs() {
    print_status "💰 Cost Estimation..."
    
    cd terraform
    
    if [ ! -f ".terraform/terraform.tfstate" ]; then
        print_warning "No infrastructure deployed. Cannot estimate costs."
        cd ..
        return
    fi
    
    print_status "Current monthly costs (estimated):"
    echo "EC2 t3.micro: ~$8.47/month"
    echo "EBS Storage (20GB): ~$1.80/month"
    echo "Data Transfer: ~$0.09/GB"
    echo "Route 53 Hosted Zone: ~$0.50/month (if using domain)"
    echo "Total: ~$10-15/month"
    
    cd ..
}

# Show logs
logs() {
    print_status "📋 Application Logs..."
    
    if [ ! -f ".env.deployment" ]; then
        print_warning "No deployment found. Run deploy first."
        return
    fi
    
    source .env.deployment
    
    if [ "$PUBLIC_IP" = "N/A" ]; then
        print_warning "No public IP found."
        return
    fi
    
    print_status "Connecting to EC2 instance for logs..."
    ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@$PUBLIC_IP "docker-compose logs -f" 2>/dev/null || print_warning "Could not connect to instance"
}

# Help
show_help() {
    echo "🌿 Landscaper Terraform Management Script"
    echo "=========================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    - Deploy infrastructure"
    echo "  destroy   - Destroy all infrastructure"
    echo "  rebuild   - Destroy and redeploy"
    echo "  status    - Show current status"
    echo "  costs     - Show cost estimation"
    echo "  logs      - Show application logs"
    echo "  help      - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Deploy infrastructure"
    echo "  $0 destroy   # Tear down everything"
    echo "  $0 rebuild   # Rebuild from scratch"
    echo ""
    echo "Safety:"
    echo "  - All commands ask for confirmation"
    echo "  - destroy removes ALL data permanently"
    echo "  - rebuild = destroy + deploy"
}

# Main function
main() {
    check_directory
    
    case "${1:-help}" in
        deploy)
            deploy
            ;;
        destroy)
            destroy
            ;;
        rebuild)
            rebuild
            ;;
        status)
            status
            ;;
        costs)
            costs
            ;;
        logs)
            logs
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
