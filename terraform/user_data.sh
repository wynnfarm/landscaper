#!/bin/bash
# User data script for EC2 instance setup
# This script runs when the EC2 instance first starts

set -e

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker and Docker Compose
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Install Node.js and npm (for React build)
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install nginx for reverse proxy
echo "Installing nginx..."
sudo apt-get install -y nginx

# Create application directory
sudo mkdir -p /opt/landscaper
sudo chown ubuntu:ubuntu /opt/landscaper

# Clone the repository (you'll need to set up deployment keys or use HTTPS)
# For now, we'll create a placeholder
echo "Setting up application directory..."

# Create nginx configuration
if [ -n "$domain_name" ]; then
    # Production configuration with domain
    sudo tee /etc/nginx/sites-available/landscaper <<EOF
server {
    listen 80;
    server_name $domain_name www.$domain_name;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $domain_name www.$domain_name;

    # SSL configuration will be added by certbot
    # ssl_certificate /etc/letsencrypt/live/$domain_name/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/$domain_name/privkey.pem;

    # React frontend
    location / {
        root /opt/landscaper/landscaper-frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Flask API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files
    location /static/ {
        proxy_pass http://localhost:5000;
    }
}
EOF
else
    # Development configuration without domain
    sudo tee /etc/nginx/sites-available/landscaper <<EOF
server {
    listen 80;
    server_name _;

    # React frontend
    location / {
        root /opt/landscaper/landscaper-frontend/build;
        try_files \$uri \$uri/ /index.html;
    }

    # Flask API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files
    location /static/ {
        proxy_pass http://localhost:5000;
    }
}
EOF
fi

# Enable the site
sudo ln -sf /etc/nginx/sites-available/landscaper /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# Install SSL certificate if domain is configured
if [ -n "$domain_name" ]; then
    echo "Setting up SSL certificate for $domain_name..."
    sudo apt-get install -y certbot python3-certbot-nginx
    
    # Generate SSL certificate
    sudo certbot --nginx -d $domain_name -d www.$domain_name --non-interactive --agree-tos --email admin@$domain_name
    
    # Set up automatic renewal
    echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
fi

# Create systemd service for the application
sudo tee /etc/systemd/system/landscaper.service <<EOF
[Unit]
Description=Landscaper Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/landscaper
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=ubuntu
Group=ubuntu

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl enable landscaper.service

# Create a simple deployment script
sudo tee /opt/landscaper/deploy.sh <<EOF
#!/bin/bash
set -e

echo "Deploying Landscaper application..."

# Pull latest changes
git pull origin main

# Build React frontend
cd landscaper-frontend
npm install
npm run build
cd ..

# Restart services
docker-compose down
docker-compose up -d

echo "Deployment complete!"
EOF

sudo chmod +x /opt/landscaper/deploy.sh

# Create environment file template
sudo tee /opt/landscaper/.env.template <<EOF
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password_here
DB_PASSWORD=your_secure_db_password_here

# Application Security
SECRET_KEY=your_secure_secret_key_here

# pgAdmin Configuration (for development)
PGADMIN_PASSWORD=your_secure_pgadmin_password_here
EOF

echo "EC2 instance setup complete!"
echo "Next steps:"
echo "1. SSH into the instance"
echo "2. Copy your application files to /opt/landscaper"
echo "3. Create .env file with your credentials"
echo "4. Run: sudo systemctl start landscaper"
