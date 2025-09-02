# CONTEXT SWITCHING RULES - LANDSCAPER PROJECT

## Overview

This document defines rules and procedures for context switching in the Landscaper project to ensure proper context management and maintain project continuity.

## Context Types

### 1. Development Context

**When to switch:** When working on code development, debugging, or technical implementation
**Current Context:** landscaper
**Key Focus Areas:**

- Flask backend development
- React frontend development
- Database operations
- API endpoint implementation
- MCP integration

### 2. Testing Context

**When to switch:** When running tests, debugging, or validating functionality
**Context:** landscaper-test
**Key Focus Areas:**

- Unit testing
- Integration testing
- API testing
- Frontend testing
- Performance testing

### 3. Deployment Context

**When to switch:** When preparing for deployment, production setup, or infrastructure work
**Context:** landscaper-deploy
**Key Focus Areas:**

- Docker configuration
- Environment setup
- Production deployment
- Monitoring setup
- Security configuration

### 4. Documentation Context

**When to switch:** When creating or updating documentation
**Context:** landscaper-docs
**Key Focus Areas:**

- API documentation
- User guides
- Technical documentation
- README files
- Code comments

## Context Switching Rules

### Rule 1: Automatic Context Detection

- **Trigger:** User mentions specific task types or areas
- **Action:** Automatically switch to appropriate context
- **Examples:**
  - "test the API" → switch to testing context
  - "deploy to production" → switch to deployment context
  - "update documentation" → switch to documentation context

### Rule 2: Context Persistence

- **Trigger:** Context switch occurs
- **Action:** Save current state and load new context
- **Requirements:**
  - Save current progress
  - Update context status
  - Load relevant files and settings
  - Maintain conversation history

### Rule 3: Context Validation

- **Trigger:** Before executing commands or making changes
- **Action:** Verify correct context is active
- **Checks:**
  - Current project context matches task
  - Required files are accessible
  - Dependencies are available
  - Environment is properly configured

### Rule 4: Context Recovery

- **Trigger:** Error occurs or context becomes inconsistent
- **Action:** Restore context to last known good state
- **Steps:**
  - Load last saved context
  - Verify file integrity
  - Restore conversation state
  - Validate environment

### Rule 5: Cross-Context Communication

- **Trigger:** Task requires multiple contexts
- **Action:** Maintain context bridges
- **Requirements:**
  - Share relevant information between contexts
  - Maintain consistency across contexts
  - Track dependencies between contexts

## Context Management Commands

### Switch Context

```bash
# Switch to development context
mcp_context_set_current_goal "Development: [specific task]" --project landscaper

# Switch to testing context
mcp_context_set_current_goal "Testing: [specific test]" --project landscaper-test

# Switch to deployment context
mcp_context_set_current_goal "Deployment: [specific deployment]" --project landscaper-deploy
```

### Save Context State

```bash
# Save current context state
mcp_context_add_completed_feature "[completed task]" --project [current-context]

# Add current issue
mcp_context_add_current_issue "[issue description]" --project [current-context]
```

### Load Context State

```bash
# Get current context
mcp_context_get_project_context --project [context-name]
```

## Context-Specific Guidelines

### Development Context Guidelines

- Always check current goal before starting development
- Save progress frequently
- Update context with completed features
- Track any issues encountered

### Testing Context Guidelines

- Verify test environment is properly set up
- Run tests in isolation
- Document test results
- Update context with test outcomes

### Deployment Context Guidelines

- Verify all dependencies are available
- Check environment configuration
- Validate security settings
- Monitor deployment process

### Documentation Context Guidelines

- Ensure documentation is up-to-date
- Verify accuracy of technical details
- Include examples and usage instructions
- Maintain consistent formatting

## Emergency Context Recovery

### If Context Becomes Corrupted

1. **Stop all operations immediately**
2. **Load last known good context**
3. **Verify file integrity**
4. **Restore from backup if necessary**
5. **Validate environment**

### If Context Switching Fails

1. **Check MCP server status**
2. **Verify network connectivity**
3. **Restart context manager if needed**
4. **Load context manually**
5. **Update context status**

## Context Monitoring

### Health Checks

- **Frequency:** Every context switch
- **Checks:**
  - Context manager is running
  - Files are accessible
  - Dependencies are available
  - Environment is configured

### Performance Monitoring

- **Metrics:**
  - Context switch time
  - Context load time
  - Context save time
  - Error rates

## Implementation Notes

### Current Active Context

- **Project:** landscaper
- **Type:** Development
- **Status:** Active
- **Last Updated:** [Current timestamp]

### Context Dependencies

- **MCP Context Manager:** Required for context switching
- **MCP Persona Manager:** Required for persona selection
- **Flask Backend:** Required for API operations
- **React Frontend:** Required for UI operations
- **PostgreSQL Database:** Required for data operations

### Context File Locations

- **Context Status:** `landscaper/contexts/landscaper_CONTEXT_STATUS.md`
- **Context Cache:** `landscaper/contexts/landscaper_context_cache.json`
- **Context Rules:** `landscaper/CONTEXT_SWITCHING_RULES.md`

---

_Last updated: [Current timestamp]_
_Context Manager Version: 1.0_
