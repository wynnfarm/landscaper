#!/bin/bash

# Security Hardening Script for Landscaper Application
# This script implements additional security measures

set -e

echo "🔒 Implementing security hardening..."

# 1. Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install and configure fail2ban
echo "🛡️ Installing fail2ban..."
sudo apt-get install -y fail2ban

# Create fail2ban configuration
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 3
EOF

# 3. Configure UFW firewall
echo "🔥 Configuring UFW firewall..."
sudo ufw --force enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force reload

# 4. Secure SSH configuration
echo "🔐 Securing SSH configuration..."
sudo tee -a /etc/ssh/sshd_config > /dev/null <<EOF

# Security hardening
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
Protocol 2
EOF

sudo systemctl restart sshd

# 5. Install and configure logwatch
echo "📊 Installing logwatch..."
sudo apt-get install -y logwatch

# 6. Set up automatic security updates
echo "🔄 Setting up automatic security updates..."
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 7. Configure nginx security headers
echo "🌐 Configuring nginx security headers..."
sudo tee /etc/nginx/conf.d/security-headers.conf > /dev/null <<EOF
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Rate limiting
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone \$binary_remote_addr zone=login:10m rate=1r/s;

# Hide nginx version
server_tokens off;
EOF

# 8. Restart services
echo "🔄 Restarting services..."
sudo systemctl restart fail2ban
sudo systemctl restart nginx

# 9. Create security monitoring script
echo "📈 Creating security monitoring script..."
sudo tee /usr/local/bin/security-check.sh > /dev/null <<'EOF'
#!/bin/bash

echo "🔒 Security Status Check"
echo "========================"

echo "1. Failed login attempts:"
sudo grep "Failed password" /var/log/auth.log | tail -5

echo "2. SSH connections:"
sudo grep "Accepted" /var/log/auth.log | tail -5

echo "3. UFW status:"
sudo ufw status

echo "4. Fail2ban status:"
sudo fail2ban-client status

echo "5. Recent nginx errors:"
sudo tail -10 /var/log/nginx/error.log

echo "6. System load:"
uptime

echo "7. Disk usage:"
df -h

echo "8. Memory usage:"
free -h
EOF

sudo chmod +x /usr/local/bin/security-check.sh

# 10. Set up log rotation for application logs
echo "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/landscaper > /dev/null <<EOF
/opt/landscaper/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        systemctl reload nginx
    endscript
}
EOF

echo "✅ Security hardening completed!"
echo ""
echo "🔒 Security measures implemented:"
echo "  ✅ Fail2ban for brute force protection"
echo "  ✅ UFW firewall configured"
echo "  ✅ SSH hardened"
echo "  ✅ Automatic security updates"
echo "  ✅ Nginx security headers"
echo "  ✅ Rate limiting"
echo "  ✅ Log monitoring"
echo ""
echo "📊 To check security status: sudo /usr/local/bin/security-check.sh"
echo "🛡️ To view fail2ban status: sudo fail2ban-client status"
echo "🔥 To view firewall status: sudo ufw status"
