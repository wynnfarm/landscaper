"""
Landscaper - Mobile-First Web Application
A Flask-based web application designed specifically for mobile devices.
Integrated with Context Manager and Persona Manager MCPs for intelligent AI assistance.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Import MCP integration
from mcp_integration import LandscaperAIAgent

# Import landscaping materials calculator
from landscaping_materials import LandscapingMaterials

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'True').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize AI Agent with MCP integration
try:
    ai_agent = LandscaperAIAgent("landscaper")
    logger.info("AI Agent initialized successfully with MCP integration")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent: {e}")
    ai_agent = None

# Initialize Landscaping Materials Calculator
try:
    materials_calculator = LandscapingMaterials()
    logger.info("Landscaping Materials Calculator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Materials Calculator: {e}")
    materials_calculator = None

@app.route('/')
def index():
    """Home page - main landing page for mobile users."""
    return render_template('index.html')

@app.route('/services')
def services():
    """Services page - detailed information about landscaping services."""
    services_data = {
        'lawn_care': {
            'title': 'Lawn Care Services',
            'description': 'Professional lawn maintenance and care',
            'services': [
                'Regular mowing and edging',
                'Fertilization and soil treatment',
                'Weed control and prevention',
                'Aeration and overseeding',
                'Pest and disease management'
            ],
            'pricing': 'Starting at $50/month'
        },
        'tree_services': {
            'title': 'Tree Services',
            'description': 'Complete tree care and maintenance',
            'services': [
                'Tree pruning and trimming',
                'Tree removal and stump grinding',
                'Disease diagnosis and treatment',
                'Emergency tree services',
                'Tree planting and transplanting'
            ],
            'pricing': 'Starting at $75/tree'
        },
        'garden_design': {
            'title': 'Garden Design',
            'description': 'Custom landscape design and installation',
            'services': [
                'Landscape planning and design',
                'Plant selection and installation',
                'Hardscaping and patios',
                'Irrigation system installation',
                'Outdoor lighting design'
            ],
            'pricing': 'Starting at $500/project'
        },
        'cleanup': {
            'title': 'Cleanup Services',
            'description': 'Seasonal cleanup and maintenance',
            'services': [
                'Spring and fall cleanup',
                'Leaf removal and disposal',
                'Debris removal',
                'Mulching and bed preparation',
                'Gutter cleaning'
            ],
            'pricing': 'Starting at $100/visit'
        }
    }
    return render_template('services.html', services=services_data)

@app.route('/gallery')
def gallery():
    """Gallery page - showcase of completed landscaping projects."""
    gallery_data = {
        'before_after': [
            {
                'title': 'Residential Lawn Transformation',
                'description': 'Complete lawn renovation with new sod and irrigation',
                'before': '/static/images/before1.jpg',
                'after': '/static/images/after1.jpg'
            },
            {
                'title': 'Garden Design Project',
                'description': 'Custom garden design with native plants and hardscaping',
                'before': '/static/images/before2.jpg',
                'after': '/static/images/after2.jpg'
            }
        ],
        'featured_projects': [
            {
                'title': 'Modern Landscape Design',
                'description': 'Contemporary design with clean lines and minimal maintenance',
                'image': '/static/images/project1.jpg'
            },
            {
                'title': 'Traditional English Garden',
                'description': 'Classic English garden with perennial borders and pathways',
                'image': '/static/images/project2.jpg'
            },
            {
                'title': 'Drought-Tolerant Landscape',
                'description': 'Water-wise design with native and adapted plants',
                'image': '/static/images/project3.jpg'
            }
        ]
    }
    return render_template('gallery.html', gallery=gallery_data)

@app.route('/chat')
def chat():
    """AI Chat page - interactive AI assistant."""
    return render_template('chat.html')

@app.route('/calculator')
def calculator():
    """Wall Material Calculator page."""
    return render_template('calculator.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page - contact form and business information."""
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # Here you would typically save to database or send email
        # For now, we'll just return a success message
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your inquiry! We will contact you within 24 hours.'
        })
    
    contact_info = {
        'phone': '555-0123',
        'email': 'info@landscaper.com',
        'address': '123 Garden Street, Green City, GC 12345',
        'hours': {
            'monday_friday': '7:00 AM - 6:00 PM',
            'saturday': '8:00 AM - 4:00 PM',
            'sunday': 'Closed'
        },
        'services': [
            'Lawn Care',
            'Tree Services',
            'Garden Design',
            'Cleanup Services',
            'Emergency Services'
        ]
    }
    return render_template('contact.html', contact_info=contact_info)

@app.route('/quote', methods=['POST'])
def get_quote():
    """Handle quote request form submission."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'phone', 'service_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'{field.replace("_", " ").title()} is required'
            }), 400
    
    # Use AI agent to process the quote request
    if ai_agent:
        try:
            quote_query = f"Customer {data['name']} is requesting a quote for {data['service_type']}. Contact: {data['email']}, {data['phone']}"
            if data.get('message'):
                quote_query += f" Additional details: {data['message']}"
            
            ai_response = ai_agent.process_user_query(quote_query, {
                'request_type': 'quote',
                'customer_name': data['name'],
                'service_type': data['service_type']
            })
            
            # Add quote request to context manager
            ai_agent.add_current_issue(
                f"Quote request from {data['name']} for {data['service_type']}",
                location="quote_system",
                root_cause="customer_inquiry"
            )
            
            logger.info(f"Quote request processed by AI agent: {ai_response.get('persona', {}).get('name', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"AI agent error during quote processing: {e}")
    
    # Here you would typically:
    # 1. Save the quote request to database
    # 2. Send email notification
    # 3. Calculate estimated pricing
    
    return jsonify({
        'success': True,
        'message': 'Quote request received! We will contact you within 24 hours with a detailed estimate.',
        'quote_id': 'Q' + str(hash(data['email']))[:8].upper()
    })

@app.route('/api/chat', methods=['POST'])
def ai_chat():
    """AI chat endpoint using MCP integration."""
    if not ai_agent:
        return jsonify({
            'success': False,
            'error': 'AI agent not available'
        }), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_context = data.get('context', {})
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Process the user query with AI agent
        response = ai_agent.process_user_query(user_message, user_context)
        
        logger.info(f"AI chat processed: {response.get('persona', {}).get('name', 'Unknown')} persona used")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your message'
        }), 500

@app.route('/api/agent/status')
def agent_status():
    """Get AI agent status and statistics."""
    if not ai_agent:
        return jsonify({
            'success': False,
            'error': 'AI agent not available'
        }), 503
    
    try:
        status = ai_agent.get_agent_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Agent status error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get agent status'
        }), 500

@app.route('/api/agent/personas')
def list_personas():
    """List available AI personas."""
    if not ai_agent:
        return jsonify({
            'success': False,
            'error': 'AI agent not available'
        }), 503
    
    try:
        personas = ai_agent.persona_manager.list_personas()
        return jsonify({
            'success': True,
            'personas': personas
        })
    except Exception as e:
        logger.error(f"List personas error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to list personas'
        }), 500

@app.route('/api/context/summary')
def context_summary():
    """Get project context summary."""
    if not ai_agent:
        return jsonify({
            'success': False,
            'error': 'AI agent not available'
        }), 503
    
    try:
        summary = ai_agent.context_manager.get_context_summary()
        return jsonify({
            'success': True,
            'context': summary
        })
    except Exception as e:
        logger.error(f"Context summary error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get context summary'
        }), 500

@app.route('/api/services')
def api_services():
    """API endpoint for services data."""
    services = [
        {
            'id': 'lawn_care',
            'name': 'Lawn Care',
            'description': 'Regular maintenance and care for your lawn',
            'icon': '🌿',
            'price_range': '$50-200/month'
        },
        {
            'id': 'tree_services',
            'name': 'Tree Services',
            'description': 'Professional tree care and maintenance',
            'icon': '🌳',
            'price_range': '$75-500/tree'
        },
        {
            'id': 'garden_design',
            'name': 'Garden Design',
            'description': 'Custom landscape design and installation',
            'icon': '🌺',
            'price_range': '$500-5000/project'
        },
        {
            'id': 'cleanup',
            'name': 'Cleanup Services',
            'description': 'Seasonal cleanup and maintenance',
            'icon': '🧹',
            'price_range': '$100-300/visit'
        }
    ]
    return jsonify(services)

@app.route('/api/materials')
def api_materials():
    """API endpoint for materials data."""
    if not materials_calculator:
        return jsonify({
            'success': False,
            'error': 'Materials calculator not available'
        }), 503
    
    try:
        materials = materials_calculator.get_all_materials()
        materials_dict = {}
        
        for material in materials:
            # Convert material to dictionary format
            material_id = material.name.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
            materials_dict[material_id] = {
                'name': material.name,
                'type': material.material_type.value,
                'dimensions': f"{material.length}\" x {material.width}\" x {material.height}\"",
                'weight': material.weight,
                'price': material.price_per_unit,
                'description': material.description,
                'use_case': material.use_case,
                'installation_notes': material.installation_notes
            }
        
        return jsonify(materials_dict)
    except Exception as e:
        logger.error(f"Error getting materials: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get materials data'
        }), 500

@app.route('/api/calculate-materials', methods=['POST'])
def api_calculate_materials():
    """API endpoint for calculating wall materials."""
    if not materials_calculator:
        return jsonify({
            'success': False,
            'error': 'Materials calculator not available'
        }), 503
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['wall_length', 'wall_height', 'material_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Calculate materials
        result = materials_calculator.calculate_wall_materials(
            wall_length=float(data['wall_length']),
            wall_height=float(data['wall_height']),
            material_id=data['material_id'],
            include_base=data.get('include_base', True),
            include_cap=data.get('include_cap', True)
        )
        
        # Log the calculation for AI agent context
        if ai_agent:
            calculation_summary = f"Wall calculation: {data['wall_length']}' x {data['wall_height']}' using {data['material_id']}, estimated cost: ${result['total_estimated_cost']}"
            ai_agent.add_conversation_entry(
                role="system",
                content=calculation_summary,
                metadata={
                    "calculation_type": "wall_materials",
                    "wall_length": data['wall_length'],
                    "wall_height": data['wall_height'],
                    "material_id": data['material_id'],
                    "total_cost": result['total_estimated_cost']
                }
            )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error calculating materials: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to calculate materials'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with mobile-friendly page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with mobile-friendly page."""
    return render_template('500.html'), 500

# PWA Routes
@app.route('/manifest.json')
def manifest():
    """PWA manifest file."""
    return {
        "name": "Landscaper - Professional Landscaping",
        "short_name": "Landscaper",
        "description": "Professional landscaping services for your home and business",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#2c5530",
        "theme_color": "#2c5530",
        "icons": [
            {
                "src": "/static/images/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

@app.route('/sw.js')
def service_worker():
    """Service worker for PWA functionality."""
    return app.send_static_file('js/sw.js')

if __name__ == '__main__':
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
