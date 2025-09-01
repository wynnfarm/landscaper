#!/usr/bin/env python3
"""
MCP CLI Tool for Landscaper Project

This CLI tool provides commands for managing the Context Manager and Persona Manager
MCPs integrated with the landscaper project.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_integration import LandscaperAIAgent, ContextManagerClient, PersonaManagerClient


def main():
    parser = argparse.ArgumentParser(description='MCP CLI Tool for Landscaper Project')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Context Manager commands
    context_parser = subparsers.add_parser('context', help='Context Manager operations')
    context_subparsers = context_parser.add_subparsers(dest='context_action', help='Context actions')
    
    # Context status
    context_subparsers.add_parser('status', help='Show context status')
    
    # Context goal
    goal_parser = context_subparsers.add_parser('goal', help='Set or get current goal')
    goal_parser.add_argument('goal_text', nargs='?', help='New goal text')
    
    # Context feature
    feature_parser = context_subparsers.add_parser('feature', help='Add completed feature')
    feature_parser.add_argument('feature_text', help='Completed feature description')
    
    # Context issue
    issue_parser = context_subparsers.add_parser('issue', help='Add current issue')
    issue_parser.add_argument('issue_text', help='Issue description')
    issue_parser.add_argument('--location', help='Issue location')
    issue_parser.add_argument('--cause', help='Root cause')
    
    # Context next
    next_parser = context_subparsers.add_parser('next', help='Add next step')
    next_parser.add_argument('step_text', help='Next step description')
    
    # Persona Manager commands
    persona_parser = subparsers.add_parser('persona', help='Persona Manager operations')
    persona_subparsers = persona_parser.add_subparsers(dest='persona_action', help='Persona actions')
    
    # List personas
    persona_subparsers.add_parser('list', help='List all personas')
    
    # Get persona
    get_parser = persona_subparsers.add_parser('get', help='Get specific persona')
    get_parser.add_argument('persona_id', help='Persona ID')
    
    # Create persona
    create_parser = persona_subparsers.add_parser('create', help='Create new persona')
    create_parser.add_argument('--name', required=True, help='Persona name')
    create_parser.add_argument('--description', required=True, help='Persona description')
    create_parser.add_argument('--expertise', nargs='+', help='Areas of expertise')
    create_parser.add_argument('--style', help='Communication style')
    create_parser.add_argument('--context', help='Usage context')
    
    # Search personas
    search_parser = persona_subparsers.add_parser('search', help='Search personas')
    search_parser.add_argument('query', help='Search query')
    
    # Select best persona
    select_parser = persona_subparsers.add_parser('select', help='Select best persona for task')
    select_parser.add_argument('task', help='Task description')
    
    # AI Agent commands
    agent_parser = subparsers.add_parser('agent', help='AI Agent operations')
    agent_subparsers = agent_parser.add_subparsers(dest='agent_action', help='Agent actions')
    
    # Agent status
    agent_subparsers.add_parser('status', help='Show agent status')
    
    # Agent chat
    chat_parser = agent_subparsers.add_parser('chat', help='Chat with AI agent')
    chat_parser.add_argument('message', help='Message to send to agent')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test MCP integration')
    test_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'context':
            handle_context_command(args)
        elif args.command == 'persona':
            handle_persona_command(args)
        elif args.command == 'agent':
            handle_agent_command(args)
        elif args.command == 'test':
            handle_test_command(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def handle_context_command(args):
    """Handle context manager commands."""
    context_manager = ContextManagerClient("landscaper")
    
    if args.context_action == 'status':
        summary = context_manager.get_context_summary()
        print("📋 Context Status:")
        print(f"  Project: {summary['project_name']}")
        print(f"  Current Goal: {summary['current_goal']}")
        print(f"  Development Phase: {summary['development_phase']}")
        print(f"  Completed Features: {summary['completed_features_count']}")
        print(f"  Current Issues: {summary['current_issues_count']}")
        print(f"  Next Steps: {summary['next_steps_count']}")
        print(f"  Last Updated: {summary['last_updated']}")
        
    elif args.context_action == 'goal':
        if args.goal_text:
            success = context_manager.set_current_goal(args.goal_text)
            if success:
                print(f"✅ Goal set: {args.goal_text}")
            else:
                print("❌ Failed to set goal")
        else:
            summary = context_manager.get_context_summary()
            print(f"Current goal: {summary['current_goal']}")
            
    elif args.context_action == 'feature':
        success = context_manager.add_completed_feature(args.feature_text)
        if success:
            print(f"✅ Added completed feature: {args.feature_text}")
        else:
            print("❌ Failed to add feature")
            
    elif args.context_action == 'issue':
        success = context_manager.add_current_issue(
            args.issue_text,
            location=args.location or "",
            root_cause=args.cause or ""
        )
        if success:
            print(f"✅ Added issue: {args.issue_text}")
        else:
            print("❌ Failed to add issue")
            
    elif args.context_action == 'next':
        success = context_manager.add_next_step(args.step_text)
        if success:
            print(f"✅ Added next step: {args.step_text}")
        else:
            print("❌ Failed to add next step")


def handle_persona_command(args):
    """Handle persona manager commands."""
    persona_manager = PersonaManagerClient()
    
    if args.persona_action == 'list':
        personas = persona_manager.list_personas()
        print("🎭 Available Personas:")
        for persona in personas:
            print(f"  {persona['id']}: {persona['name']}")
            print(f"    Description: {persona['description']}")
            print(f"    Expertise: {', '.join(persona.get('expertise', []))}")
            print()
            
    elif args.persona_action == 'get':
        persona = persona_manager.get_persona(args.persona_id)
        if persona:
            print(f"🎭 Persona: {persona['name']}")
            print(f"  ID: {persona['id']}")
            print(f"  Description: {persona['description']}")
            print(f"  Expertise: {', '.join(persona.get('expertise', []))}")
            print(f"  Communication Style: {persona.get('communication_style', 'N/A')}")
            print(f"  Context: {persona.get('context', 'N/A')}")
            print(f"  Usage Count: {persona.get('usage_count', 0)}")
        else:
            print(f"❌ Persona not found: {args.persona_id}")
            
    elif args.persona_action == 'create':
        persona_data = {
            'name': args.name,
            'description': args.description,
            'expertise': args.expertise or [],
            'communication_style': args.style or 'Professional',
            'context': args.context or 'General assistance'
        }
        success = persona_manager.create_persona(persona_data)
        if success:
            print(f"✅ Created persona: {args.name}")
        else:
            print("❌ Failed to create persona")
            
    elif args.persona_action == 'search':
        results = persona_manager.search_personas(args.query)
        print(f"🔍 Search results for '{args.query}':")
        for persona in results:
            print(f"  {persona['id']}: {persona['name']}")
            
    elif args.persona_action == 'select':
        persona, confidence = persona_manager.select_best_persona(args.task)
        if persona:
            print(f"🎯 Best persona for '{args.task}':")
            print(f"  Persona: {persona['name']}")
            print(f"  Confidence: {confidence:.2f}")
            print(f"  Description: {persona['description']}")
        else:
            print("❌ No suitable persona found")


def handle_agent_command(args):
    """Handle AI agent commands."""
    agent = LandscaperAIAgent("landscaper")
    
    if args.agent_action == 'status':
        status = agent.get_agent_status()
        print("🤖 AI Agent Status:")
        print(f"  Session ID: {status['session_id']}")
        print(f"  Current Persona: {status['current_persona']}")
        print(f"  Agent Status: {status['agent_status']}")
        print(f"  Project Context: {status['project_context']['current_goal']}")
        print(f"  Persona Statistics: {status['persona_statistics']}")
        
    elif args.agent_action == 'chat':
        response = agent.process_user_query(args.message)
        if response['success']:
            print(f"🤖 {response['persona']['name']} (Confidence: {response['persona']['confidence']:.2f}):")
            print(f"  {response['response']}")
        else:
            print(f"❌ Error: {response.get('error', 'Unknown error')}")


def handle_test_command(args):
    """Test MCP integration."""
    print("🧪 Testing MCP Integration...")
    
    # Test Context Manager
    print("\n📋 Testing Context Manager...")
    try:
        context_manager = ContextManagerClient("landscaper")
        summary = context_manager.get_context_summary()
        print(f"  ✅ Context Manager: {summary['project_name']} - {summary['current_goal']}")
    except Exception as e:
        print(f"  ❌ Context Manager Error: {e}")
    
    # Test Persona Manager
    print("\n🎭 Testing Persona Manager...")
    try:
        persona_manager = PersonaManagerClient()
        personas = persona_manager.list_personas()
        print(f"  ✅ Persona Manager: {len(personas)} personas available")
        if args.verbose:
            for persona in personas:
                print(f"    - {persona['name']}")
    except Exception as e:
        print(f"  ❌ Persona Manager Error: {e}")
    
    # Test AI Agent
    print("\n🤖 Testing AI Agent...")
    try:
        agent = LandscaperAIAgent("landscaper")
        test_response = agent.process_user_query("Hello, what services do you offer?")
        if test_response['success']:
            print(f"  ✅ AI Agent: {test_response['persona']['name']} responded")
            if args.verbose:
                print(f"    Response: {test_response['response'][:100]}...")
        else:
            print(f"  ❌ AI Agent Error: {test_response.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"  ❌ AI Agent Error: {e}")
    
    print("\n🎉 MCP Integration Test Complete!")


if __name__ == '__main__':
    main()
