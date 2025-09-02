#!/bin/bash
# GitLab Project Creator - Shell Version
# Usage: ./create_gitlab_project.sh "project_name" "description" "visibility"

set -e

# Configuration
GITLAB_TOKEN="${GITLAB_TOKEN:-}"
GITLAB_URL="${GITLAB_URL:-https://gitlab.com}"

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

# Check if token is set
if [ -z "$GITLAB_TOKEN" ]; then
    print_error "GITLAB_TOKEN environment variable is not set"
    echo "Please set it with: export GITLAB_TOKEN='your_token_here'"
    exit 1
fi

# Get project details
PROJECT_NAME="${1:-}"
PROJECT_DESCRIPTION="${2:-}"
PROJECT_VISIBILITY="${3:-private}"

# Validate visibility
if [[ ! "$PROJECT_VISIBILITY" =~ ^(private|internal|public)$ ]]; then
    print_warning "Invalid visibility '$PROJECT_VISIBILITY'. Using 'private'"
    PROJECT_VISIBILITY="private"
fi

# If no project name provided, prompt for it
if [ -z "$PROJECT_NAME" ]; then
    echo -n "Enter project name: "
    read PROJECT_NAME
fi

if [ -z "$PROJECT_NAME" ]; then
    print_error "Project name is required"
    exit 1
fi

# If no description provided, prompt for it
if [ -z "$PROJECT_DESCRIPTION" ]; then
    echo -n "Enter project description (optional): "
    read PROJECT_DESCRIPTION
fi

print_status "Creating GitLab project: $PROJECT_NAME"

# Create the project using GitLab API
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "Authorization: Bearer $GITLAB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"$PROJECT_NAME\",
        \"description\": \"$PROJECT_DESCRIPTION\",
        \"visibility\": \"$PROJECT_VISIBILITY\"
    }" \
    "$GITLAB_URL/api/v4/projects")

# Extract HTTP status code and response body
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    print_success "Project created successfully!"
    
    # Extract project URL from response
    PROJECT_URL=$(echo "$RESPONSE_BODY" | grep -o '"web_url":"[^"]*"' | cut -d'"' -f4)
    HTTP_URL=$(echo "$RESPONSE_BODY" | grep -o '"http_url_to_repo":"[^"]*"' | cut -d'"' -f4)
    SSH_URL=$(echo "$RESPONSE_BODY" | grep -o '"ssh_url_to_repo":"[^"]*"' | cut -d'"' -f4)
    
    echo "Project URL: $PROJECT_URL"
    echo "HTTP URL: $HTTP_URL"
    echo "SSH URL: $SSH_URL"
    
    # Ask if user wants to add remote
    echo -n "Add this as a remote to your current git repository? (y/n): "
    read ADD_REMOTE
    
    if [[ "$ADD_REMOTE" =~ ^[Yy]$ ]]; then
        echo -n "Remote name (default: origin): "
        read REMOTE_NAME
        REMOTE_NAME="${REMOTE_NAME:-origin}"
        
        git remote add "$REMOTE_NAME" "$HTTP_URL"
        print_success "Added remote '$REMOTE_NAME' pointing to $HTTP_URL"
        
        echo -n "Push current code to the new repository? (y/n): "
        read PUSH_CODE
        
        if [[ "$PUSH_CODE" =~ ^[Yy]$ ]]; then
            git push -u "$REMOTE_NAME" main
            print_success "Code pushed to GitLab!"
        fi
    fi
    
else
    print_error "Failed to create project. HTTP Code: $HTTP_CODE"
    echo "Response: $RESPONSE_BODY"
    exit 1
fi
