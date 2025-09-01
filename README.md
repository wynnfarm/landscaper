# Landscaper - Mobile-First Web Application

A modern, mobile-first web application for landscaping services, built with Flask and optimized for mobile devices.

## Features

- 📱 **Mobile-First Design**: Optimized for smartphones and tablets
- 🌿 **Landscaping Services**: Complete service catalog and booking system
- 📞 **Contact Integration**: Direct calling, email, and location services
- 🎨 **Modern UI**: Clean, responsive design with touch-friendly interface
- ⚡ **PWA Ready**: Progressive Web App capabilities for app-like experience
- 🔄 **Offline Support**: Service worker for offline functionality
- 🤖 **AI Assistant**: Intelligent AI agent with Context Manager and Persona Manager MCPs
- 🎭 **Smart Personas**: 5 specialized AI personas for different customer needs
- 📋 **Context Tracking**: Maintains conversation context and project state
- 🛠️ **MCP Integration**: Full integration with Model Context Protocol
- 🧮 **Material Calculator**: Comprehensive wall material calculator with visual representation
- 💰 **Cost Estimation**: Real-time material cost calculations and project estimates
- 🏗️ **Visual Wall Builder**: Interactive wall visualization and design tool

## Project Structure

```
landscaper/
├── app.py                 # Main Flask application with MCP integration
├── requirements.txt       # Python dependencies
├── mcp_config.json       # MCP configuration
├── mcp_cli.py           # CLI tool for MCP management
├── landscaping_materials.py # Material calculator and database
├── test_calculator.py    # Calculator test suite
├── mcp_integration/     # MCP integration modules
│   ├── __init__.py
│   ├── context_manager_client.py
│   ├── persona_manager_client.py
│   └── ai_agent.py
├── static/               # Static assets
│   ├── css/
│   │   └── mobile.css    # Mobile-first CSS framework
│   ├── js/
│   │   └── app.js        # Mobile JavaScript functionality
│   └── images/           # Images and icons
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── chat.html         # AI chat interface
│   └── calculator.html   # Material calculator interface
├── personas/             # AI persona storage
│   └── landscaper_personas.json
├── contexts/             # Context storage
│   ├── landscaper_context_cache.json
│   └── landscaper_CONTEXT_STATUS.md
├── src/                  # Source code (for future expansion)
└── tests/                # Test files
```

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd landscaper
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Test MCP Integration**

   ```bash
   # Test the MCP integration
   python mcp_cli.py test
   
   # Check context status
   python mcp_cli.py context status
   
   # List available AI personas
   python mcp_cli.py persona list
   
   # Test the material calculator
   python test_calculator.py
   ```

6. **Access the application**
   - Open your mobile browser and navigate to `http://localhost:5000`
   - Or use your computer's browser and resize to mobile view
   - Try the AI chat at `http://localhost:5000/chat`
   - Use the material calculator at `http://localhost:5000/calculator`

## Mobile Features

### Touch Gestures

- **Swipe Navigation**: Swipe left/right to navigate between sections
- **Touch Targets**: All buttons and links are optimized for finger navigation
- **Responsive Design**: Adapts to different screen sizes and orientations

### Native Integration

- **Phone Calls**: Tap phone numbers to call directly
- **Email**: Tap email addresses to open email client
- **Maps**: Tap addresses to open in maps application
- **Share**: Share the app using native sharing capabilities

### Performance

- **Fast Loading**: Optimized CSS and JavaScript for mobile networks
- **Offline Support**: Basic functionality works without internet connection
- **PWA Features**: Can be installed as a home screen app

### AI Assistant Features

- **Intelligent Personas**: 5 specialized AI personas for different customer needs
- **Context Awareness**: Maintains conversation context and project state
- **Smart Selection**: Automatically selects the best persona for each query
- **Real-time Chat**: Interactive AI chat interface optimized for mobile
- **Service Integration**: AI responses integrated with business services and pricing

### Material Calculator Features

- **Comprehensive Database**: 12+ different landscaping materials with specifications
- **Wall Height Calculation**: Determines exact quantities based on wall dimensions
- **Cost Estimation**: Real-time pricing for materials and installation
- **Visual Representation**: Interactive wall diagram showing block layout
- **Multiple Material Types**: Retaining walls, pavers, stone, concrete, brick, timber, gabion
- **Base & Cap Materials**: Includes foundation and finishing materials
- **Installation Notes**: Professional guidance for each material type

## Development

### Running in Development Mode

```bash
export DEBUG=True
python app.py
```

### Environment Variables

- `DEBUG`: Set to `True` for development mode
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Port number (default: 5000)

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Test MCP integration
python mcp_cli.py test --verbose

# Test AI agent
python mcp_cli.py agent chat "Hello, what services do you offer?"
```

## Deployment

### Local Production

```bash
export DEBUG=False
export SECRET_KEY=your-secret-key
python app.py
```

### Docker Deployment

```bash
# Build image
docker build -t landscaper .

# Run container
docker run -p 5000:5000 landscaper
```

## Browser Support

- **Mobile Browsers**: iOS Safari, Chrome Mobile, Firefox Mobile
- **Desktop Browsers**: Chrome, Firefox, Safari, Edge (with mobile view)
- **PWA Support**: Modern browsers with service worker support

## MCP Integration

This project includes comprehensive integration with the Context Manager and Persona Manager MCPs:

- **Context Manager**: Tracks project goals, completed features, current issues, and conversation history
- **Persona Manager**: Provides 5 specialized AI personas for different customer interaction types
- **AI Agent**: Intelligent agent that automatically selects the best persona for each query
- **CLI Tools**: Command-line interface for managing MCP services
- **API Endpoints**: RESTful APIs for AI chat, agent status, and context management

For detailed MCP integration documentation, see [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md).

## Material Calculator

The application includes a comprehensive material calculator for landscaping wall construction:

### Overview
- **Material Database**: 12+ different landscaping materials with specifications
- **Wall Calculator**: Determines exact quantities based on wall dimensions
- **Cost Estimation**: Real-time pricing for materials and installation
- **Visual Builder**: Interactive wall diagram showing block layout

### Supported Materials
- **Retaining Wall Blocks**: Versa-Lok, Allan Block, Keystone
- **Pavers**: Concrete pavers in various sizes
- **Natural Stone**: Fieldstone, limestone blocks
- **Concrete Blocks**: Standard concrete blocks
- **Brick**: Standard clay bricks
- **Landscape Timber**: Pressure-treated timbers
- **Gabion Baskets**: Wire baskets for stone fill

For detailed material information and usage guide, see [LANDSCAPING_MATERIALS_GUIDE.md](LANDSCAPING_MATERIALS_GUIDE.md).

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
