#!/usr/bin/env python3
"""
Automatic Context Switching Integration
Integrates with the MCP Context Manager to automatically switch contexts based on user input.
"""

import sys
import os
from pathlib import Path
from context_switcher import ContextSwitcher

def auto_switch_context(user_input: str, project_name: str = "landscaper"):
    """
    Automatically switch context based on user input and update MCP context manager
    """
    switcher = ContextSwitcher()
    
    # Detect context type from user input
    context_type = switcher.detect_context_type(user_input)
    
    # Switch to the detected context
    status = switcher.switch_context(context_type, user_input)
    
    print(f"🤖 **Auto Context Switch Detected**")
    print(f"📋 **Input:** {user_input}")
    print(f"🔄 **Switched to:** {context_type} context")
    print(f"📁 **Project:** {status['project']}")
    print(f"📝 **Task:** {status['task']}")
    
    # Here you would integrate with MCP Context Manager
    # For now, we'll just print the status
    print(f"✅ **Context switch completed successfully**")
    
    return status

def get_context_guidelines(context_type: str) -> str:
    """Get guidelines for the specified context type"""
    guidelines = {
        "development": """
        🛠️ **Development Context Guidelines:**
        - Always check current goal before starting development
        - Save progress frequently
        - Update context with completed features
        - Track any issues encountered
        - Follow coding standards and best practices
        """,
        "testing": """
        🧪 **Testing Context Guidelines:**
        - Verify test environment is properly set up
        - Run tests in isolation
        - Document test results
        - Update context with test outcomes
        - Ensure test coverage is adequate
        """,
        "deployment": """
        🚀 **Deployment Context Guidelines:**
        - Verify all dependencies are available
        - Check environment configuration
        - Validate security settings
        - Monitor deployment process
        - Test in staging environment first
        """,
        "documentation": """
        📚 **Documentation Context Guidelines:**
        - Ensure documentation is up-to-date
        - Verify accuracy of technical details
        - Include examples and usage instructions
        - Maintain consistent formatting
        - Review and update regularly
        """
    }
    
    return guidelines.get(context_type, "No specific guidelines available for this context type.")

def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python auto_context_switch.py <user_input>")
        print("Example: python auto_context_switch.py 'test the API endpoints'")
        return
    
    user_input = " ".join(sys.argv[1:])
    
    try:
        status = auto_switch_context(user_input)
        print("\n" + get_context_guidelines(status['type']))
        
    except Exception as e:
        print(f"❌ Error during context switch: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
