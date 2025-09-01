"""
Landscaper - Mobile-First Web Application
A Flask-based web application designed specifically for mobile devices.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'True').lower() == 'true'

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
    
    # Here you would typically:
    # 1. Save the quote request to database
    # 2. Send email notification
    # 3. Calculate estimated pricing
    
    return jsonify({
        'success': True,
        'message': 'Quote request received! We will contact you within 24 hours with a detailed estimate.',
        'quote_id': 'Q' + str(hash(data['email']))[:8].upper()
    })

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
