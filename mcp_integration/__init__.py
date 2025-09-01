"""
MCP Integration for Landscaper Project

This module provides integration with the Context Manager and Persona Manager MCPs
for enhanced AI agent capabilities in the landscaper web application.
"""

from .context_manager_client import ContextManagerClient
from .persona_manager_client import PersonaManagerClient
from .ai_agent import LandscaperAIAgent

__version__ = "1.0.0"
__all__ = ["ContextManagerClient", "PersonaManagerClient", "LandscaperAIAgent"]
