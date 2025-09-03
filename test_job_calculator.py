#!/usr/bin/env python3
"""
Simple test Flask app for job calculator
"""

from flask import Flask, jsonify
from flask_cors import CORS
from job_calculator import JobCalculator
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the job calculator
job_calculator = JobCalculator()

@app.route('/api/job-calculator/types', methods=['GET'])
def get_job_types():
    """Get available job types"""
    try:
        job_types = job_calculator.get_job_types()
        return jsonify({
            'success': True,
            'job_types': job_types,
            'descriptions': {
                'pavers': 'Paver installation with base layers',
                'walls': 'Wall construction with blocks and mortar',
                'stairs': 'Stair construction with treads and risers',
                'steps': 'Individual step installation'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/job-calculator/calculate', methods=['POST'])
def calculate_job():
    """Calculate job requirements"""
    try:
        from flask import request
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        job_type = data.get('job_type')
        measurements = data.get('measurements', {})
        
        if not job_type:
            return jsonify({'success': False, 'error': 'Job type required'}), 400
        
        # Calculate the job
        result = job_calculator.calculate_job(job_type, measurements)
        
        # Add metadata
        result['metadata'] = {
            'calculation_date': datetime.now().isoformat(),
            'job_type': job_type,
            'input_measurements': measurements
        }
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/job-calculator/templates', methods=['GET'])
def get_job_templates():
    """Get job calculation templates"""
    templates = {
        'pavers': {
            'name': 'Paver Installation',
            'description': 'Calculate materials needed for paver installation',
            'measurements': {
                'length_ft': {'type': 'number', 'label': 'Length (feet)', 'required': True},
                'length_in': {'type': 'number', 'label': 'Length (inches)', 'required': False},
                'width_ft': {'type': 'number', 'label': 'Width (feet)', 'required': True},
                'width_in': {'type': 'number', 'label': 'Width (inches)', 'required': False},
                'paver_height': {'type': 'number', 'label': 'Paver Height (inches)', 'default': 2.375},
                'fines_depth': {'type': 'number', 'label': 'Fines Depth (inches)', 'default': 2.375},
                'ca11_depth': {'type': 'number', 'label': 'CA11 Base Depth (inches)', 'default': 3.625}
            }
        },
        'walls': {
            'name': 'Wall Construction',
            'description': 'Calculate materials needed for wall construction',
            'measurements': {
                'length_ft': {'type': 'number', 'label': 'Length (feet)', 'required': True},
                'length_in': {'type': 'number', 'label': 'Length (inches)', 'required': False},
                'height_ft': {'type': 'number', 'label': 'Height (feet)', 'required': True},
                'height_in': {'type': 'number', 'label': 'Height (inches)', 'required': False},
                'width_ft': {'type': 'number', 'label': 'Width (feet)', 'required': False},
                'width_in': {'type': 'number', 'label': 'Width (inches)', 'required': False},
                'block_type': {'type': 'select', 'label': 'Block Type', 'options': ['Standard Concrete Block', 'Decorative Block', 'Retaining Wall Block']}
            }
        },
        'stairs': {
            'name': 'Stair Construction',
            'description': 'Calculate materials needed for stair construction',
            'measurements': {
                'total_rise_ft': {'type': 'number', 'label': 'Total Rise (feet)', 'required': True},
                'total_rise_in': {'type': 'number', 'label': 'Total Rise (inches)', 'required': False},
                'total_run_ft': {'type': 'number', 'label': 'Total Run (feet)', 'required': True},
                'total_run_in': {'type': 'number', 'label': 'Total Run (inches)', 'required': False},
                'step_count': {'type': 'number', 'label': 'Number of Steps (optional)', 'required': False},
                'tread_width': {'type': 'number', 'label': 'Tread Width (inches)', 'default': 36}
            }
        },
        'steps': {
            'name': 'Step Installation',
            'description': 'Calculate materials needed for individual step',
            'measurements': {
                'rise_ft': {'type': 'number', 'label': 'Rise (feet)', 'required': True},
                'rise_in': {'type': 'number', 'label': 'Rise (inches)', 'required': False},
                'run_ft': {'type': 'number', 'label': 'Run (feet)', 'required': True},
                'run_in': {'type': 'number', 'label': 'Run (inches)', 'required': False},
                'width_ft': {'type': 'number', 'label': 'Width (feet)', 'required': True},
                'width_in': {'type': 'number', 'label': 'Width (inches)', 'required': False},
                'tread_material': {'type': 'select', 'label': 'Tread Material', 'options': ['Stone', 'Concrete', 'Brick']},
                'riser_material': {'type': 'select', 'label': 'Riser Material', 'options': ['Stone', 'Concrete', 'Brick']}
            }
        }
    }
    
    return jsonify({
        'success': True,
        'templates': templates
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Job Calculator API is running!',
        'endpoints': [
            '/api/job-calculator/types',
            '/api/job-calculator/templates',
            '/api/job-calculator/calculate'
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Job Calculator API...")
    print("📊 Available endpoints:")
    print("   - GET  /api/job-calculator/types")
    print("   - GET  /api/job-calculator/templates")
    print("   - POST /api/job-calculator/calculate")
    print("🌐 Server will be available at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
