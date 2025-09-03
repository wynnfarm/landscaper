#!/usr/bin/env python3
"""
Flask app for landscaping management system with real database integration.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
import os
import uuid
from datetime import datetime, date

# Import models
from models import init_database, db
from models import Material, MaterialType, Equipment, EquipmentStatus, CrewMember, CrewRole, Job, JobStatus, Client

# Import job calculator
from job_calculator_api import create_job_calculator_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize database
init_database(app)

# Add job calculator routes
create_job_calculator_routes(app)

# API Routes
@app.route('/api/materials')
def get_materials():
    """Get all materials from database."""
    try:
        materials = Material.query.filter_by(is_active=True).all()
        return jsonify([material.to_dict() for material in materials])
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        return jsonify({'error': 'Failed to fetch materials'}), 500

@app.route('/api/materials/types')
def get_material_types():
    """Get available material types for the calculator."""
    try:
        # Get unique material types from the materials data
        material_types = db.session.query(Material.material_type).distinct().all()
        
        # Create a mapping of material types to their display names
        material_type_mapping = {
            "concrete": "Concrete",
            "stone": "Natural Stone", 
            "brick": "Brick",
            "block": "Block",
            "wood": "Wood",
            "metal": "Metal",
            "other": "Other"
        }
        
        # Format the response with display names
        formatted_types = [
            {
                "value": material_type[0],
                "label": material_type_mapping.get(material_type[0], material_type[0].title())
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
        elif project_type == 'garden_wall':
            return calculate_garden_wall(dimensions, material_type)
        else:
            return jsonify({'success': False, 'error': 'Unsupported project type'}), 400
            
    except Exception as e:
        logger.error(f"Error calculating materials: {e}")
        return jsonify({'success': False, 'error': 'Failed to calculate materials'}), 500

def calculate_retaining_wall(dimensions, material_type):
    """Calculate materials for retaining wall."""
    length = dimensions.get('length', 0)
    height = dimensions.get('height', 0)
    depth = dimensions.get('depth', 0)
    
    if not all([length, height, depth]):
        return jsonify({'success': False, 'error': 'Missing dimensions'}), 400
    
    # Calculate wall area
    wall_area = length * height
    
    # Calculate materials based on type
    if material_type == 'concrete':
        # Concrete blocks: 0.5 sq ft per block
        blocks_needed = int(wall_area / 0.5) + 1  # Add 1 for safety
        cap_blocks = int(length / 1) + 1  # 1 foot per cap block
        
        # Base materials
        gravel_base = wall_area * 0.5  # 0.5 cubic yards per 100 sq ft
        sand_fill = wall_area * 0.1    # 0.1 cubic yards per 100 sq ft
        
        materials = {
            'concrete_blocks': {
                'quantity': blocks_needed,
                'unit': 'blocks',
                'cost_per_unit': 4.50,
                'total_cost': blocks_needed * 4.50
            },
            'cap_blocks': {
                'quantity': cap_blocks,
                'unit': 'blocks',
                'cost_per_unit': 3.25,
                'total_cost': cap_blocks * 3.25
            },
            'gravel_base': {
                'quantity': gravel_base,
                'unit': 'cubic yards',
                'cost_per_unit': 45.00,
                'total_cost': gravel_base * 45.00
            },
            'sand_fill': {
                'quantity': sand_fill,
                'unit': 'cubic yards',
                'cost_per_unit': 35.00,
                'total_cost': sand_fill * 35.00
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'retaining_wall',
            'dimensions': dimensions,
            'wall_area': wall_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': wall_area * 2  # 2 hours per 100 sq ft
        })
    
    elif material_type == 'stone':
        # Natural stone: 1 ton covers ~35 sq ft
        stone_needed = int(wall_area / 35) + 1
        
        materials = {
            'natural_stone': {
                'quantity': stone_needed,
                'unit': 'tons',
                'cost_per_unit': 150.00,
                'total_cost': stone_needed * 150.00
            },
            'mortar': {
                'quantity': stone_needed * 0.1,
                'unit': 'bags',
                'cost_per_unit': 12.00,
                'total_cost': stone_needed * 0.1 * 12.00
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'retaining_wall',
            'dimensions': dimensions,
            'wall_area': wall_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': wall_area * 3  # 3 hours per 100 sq ft for stone
        })
    
    else:
        return jsonify({'success': False, 'error': 'Unsupported material type'}), 400

def calculate_patio(dimensions, material_type):
    """Calculate materials for patio."""
    length = dimensions.get('length', 0)
    width = dimensions.get('width', 0)
    
    if not all([length, width]):
        return jsonify({'success': False, 'error': 'Missing dimensions'}), 400
    
    patio_area = length * width
    
    if material_type == 'concrete':
        # Concrete pavers: 0.25 sq ft per paver
        pavers_needed = int(patio_area / 0.25) + 1
        
        materials = {
            'concrete_pavers': {
                'quantity': pavers_needed,
                'unit': 'pavers',
                'cost_per_unit': 1.50,
                'total_cost': pavers_needed * 1.50
            },
            'sand_base': {
                'quantity': patio_area * 0.1,
                'unit': 'cubic yards',
                'cost_per_unit': 35.00,
                'total_cost': patio_area * 0.1 * 35.00
            },
            'edge_restraints': {
                'quantity': int((length + width) * 2 / 4) + 1,  # 4 ft per restraint
                'unit': 'pieces',
                'cost_per_unit': 8.00,
                'total_cost': int((length + width) * 2 / 4) * 8.00
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'patio',
            'dimensions': dimensions,
            'patio_area': patio_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': patio_area * 1.5  # 1.5 hours per 100 sq ft
        })
    
    elif material_type == 'stone':
        # Natural stone pavers: 0.5 sq ft per stone
        stone_pavers_needed = int(patio_area / 0.5) + 1
        
        materials = {
            'natural_stone_pavers': {
                'quantity': stone_pavers_needed,
                'unit': 'stones',
                'cost_per_unit': 8.00,
                'total_cost': stone_pavers_needed * 8.00
            },
            'sand_base': {
                'quantity': patio_area * 0.1,
                'unit': 'cubic yards',
                'cost_per_unit': 35.00,
                'total_cost': patio_area * 0.1 * 35.00
            },
            'polymeric_sand': {
                'quantity': patio_area * 0.05,
                'unit': 'bags',
                'cost_per_unit': 25.00,
                'total_cost': patio_area * 0.05 * 25.00
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'patio',
            'dimensions': dimensions,
            'patio_area': patio_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': patio_area * 2.5  # 2.5 hours per 100 sq ft for stone
        })
    
    elif material_type == 'brick':
        # Brick pavers: 0.33 sq ft per brick
        brick_pavers_needed = int(patio_area / 0.33) + 1
        
        materials = {
            'brick_pavers': {
                'quantity': brick_pavers_needed,
                'unit': 'bricks',
                'cost_per_unit': 2.25,
                'total_cost': brick_pavers_needed * 2.25
            },
            'sand_base': {
                'quantity': patio_area * 0.1,
                'unit': 'cubic yards',
                'cost_per_unit': 35.00,
                'total_cost': patio_area * 0.1 * 35.00
            },
            'edge_restraints': {
                'quantity': int((length + width) * 2 / 4) + 1,
                'unit': 'pieces',
                'cost_per_unit': 8.00,
                'total_cost': int((length + width) * 2 / 4) * 8.00
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'patio',
            'dimensions': dimensions,
            'patio_area': patio_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': patio_area * 2.0  # 2 hours per 100 sq ft for brick
        })
    
    else:
        return jsonify({'success': False, 'error': f'Unsupported material type "{material_type}" for patio. Supported types: concrete, stone, brick'}), 400

def calculate_garden_wall(dimensions, material_type):
    """Calculate materials for garden wall."""
    length = dimensions.get('length', 0)
    height = dimensions.get('height', 0)
    
    if not all([length, height]):
        return jsonify({'success': False, 'error': 'Missing dimensions'}), 400
    
    wall_area = length * height
    
    # Similar to retaining wall but smaller scale
    if material_type == 'concrete':
        blocks_needed = int(wall_area / 0.5) + 1
        
        materials = {
            'concrete_blocks': {
                'quantity': blocks_needed,
                'unit': 'blocks',
                'cost_per_unit': 4.50,
                'total_cost': blocks_needed * 4.50
            },
            'cap_blocks': {
                'quantity': int(length / 1) + 1,
                'unit': 'blocks',
                'cost_per_unit': 3.25,
                'total_cost': int(length / 1) * 3.25
            }
        }
        
        total_cost = sum(item['total_cost'] for item in materials.values())
        
        return jsonify({
            'success': True,
            'project_type': 'garden_wall',
            'dimensions': dimensions,
            'wall_area': wall_area,
            'materials': materials,
            'total_cost': total_cost,
            'labor_hours': wall_area * 1.5  # 1.5 hours per 100 sq ft
        })
    
    else:
        return jsonify({'success': False, 'error': f'Unsupported material type "{material_type}" for garden wall. Supported types: concrete, stone, brick'}), 400

@app.route('/api/equipment')
def get_equipment():
    """Get all equipment from database."""
    try:
        equipment = Equipment.query.filter_by(is_active=True).all()
        return jsonify([item.to_dict() for item in equipment])
    except Exception as e:
        logger.error(f"Error fetching equipment: {e}")
        return jsonify({'error': 'Failed to fetch equipment'}), 500

@app.route('/api/crew')
def get_crew():
    """Get all crew members from database."""
    try:
        crew = CrewMember.query.filter_by(is_active=True).all()
        return jsonify([member.to_dict() for member in crew])
    except Exception as e:
        logger.error(f"Error fetching crew: {e}")
        return jsonify({'error': 'Failed to fetch crew'}), 500

@app.route('/api/projects')
def get_projects():
    """Get all jobs/projects from database."""
    try:
        jobs = Job.query.all()
        return jsonify([job.to_dict() for job in jobs])
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return jsonify({'error': 'Failed to fetch projects'}), 500

# Project management endpoints
@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project."""
    try:
        data = request.get_json()
        
        # Generate a unique job number
        job_number = f"JOB-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Create new job
        new_job = Job(
            id=str(uuid.uuid4()),
            job_number=job_number,
            client_id=data.get('client_id', str(uuid.uuid4())),  # Default client for now
            title=data.get('name', 'New Project'),
            description=data.get('description', ''),
            job_type='garden_design',
            status='planning',
            estimated_cost=data.get('budget', 0),
            created_by=None  # Will be set when user authentication is implemented
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project': new_job.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to create project'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project."""
    try:
        data = request.get_json()
        job = Job.query.get(project_id)
        
        if not job:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Update fields
        if 'name' in data:
            job.title = data['name']
        if 'status' in data:
            job.status = data['status']
        if 'budget' in data:
            job.estimated_cost = data['budget']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project': job.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update project'}), 500

@app.route('/api/projects/<int:project_id>/materials', methods=['POST'])
def add_material_to_project(project_id):
    """Add materials to an existing project."""
    try:
        data = request.get_json()
        job = Job.query.get(project_id)
        
        if not job:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # For now, just return success (material tracking will be implemented later)
        return jsonify({
            'success': True,
            'message': 'Materials added to project'
        })
        
    except Exception as e:
        logger.error(f"Error adding materials to project: {e}")
        return jsonify({'success': False, 'error': 'Failed to add materials to project'}), 500

@app.route('/api/projects/<int:project_id>/materials/<int:material_index>', methods=['DELETE'])
def remove_material_from_project(project_id, material_index):
    """Remove a material from a project."""
    try:
        job = Job.query.get(project_id)
        
        if not job:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # For now, just return success (material tracking will be implemented later)
        return jsonify({
            'success': True,
            'message': 'Material removed from project'
        })
        
    except Exception as e:
        logger.error(f"Error removing material from project: {e}")
        return jsonify({'success': False, 'error': 'Failed to remove material from project'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
