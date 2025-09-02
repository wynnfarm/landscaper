"""
Context Manager MCP Client for Landscaper Project

This client integrates with the context_manager MCP to maintain project context,
track goals, and manage conversation state for the landscaper application.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ContextManagerClient:
    """Client for interacting with the Context Manager MCP."""
    
    def __init__(self, project_name: str = "landscaper", project_root: Optional[str] = None):
        self.project_name = project_name
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.context_file = self.project_root / "contexts" / f"{self.project_name}_context_cache.json"
        self.status_file = self.project_root / "contexts" / f"{self.project_name}_CONTEXT_STATUS.md"
        
        # Ensure contexts directory exists
        self.context_file.parent.mkdir(exist_ok=True)
        
        # Initialize context if it doesn't exist
        if not self.context_file.exists():
            self._initialize_context()
    
    def _initialize_context(self):
        """Initialize the context file with default values."""
        initial_context = {
            "project_name": self.project_name,
            "current_goal": "Build a mobile-first landscaping web application",
            "completed_features": [
                "Basic Flask web application structure",
                "Mobile-first CSS framework",
                "Responsive design with touch-friendly interface",
                "PWA capabilities with service worker",
                "Contact integration (phone, email, maps)",
                "Service catalog and pricing information"
            ],
            "current_issues": [],
            "next_steps": [
                "Integrate MCP services (Context Manager and Persona Manager)",
                "Add AI agent for customer interactions",
                "Implement booking system",
                "Add image gallery for completed projects",
                "Set up database for customer data"
            ],
            "current_state": {
                "development_phase": "MCP Integration",
                "last_major_update": datetime.now().isoformat(),
                "active_features": ["web_ui", "mobile_optimization", "pwa"]
            },
            "key_files": [
                "app.py",
                "static/css/mobile.css",
                "static/js/app.js",
                "templates/base.html",
                "templates/index.html"
            ],
            "context_anchors": [
                {
                    "key": "PROJECT_TYPE",
                    "value": "Mobile-first web application for landscaping services",
                    "description": "Primary project type and target platform",
                    "priority": 1
                },
                {
                    "key": "TECH_STACK",
                    "value": "Flask, HTML5, CSS3, JavaScript, PWA",
                    "description": "Main technologies used in the project",
                    "priority": 1
                },
                {
                    "key": "TARGET_AUDIENCE",
                    "value": "Mobile users seeking landscaping services",
                    "description": "Primary user demographic",
                    "priority": 2
                }
            ],
            "conversation_history": [],
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_context(initial_context)
        self._create_status_file(initial_context)
    
    def _save_context(self, context: Dict[str, Any]):
        """Save context to JSON file."""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(context, f, indent=2)
            logger.info(f"Context saved to {self.context_file}")
        except Exception as e:
            logger.error(f"Failed to save context: {e}")
    
    def _load_context(self) -> Dict[str, Any]:
        """Load context from JSON file."""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load context: {e}")
            return {}
    
    def _create_status_file(self, context: Dict[str, Any]):
        """Create a human-readable status file."""
        status_content = f"""# {self.project_name.upper()} - CONTEXT STATUS

## Current Goal
{context.get('current_goal', 'No goal set')}

## Completed Features
{chr(10).join(f"- {feature}" for feature in context.get('completed_features', []))}

## Current Issues
{chr(10).join(f"- {issue}" for issue in context.get('current_issues', [])) if context.get('current_issues') else "No current issues"}

## Next Steps
{chr(10).join(f"- {step}" for step in context.get('next_steps', []))}

## Current State
- Development Phase: {context.get('current_state', {}).get('development_phase', 'Unknown')}
- Last Updated: {context.get('last_updated', 'Unknown')}

## Key Files
{chr(10).join(f"- {file}" for file in context.get('key_files', []))}

## Context Anchors
{chr(10).join(f"- **{anchor['key']}**: {anchor['value']} - {anchor['description']}" for anchor in context.get('context_anchors', []))}

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        try:
            with open(self.status_file, 'w') as f:
                f.write(status_content)
            logger.info(f"Status file created at {self.status_file}")
        except Exception as e:
            logger.error(f"Failed to create status file: {e}")
    
    def set_current_goal(self, goal: str) -> bool:
        """Set the current primary goal."""
        try:
            context = self._load_context()
            context['current_goal'] = goal
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to set goal: {e}")
            return False
    
    def add_completed_feature(self, feature: str) -> bool:
        """Add a completed feature to the status."""
        try:
            context = self._load_context()
            completed_features = context.get('completed_features', [])
            if feature not in completed_features:
                completed_features.append(feature)
                context['completed_features'] = completed_features
                context['last_updated'] = datetime.now().isoformat()
                self._save_context(context)
                self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to add completed feature: {e}")
            return False
    
    def add_current_issue(self, problem: str, location: str = "", root_cause: str = "", status: str = "open") -> bool:
        """Add a current issue to track."""
        try:
            context = self._load_context()
            issues = context.get('current_issues', [])
            
            issue = {
                "problem": problem,
                "location": location,
                "root_cause": root_cause,
                "status": status,
                "created_at": datetime.now().isoformat()
            }
            
            issues.append(issue)
            context['current_issues'] = issues
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to add issue: {e}")
            return False
    
    def add_next_step(self, step: str) -> bool:
        """Add a next step to the plan."""
        try:
            context = self._load_context()
            next_steps = context.get('next_steps', [])
            if step not in next_steps:
                next_steps.append(step)
                context['next_steps'] = next_steps
                context['last_updated'] = datetime.now().isoformat()
                self._save_context(context)
                self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to add next step: {e}")
            return False
    
    def add_context_anchor(self, key: str, value: str, description: str = "", priority: int = 1) -> bool:
        """Add a context anchor for important information."""
        try:
            context = self._load_context()
            anchors = context.get('context_anchors', [])
            
            # Remove existing anchor with same key
            anchors = [a for a in anchors if a.get('key') != key]
            
            anchor = {
                "key": key,
                "value": value,
                "description": description,
                "priority": priority,
                "created_at": datetime.now().isoformat()
            }
            
            anchors.append(anchor)
            context['context_anchors'] = anchors
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to add context anchor: {e}")
            return False
    
    def update_current_state(self, state_updates: Dict[str, Any]) -> bool:
        """Update the current state with new information."""
        try:
            context = self._load_context()
            current_state = context.get('current_state', {})
            current_state.update(state_updates)
            context['current_state'] = current_state
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to update state: {e}")
            return False
    
    def add_conversation_entry(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add an entry to the conversation history."""
        try:
            context = self._load_context()
            history = context.get('conversation_history', [])
            
            entry = {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            history.append(entry)
            
            # Keep only last 50 entries to prevent file from growing too large
            if len(history) > 50:
                history = history[-50:]
            
            context['conversation_history'] = history
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            return True
        except Exception as e:
            logger.error(f"Failed to add conversation entry: {e}")
            return False
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of the current context."""
        context = self._load_context()
        return {
            "project_name": context.get('project_name', ''),
            "current_goal": context.get('current_goal', ''),
            "completed_features_count": len(context.get('completed_features', [])),
            "current_issues_count": len(context.get('current_issues', [])),
            "next_steps_count": len(context.get('next_steps', [])),
            "context_anchors_count": len(context.get('context_anchors', [])),
            "last_updated": context.get('last_updated', ''),
            "development_phase": context.get('current_state', {}).get('development_phase', 'Unknown')
        }
    
    def get_full_context(self) -> Dict[str, Any]:
        """Get the complete context data."""
        return self._load_context()
    
    def clear_issues(self) -> bool:
        """Clear all current issues."""
        try:
            context = self._load_context()
            context['current_issues'] = []
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to clear issues: {e}")
            return False
    
    def mark_issue_resolved(self, problem: str) -> bool:
        """Mark a specific issue as resolved."""
        try:
            context = self._load_context()
            issues = context.get('current_issues', [])
            
            for issue in issues:
                if issue.get('problem') == problem:
                    issue['status'] = 'resolved'
                    issue['resolved_at'] = datetime.now().isoformat()
                    break
            
            context['current_issues'] = issues
            context['last_updated'] = datetime.now().isoformat()
            self._save_context(context)
            self._create_status_file(context)
            return True
        except Exception as e:
            logger.error(f"Failed to mark issue as resolved: {e}")
            return False


