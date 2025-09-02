#!/usr/bin/env python3
"""
Context Switching Utility for Landscaper Project
Automatically manages context switching based on task type and user input.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

class ContextSwitcher:
    """Manages context switching for the Landscaper project"""
    
    def __init__(self):
        self.project_root = Path("/Users/wynnfarm/dev/landscaper")
        self.contexts_dir = self.project_root / "contexts"
        self.rules_file = self.project_root / "CONTEXT_SWITCHING_RULES.md"
        
        # Define context types and their triggers
        self.context_types = {
            "development": {
                "triggers": ["develop", "code", "implement", "build", "create", "add", "fix", "debug"],
                "context": "landscaper",
                "description": "Development context for coding and implementation"
            },
            "testing": {
                "triggers": ["test", "validate", "verify", "check", "run test", "debug"],
                "context": "landscaper-test",
                "description": "Testing context for validation and testing"
            },
            "deployment": {
                "triggers": ["deploy", "production", "docker", "container", "infrastructure"],
                "context": "landscaper-deploy",
                "description": "Deployment context for production setup"
            },
            "documentation": {
                "triggers": ["document", "docs", "readme", "comment", "guide"],
                "context": "landscaper-docs",
                "description": "Documentation context for writing docs"
            }
        }
    
    def detect_context_type(self, user_input: str) -> str:
        """Detect the appropriate context type based on user input"""
        user_input_lower = user_input.lower()
        
        for context_type, config in self.context_types.items():
            for trigger in config["triggers"]:
                if trigger in user_input_lower:
                    return context_type
        
        # Default to development context
        return "development"
    
    def switch_context(self, context_type: str, task_description: str = "") -> dict:
        """Switch to the specified context type"""
        if context_type not in self.context_types:
            raise ValueError(f"Unknown context type: {context_type}")
        
        context_config = self.context_types[context_type]
        context_name = context_config["context"]
        
        # Create context status
        context_status = {
            "project": context_name,
            "type": context_type,
            "description": context_config["description"],
            "task": task_description,
            "switched_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Save context status
        self._save_context_status(context_name, context_status)
        
        return context_status
    
    def _save_context_status(self, context_name: str, status: dict):
        """Save context status to file"""
        status_file = self.contexts_dir / f"{context_name}_CONTEXT_STATUS.md"
        
        status_content = f"""# {context_name.upper()} - CONTEXT STATUS

## Current Context Type
{status['type']}

## Current Task
{status['task']}

## Context Description
{status['description']}

## Status
{status['status']}

## Last Updated
{status['switched_at']}

## Context Rules
- Follow context-specific guidelines
- Save progress frequently
- Update context with completed features
- Track any issues encountered

---
*Last updated: {status['switched_at']}*
"""
        
        with open(status_file, 'w') as f:
            f.write(status_content)
    
    def get_current_context(self) -> dict:
        """Get the current active context"""
        # Look for the most recently updated context file
        context_files = list(self.contexts_dir.glob("*_CONTEXT_STATUS.md"))
        
        if not context_files:
            return {"project": "landscaper", "type": "development", "status": "default"}
        
        # Find the most recently modified file
        latest_file = max(context_files, key=lambda f: f.stat().st_mtime)
        context_name = latest_file.stem.replace("_CONTEXT_STATUS", "")
        
        return {
            "project": context_name,
            "file": str(latest_file),
            "last_modified": datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
        }
    
    def validate_context(self, context_name: str) -> bool:
        """Validate that a context is properly set up"""
        status_file = self.contexts_dir / f"{context_name}_CONTEXT_STATUS.md"
        cache_file = self.contexts_dir / f"{context_name}_context_cache.json"
        
        return status_file.exists() and cache_file.exists()
    
    def list_contexts(self) -> list:
        """List all available contexts"""
        context_files = list(self.contexts_dir.glob("*_CONTEXT_STATUS.md"))
        contexts = []
        
        for file in context_files:
            context_name = file.stem.replace("_CONTEXT_STATUS", "")
            contexts.append({
                "name": context_name,
                "file": str(file),
                "exists": True,
                "last_modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
        
        return contexts

def main():
    """Main function for command-line usage"""
    switcher = ContextSwitcher()
    
    if len(sys.argv) < 2:
        print("Usage: python context_switcher.py <command> [options]")
        print("\nCommands:")
        print("  detect <user_input>    - Detect context type from user input")
        print("  switch <context_type>  - Switch to specified context type")
        print("  current               - Show current context")
        print("  list                  - List all available contexts")
        print("  validate <context>    - Validate context setup")
        return
    
    command = sys.argv[1]
    
    if command == "detect" and len(sys.argv) > 2:
        user_input = " ".join(sys.argv[2:])
        context_type = switcher.detect_context_type(user_input)
        print(f"Detected context type: {context_type}")
        print(f"Context: {switcher.context_types[context_type]['context']}")
        print(f"Description: {switcher.context_types[context_type]['description']}")
    
    elif command == "switch" and len(sys.argv) > 2:
        context_type = sys.argv[2]
        task_description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        
        try:
            status = switcher.switch_context(context_type, task_description)
            print(f"Switched to {context_type} context")
            print(f"Project: {status['project']}")
            print(f"Task: {status['task']}")
        except ValueError as e:
            print(f"Error: {e}")
    
    elif command == "current":
        context = switcher.get_current_context()
        print(f"Current context: {context['project']}")
        print(f"File: {context['file']}")
        print(f"Last modified: {context['last_modified']}")
    
    elif command == "list":
        contexts = switcher.list_contexts()
        print("Available contexts:")
        for ctx in contexts:
            print(f"  - {ctx['name']} (last modified: {ctx['last_modified']})")
    
    elif command == "validate" and len(sys.argv) > 2:
        context_name = sys.argv[2]
        is_valid = switcher.validate_context(context_name)
        print(f"Context '{context_name}' is {'valid' if is_valid else 'invalid'}")
    
    else:
        print("Invalid command or missing arguments")
        print("Use 'python context_switcher.py' for usage information")

if __name__ == "__main__":
    main()
