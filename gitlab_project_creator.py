#!/usr/bin/env python3
"""
GitLab Project Creator Script

This script helps you create projects in GitLab using the GitLab API.
You'll need a GitLab Personal Access Token with 'api' scope.

Usage:
1. Set your GitLab token: export GITLAB_TOKEN="your_token_here"
2. Set your GitLab URL: export GITLAB_URL="https://gitlab.com" (or your self-hosted instance)
3. Run: python gitlab_project_creator.py
"""

import os
import requests
import json
from typing import Optional, Dict, Any

class GitLabProjectCreator:
    def __init__(self, token: Optional[str] = None, url: Optional[str] = None):
        self.token = token or os.getenv('GITLAB_TOKEN')
        self.url = url or os.getenv('GITLAB_URL', 'https://gitlab.com')
        self.api_base = f"{self.url}/api/v4"
        
        if not self.token:
            raise ValueError("GitLab token is required. Set GITLAB_TOKEN environment variable or pass it to the constructor.")
    
    def create_project(self, name: str, description: str = "", visibility: str = "private", 
                      namespace_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a new GitLab project
        
        Args:
            name: Project name
            description: Project description
            visibility: 'private', 'internal', or 'public'
            namespace_id: ID of the namespace/group (optional)
        
        Returns:
            Dict containing the created project information
        """
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'name': name,
            'description': description,
            'visibility': visibility
        }
        
        if namespace_id:
            data['namespace_id'] = namespace_id
        
        response = requests.post(
            f"{self.api_base}/projects",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create project: {response.status_code} - {response.text}")
    
    def list_projects(self) -> list:
        """List all projects accessible to the user"""
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        response = requests.get(
            f"{self.api_base}/projects",
            headers=headers,
            params={'per_page': 100}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list projects: {response.status_code} - {response.text}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        
        response = requests.get(
            f"{self.api_base}/user",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.status_code} - {response.text}")

def main():
    """Interactive project creation"""
    try:
        creator = GitLabProjectCreator()
        
        # Get user info
        print("🔍 Getting user information...")
        user_info = creator.get_user_info()
        print(f"✅ Logged in as: {user_info['name']} (@{user_info['username']})")
        
        # List existing projects
        print("\n📋 Listing existing projects...")
        projects = creator.list_projects()
        print(f"Found {len(projects)} projects")
        
        # Interactive project creation
        print("\n🚀 Create a new GitLab project")
        print("=" * 40)
        
        name = input("Project name: ").strip()
        if not name:
            print("❌ Project name is required")
            return
        
        description = input("Description (optional): ").strip()
        visibility = input("Visibility (private/internal/public) [private]: ").strip() or "private"
        
        if visibility not in ['private', 'internal', 'public']:
            print("❌ Invalid visibility. Using 'private'")
            visibility = "private"
        
        # Create the project
        print(f"\n🔄 Creating project '{name}'...")
        project = creator.create_project(
            name=name,
            description=description,
            visibility=visibility
        )
        
        print("✅ Project created successfully!")
        print(f"📁 Project ID: {project['id']}")
        print(f"🔗 Project URL: {project['web_url']}")
        print(f"📋 SSH URL: {project['ssh_url_to_repo']}")
        print(f"🔗 HTTP URL: {project['http_url_to_repo']}")
        
        # Ask if user wants to add remote
        add_remote = input("\n🤔 Add this as a remote to your current git repository? (y/n): ").strip().lower()
        if add_remote in ['y', 'yes']:
            remote_name = input("Remote name [origin]: ").strip() or "origin"
            os.system(f"git remote add {remote_name} {project['http_url_to_repo']}")
            print(f"✅ Added remote '{remote_name}' pointing to {project['http_url_to_repo']}")
            
            push = input("Push current code to the new repository? (y/n): ").strip().lower()
            if push in ['y', 'yes']:
                os.system(f"git push -u {remote_name} main")
                print("✅ Code pushed to GitLab!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("1. Set GITLAB_TOKEN environment variable with your Personal Access Token")
        print("2. Set GITLAB_URL if using a self-hosted GitLab instance")
        print("3. Token has 'api' scope permissions")

if __name__ == "__main__":
    main()
