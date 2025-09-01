# MCP Integration Guide for Landscaper Project

This guide explains how the Context Manager and Persona Manager MCPs are integrated into the Landscaper mobile-first web application.

## 🎯 Overview

The Landscaper project now includes intelligent AI assistance powered by two MCPs:

1. **Context Manager MCP**: Maintains project context, tracks goals, and manages conversation state
2. **Persona Manager MCP**: Provides intelligent persona selection for different types of customer interactions

## 🏗️ Architecture

```
landscaper/
├── mcp_integration/           # MCP integration modules
│   ├── __init__.py           # Package initialization
│   ├── context_manager_client.py  # Context Manager MCP client
│   ├── persona_manager_client.py  # Persona Manager MCP client
│   └── ai_agent.py           # Main AI agent using both MCPs
├── mcp_config.json           # MCP configuration
├── mcp_cli.py               # CLI tool for MCP management
├── personas/                # Persona storage
│   └── landscaper_personas.json
├── contexts/                # Context storage
│   ├── landscaper_context_cache.json
│   └── landscaper_CONTEXT_STATUS.md
└── app.py                   # Flask app with MCP integration
```

## 🤖 AI Agent Features

### Intelligent Persona Selection

The AI agent automatically selects the most appropriate persona based on the user's query:

- **Customer Service Representative**: General inquiries, scheduling, support
- **Landscaping Expert**: Technical advice, plant care, design questions
- **Sales Specialist**: Pricing, quotes, service packages
- **Technical Support**: Website/app issues, navigation help
- **Emergency Responder**: Urgent situations, storm damage, safety concerns

### Context-Aware Responses

The agent maintains context across conversations and provides:

- Project-specific information
- Consistent service recommendations
- Personalized responses based on user needs
- Conversation history tracking

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize MCP Integration

```bash
# Test the MCP integration
python mcp_cli.py test

# Check context status
python mcp_cli.py context status

# List available personas
python mcp_cli.py persona list
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access AI Chat

Navigate to `http://localhost:5000/chat` to interact with the AI agent.

## 🛠️ CLI Commands

### Context Manager Commands

```bash
# Show current context status
python mcp_cli.py context status

# Set current goal
python mcp_cli.py context goal "Deploy to production"

# Add completed feature
python mcp_cli.py context feature "AI chat integration"

# Add current issue
python mcp_cli.py context issue "Database connection timeout" --location "app.py" --cause "Network latency"

# Add next step
python mcp_cli.py context next "Implement error handling"
```

### Persona Manager Commands

```bash
# List all personas
python mcp_cli.py persona list

# Get specific persona
python mcp_cli.py persona get customer_service_rep

# Search personas
python mcp_cli.py persona search "technical"

# Select best persona for task
python mcp_cli.py persona select "Customer needs help with plant care"

# Create new persona
python mcp_cli.py persona create --name "Garden Consultant" --description "Expert in garden design" --expertise "Design" "Plants" "Seasonal Care"
```

### AI Agent Commands

```bash
# Show agent status
python mcp_cli.py agent status

# Chat with agent
python mcp_cli.py agent chat "What services do you offer?"
```

## 📡 API Endpoints

### AI Chat API

```bash
POST /api/chat
Content-Type: application/json

{
  "message": "I need help with my lawn",
  "context": {
    "page": "services",
    "user_type": "customer"
  }
}
```

Response:

```json
{
  "success": true,
  "response": "I'd be happy to help you with your lawn care needs!...",
  "persona": {
    "id": "landscaping_expert",
    "name": "Landscaping Expert",
    "confidence": 0.85
  },
  "metadata": {
    "session_id": "20240101_120000",
    "timestamp": "2024-01-01T12:00:00Z",
    "query_type": "technical",
    "response_type": "expert_advice"
  }
}
```

### Agent Status API

```bash
GET /api/agent/status
```

### Context Summary API

```bash
GET /api/context/summary
```

### Personas API

```bash
GET /api/agent/personas
```

## 🎭 Available Personas

### 1. Customer Service Representative

- **Use Case**: General inquiries, scheduling, support
- **Expertise**: Customer Service, Landscaping Services, Appointment Scheduling
- **Style**: Warm, professional, and helpful

### 2. Landscaping Expert

- **Use Case**: Technical questions, plant care, design advice
- **Expertise**: Landscape Design, Plant Selection, Garden Maintenance
- **Style**: Knowledgeable, detailed, and educational

### 3. Sales Specialist

- **Use Case**: Pricing, quotes, service packages
- **Expertise**: Sales, Project Proposals, Cost Estimation
- **Style**: Persuasive, consultative, and results-oriented

### 4. Technical Support

- **Use Case**: Website/app issues, navigation help
- **Expertise**: Technical Support, Website Navigation, Troubleshooting
- **Style**: Clear, step-by-step, and patient

### 5. Emergency Responder

- **Use Case**: Urgent situations, storm damage, safety concerns
- **Expertise**: Emergency Response, Storm Damage, Safety Assessment
- **Style**: Urgent, reassuring, and action-oriented

## 🔧 Configuration

### MCP Configuration (`mcp_config.json`)

```json
{
  "mcp_servers": {
    "context_manager": {
      "enabled": true,
      "config": {
        "project_name": "landscaper",
        "auto_save": true,
        "conversation_history_limit": 50
      }
    },
    "persona_manager": {
      "enabled": true,
      "config": {
        "personas_dir": "./personas",
        "confidence_threshold": 0.3,
        "usage_tracking": true
      }
    }
  },
  "ai_agent": {
    "enabled": true,
    "config": {
      "default_persona": "customer_service_rep",
      "fallback_persona": "customer_service_rep",
      "response_timeout": 30,
      "max_response_length": 2000
    }
  }
}
```

## 📊 Monitoring and Analytics

### Context Tracking

- Project goals and progress
- Completed features
- Current issues and resolutions
- Next steps and planning

### Persona Analytics

- Usage statistics per persona
- Confidence scores for selections
- Performance metrics
- User interaction patterns

### Conversation History

- Session tracking
- Query classification
- Response effectiveness
- User satisfaction indicators

## 🚨 Troubleshooting

### Common Issues

1. **AI Agent Not Available**

   ```bash
   # Check if MCP integration is working
   python mcp_cli.py test
   ```

2. **Persona Selection Issues**

   ```bash
   # Check available personas
   python mcp_cli.py persona list

   # Test persona selection
   python mcp_cli.py persona select "test query"
   ```

3. **Context Not Saving**

   ```bash
   # Check context status
   python mcp_cli.py context status

   # Verify file permissions
   ls -la contexts/
   ```

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export DEBUG=True
python app.py
```

## 🔮 Future Enhancements

### Planned Features

- [ ] Database integration for persistent storage
- [ ] Advanced analytics dashboard
- [ ] Custom persona creation via web interface
- [ ] Multi-language support
- [ ] Voice interaction capabilities
- [ ] Integration with external CRM systems

### Extensibility

- Add new personas for specific use cases
- Customize response templates
- Integrate with external APIs
- Add machine learning for improved persona selection

## 📚 Additional Resources

- [Context Manager Documentation](../context_manager/README.md)
- [Persona Manager Documentation](../persona-manager-mcp/README.md)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 🤝 Contributing

To contribute to the MCP integration:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python mcp_cli.py test`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
