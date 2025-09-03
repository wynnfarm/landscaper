#!/usr/bin/env python3
"""
Simplified Flask app with job calculator integration
No database dependencies - just the job calculator functionality
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
import os
import uuid
from datetime import datetime, date

# Import job calculator
from job_calculator_api import create_job_calculator_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Add job calculator routes
create_job_calculator_routes(app)

# Simple in-memory data storage (no database required)
materials_data = [
    {
        "id": "1",
        "name": "Concrete Pavers",
        "material_type": "concrete",
        "description": "Standard concrete pavers",
        "unit": "piece",
        "cost_per_unit": 2.50,
        "is_active": True
    },
    {
        "id": "2", 
        "name": "Natural Stone",
        "material_type": "stone",
        "description": "Natural stone pavers",
        "unit": "sqft",
        "cost_per_unit": 15.00,
        "is_active": True
    },
    {
        "id": "3",
        "name": "CA11 Base",
        "material_type": "gravel",
        "description": "Crushed aggregate base material",
        "unit": "cuyd",
        "cost_per_unit": 35.00,
        "is_active": True
    }
]

equipment_data = [
    {
        "id": "1",
        "name": "Skid Steer",
        "equipment_type": "heavy_equipment",
        "description": "Bobcat skid steer loader",
        "status": "available",
        "daily_rate": 250.00,
        "is_active": True
    },
    {
        "id": "2",
        "name": "Plate Compactor",
        "equipment_type": "compaction",
        "description": "Vibratory plate compactor",
        "status": "available", 
        "daily_rate": 75.00,
        "is_active": True
    }
]

crew_data = [
    {
        "id": "1",
        "name": "John Smith",
        "role": "foreman",
        "phone": "555-0101",
        "email": "john@landscaper.com",
        "hourly_rate": 25.00,
        "is_active": True
    },
    {
        "id": "2",
        "name": "Mike Johnson",
        "role": "laborer",
        "phone": "555-0102", 
        "email": "mike@landscaper.com",
        "hourly_rate": 18.00,
        "is_active": True
    }
]

projects_data = [
    {
        "id": "1",
        "name": "Downtown Patio",
        "description": "Commercial patio installation",
        "status": "in_progress",
        "budget": 15000.00,
        "start_date": "2024-08-01",
        "is_active": True
    },
    {
        "id": "2",
        "name": "Residential Wall",
        "description": "Retaining wall construction",
        "status": "planning",
        "budget": 8000.00,
        "start_date": "2024-09-15",
        "is_active": True
    }
]

# Jobs data - new structure for project-job relationship
jobs_data = [
    {
        "id": "1",
        "project_id": "1",
        "name": "Main Patio Area",
        "job_type": "pavers",
        "description": "Primary patio installation with concrete pavers",
        "status": "in_progress",
        "measurements": {
            "length_ft": 20,
            "length_in": 0,
            "width_ft": 15,
            "width_in": 0,
            "ca11_depth": 3.625,
            "fines_depth": 2.375
        },
        "calculation_result": {
            "area_sqft": 300.0,
            "total_depth_inches": 6.0,
            "materials": {
                "CA11": {"quantity": 3.7, "unit": "cubic yards"},
                "Fines": {"quantity": 2.3, "unit": "cubic yards"},
                "Pavers": {"quantity": 300, "unit": "square feet"}
            },
            "layers": [
                {"name": "CA11 Base", "material": "CA11", "depth": 3.625},
                {"name": "Fines", "material": "Fines", "depth": 2.375}
            ],
            "calculations": {
                "total_volume_cubic_yards": 6.0,
                "total_weight_tons": 8.1
            }
        },
        "created_at": "2024-08-01T10:00:00Z",
        "updated_at": "2024-08-01T10:00:00Z",
        "is_active": True
    },
    {
        "id": "2",
        "project_id": "1",
        "name": "Walkway Extension",
        "job_type": "pavers",
        "description": "Additional walkway connecting to patio",
        "status": "planned",
        "measurements": {
            "length_ft": 12,
            "length_in": 0,
            "width_ft": 4,
            "width_in": 0,
            "ca11_depth": 3.625,
            "fines_depth": 2.375
        },
        "calculation_result": {
            "area_sqft": 48.0,
            "total_depth_inches": 6.0,
            "materials": {
                "CA11": {"quantity": 0.6, "unit": "cubic yards"},
                "Fines": {"quantity": 0.4, "unit": "cubic yards"},
                "Pavers": {"quantity": 48, "unit": "square feet"}
            },
            "layers": [
                {"name": "CA11 Base", "material": "CA11", "depth": 3.625},
                {"name": "Fines", "material": "Fines", "depth": 2.375}
            ],
            "calculations": {
                "total_volume_cubic_yards": 1.0,
                "total_weight_tons": 1.3
            }
        },
        "created_at": "2024-08-01T11:00:00Z",
        "updated_at": "2024-08-01T11:00:00Z",
        "is_active": True
    },
    {
        "id": "3",
        "project_id": "2",
        "name": "Retaining Wall",
        "job_type": "walls",
        "description": "Main retaining wall structure",
        "status": "planned",
        "measurements": {
            "length_ft": 25,
            "length_in": 0,
            "height_ft": 4,
            "height_in": 0,
            "depth_ft": 1,
            "depth_in": 6
        },
        "calculation_result": {
            "area_sqft": 100.0,
            "total_depth_inches": 18.0,
            "materials": {
                "Blocks": {"quantity": 200, "unit": "blocks"},
                "Mortar": {"quantity": 0.8, "unit": "cubic yards"},
                "Backfill": {"quantity": 5.6, "unit": "cubic yards"}
            },
            "layers": [
                {"name": "Wall Blocks", "material": "Blocks", "depth": 18.0}
            ],
            "calculations": {
                "total_volume_cubic_yards": 6.4,
                "total_weight_tons": 8.6
            }
        },
        "created_at": "2024-09-15T09:00:00Z",
        "updated_at": "2024-09-15T09:00:00Z",
        "is_active": True
    }
]

# API Routes
@app.route('/api/materials')
def get_materials():
    """Get all materials."""
    try:
        return jsonify([m for m in materials_data if m['is_active']])
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        return jsonify({'error': 'Failed to fetch materials'}), 500

@app.route('/api/materials/types')
def get_material_types():
    """Get available material types for the calculator."""
    try:
        material_types = list(set(m['material_type'] for m in materials_data))
        
        material_type_mapping = {
            "concrete": "Concrete",
            "stone": "Natural Stone", 
            "brick": "Brick",
            "block": "Block",
            "wood": "Wood",
            "metal": "Metal",
            "gravel": "Gravel",
            "other": "Other"
        }
        
        formatted_types = [
            {
                "value": material_type,
                "label": material_type_mapping.get(material_type, material_type.title())
            }
            for material_type in material_types
        ]
        
        return jsonify({
            'success': True,
            'material_types': formatted_types
        })
        
    except Exception as e:
        logger.error(f"Error getting material types: {e}")
        return jsonify({'success': False, 'error': 'Failed to get material types'}), 500

@app.route('/api/materials/calculate', methods=['POST'])
def calculate_materials():
    """Calculate materials needed for a project."""
    try:
        data = request.get_json()
        
        # Extract calculation parameters
        project_type = data.get('project_type', 'retaining_wall')
        material_type = data.get('material_type', 'concrete')
        
        # Handle both old format (dimensions object) and new format (direct dimensions)
        if 'dimensions' in data:
            dimensions = data.get('dimensions', {})
        else:
            # New format: dimensions are directly in the data
            dimensions = {
                'length': data.get('length', 0),
                'width': data.get('width', 0),
                'height': data.get('height', 0),
                'depth': data.get('depth', 0)
            }
        
        # Calculate based on project type
        if project_type == 'retaining_wall':
            return calculate_retaining_wall(dimensions, material_type)
        elif project_type == 'patio':
            return calculate_patio(dimensions, material_type)
        else:
            return jsonify({'error': 'Unknown project type'}), 400
            
    except Exception as e:
        logger.error(f"Error calculating materials: {e}")
        return jsonify({'error': 'Failed to calculate materials'}), 500

def calculate_retaining_wall(dimensions, material_type):
    """Calculate materials for retaining wall."""
    length = dimensions.get('length', 0)
    height = dimensions.get('height', 0)
    width = dimensions.get('width', 0)
    
    # Calculate volume
    volume_cubic_feet = length * height * width
    volume_cubic_yards = volume_cubic_feet / 27
    
    # Calculate surface area
    surface_area = length * height
    
    # Material calculations based on type
    if material_type == 'concrete':
        blocks_needed = surface_area * 1.125  # 1.125 blocks per sqft
        mortar_needed = volume_cubic_feet * 0.1  # 10% of volume
    elif material_type == 'stone':
        stone_needed = surface_area * 0.5  # 0.5 tons per sqft
        mortar_needed = surface_area * 0.1  # 0.1 cuft per sqft
    else:
        blocks_needed = surface_area * 1.0
        mortar_needed = volume_cubic_feet * 0.1
    
    return jsonify({
        'success': True,
        'calculation': {
            'project_type': 'retaining_wall',
            'material_type': material_type,
            'dimensions': dimensions,
            'volume_cubic_yards': round(volume_cubic_yards, 2),
            'surface_area_sqft': round(surface_area, 2),
            'materials': {
                'blocks_stone': round(blocks_needed, 2),
                'mortar_cubic_feet': round(mortar_needed, 2)
            }
        }
    })

def calculate_patio(dimensions, material_type):
    """Calculate materials for patio."""
    length = dimensions.get('length', 0)
    width = dimensions.get('width', 0)
    depth = dimensions.get('depth', 0.25)  # Default 3 inches
    
    # Calculate area and volume
    area_sqft = length * width
    volume_cubic_feet = area_sqft * depth
    volume_cubic_yards = volume_cubic_feet / 27
    
    # Material calculations based on type
    if material_type == 'stone':
        pavers_needed = area_sqft * 1.1  # 10% waste factor
        base_material = volume_cubic_yards * 1.2  # 20% compaction factor
    elif material_type == 'concrete':
        concrete_needed = volume_cubic_yards * 1.1  # 10% waste factor
        base_material = volume_cubic_yards * 0.5  # 50% of concrete volume
    else:
        pavers_needed = area_sqft
        base_material = volume_cubic_yards
    
    return jsonify({
        'success': True,
        'calculation': {
            'project_type': 'patio',
            'material_type': material_type,
            'dimensions': dimensions,
            'area_sqft': round(area_sqft, 2),
            'volume_cubic_yards': round(volume_cubic_yards, 2),
            'materials': {
                'pavers_concrete': round(pavers_needed, 2),
                'base_material': round(base_material, 2)
            }
        }
    })

@app.route('/api/equipment')
def get_equipment():
    """Get all equipment."""
    try:
        return jsonify([e for e in equipment_data if e['is_active']])
    except Exception as e:
        logger.error(f"Error fetching equipment: {e}")
        return jsonify({'error': 'Failed to fetch equipment'}), 500

@app.route('/api/crew')
def get_crew():
    """Get all crew members."""
    try:
        return jsonify([c for c in crew_data if c['is_active']])
    except Exception as e:
        logger.error(f"Error fetching crew: {e}")
        return jsonify({'error': 'Failed to fetch crew'}), 500

@app.route('/api/projects')
def get_projects():
    """Get all projects."""
    try:
        return jsonify([p for p in projects_data if p['is_active']])
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return jsonify({'error': 'Failed to fetch projects'}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Create new project
        new_project = {
            'id': project_id,
            'name': data.get('name', 'New Project'),
            'description': data.get('description', ''),
            'status': data.get('status', 'planning'),
            'budget': data.get('budget', 0),
            'start_date': data.get('start_date', date.today().isoformat()),
            'is_active': True
        }
        
        projects_data.append(new_project)
        
        return jsonify({
            'success': True,
            'project': new_project
        })
        
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to create project'}), 500

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project."""
    try:
        data = request.get_json()
        project = next((p for p in projects_data if p['id'] == project_id), None)
        
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Update fields
        if 'name' in data:
            project['name'] = data['name']
        if 'status' in data:
            project['status'] = data['status']
        if 'budget' in data:
            project['budget'] = data['budget']
        
        return jsonify({
            'success': True,
            'project': project
        })
        
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to update project'}), 500

@app.route('/api/jobs')
def get_jobs():
    """Get all jobs."""
    try:
        return jsonify([j for j in jobs_data if j['is_active']])
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        return jsonify({'error': 'Failed to fetch jobs'}), 500

@app.route('/api/jobs/<job_id>')
def get_job(job_id):
    """Get a specific job by ID."""
    try:
        job = next((j for j in jobs_data if j['id'] == job_id and j['is_active']), None)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        return jsonify(job)
    except Exception as e:
        logger.error(f"Error fetching job: {e}")
        return jsonify({'error': 'Failed to fetch job'}), 500

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create new job
        new_job = {
            'id': job_id,
            'project_id': data.get('project_id'),
            'name': data.get('name', 'New Job'),
            'job_type': data.get('job_type'),
            'description': data.get('description', ''),
            'status': data.get('status', 'planned'),
            'measurements': data.get('measurements', {}),
            'calculation_result': data.get('calculation_result', {}),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        jobs_data.append(new_job)
        
        return jsonify({
            'success': True,
            'job': new_job
        })
        
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        return jsonify({'success': False, 'error': 'Failed to create job'}), 500

@app.route('/api/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    """Update an existing job."""
    try:
        data = request.get_json()
        job = next((j for j in jobs_data if j['id'] == job_id), None)
        
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Update fields
        if 'name' in data:
            job['name'] = data['name']
        if 'description' in data:
            job['description'] = data['description']
        if 'status' in data:
            job['status'] = data['status']
        if 'measurements' in data:
            job['measurements'] = data['measurements']
        if 'calculation_result' in data:
            job['calculation_result'] = data['calculation_result']
        
        job['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'job': job
        })
        
    except Exception as e:
        logger.error(f"Error updating job: {e}")
        return jsonify({'success': False, 'error': 'Failed to update job'}), 500

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job (soft delete)."""
    try:
        job = next((j for j in jobs_data if j['id'] == job_id), None)
        
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        job['is_active'] = False
        
        return jsonify({
            'success': True,
            'message': 'Job deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete job'}), 500

@app.route('/api/projects/<project_id>/jobs')
def get_project_jobs(project_id):
    """Get all jobs for a specific project."""
    try:
        project_jobs = [j for j in jobs_data if j['project_id'] == project_id and j['is_active']]
        return jsonify(project_jobs)
    except Exception as e:
        logger.error(f"Error fetching project jobs: {e}")
        return jsonify({'error': 'Failed to fetch project jobs'}), 500

@app.route('/api/jobs/<job_id>/recalculate', methods=['POST'])
def recalculate_job(job_id):
    """Recalculate a job using the job calculator."""
    try:
        from job_calculator import JobCalculator
        
        job = next((j for j in jobs_data if j['id'] == job_id), None)
        
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # Get the job calculator
        calculator = JobCalculator()
        
        # Perform calculation using the correct method signature
        result = calculator.calculate_job(job['job_type'], job['measurements'])
        
        # Update job with new calculation
        job['calculation_result'] = result
        job['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'job': job,
            'calculation': result
        })
            
    except Exception as e:
        logger.error(f"Error recalculating job: {e}")
        return jsonify({'success': False, 'error': f'Failed to recalculate job: {str(e)}'}), 500

@app.route('/')
def home():
    return jsonify({
        'message': 'Landscaper Management System API',
        'version': '1.0.0',
        'endpoints': [
            '/api/materials',
            '/api/equipment', 
            '/api/crew',
            '/api/projects',
            '/api/jobs',
            '/api/projects/<project_id>/jobs',
            '/api/jobs/<job_id>/recalculate',
            '/api/job-calculator/types',
            '/api/job-calculator/templates',
            '/api/job-calculator/calculate'
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Landscaper Management System...")
    print("📊 Available endpoints:")
    print("   - GET  /api/materials")
    print("   - GET  /api/equipment") 
    print("   - GET  /api/crew")
    print("   - GET  /api/projects")
    print("   - GET  /api/jobs")
    print("   - GET  /api/projects/<project_id>/jobs")
    print("   - POST /api/jobs/<job_id>/recalculate")
    print("   - GET  /api/job-calculator/types")
    print("   - GET  /api/job-calculator/templates")
    print("   - POST /api/job-calculator/calculate")
    print("🌐 Server will be available at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
