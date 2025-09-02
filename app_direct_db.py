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
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Database configuration
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5433'),
    'database': os.environ.get('DB_NAME', 'landscaper'),
    'user': os.environ.get('DB_USER', 'landscaper_user'),
    'password': os.environ.get('DB_PASSWORD', 'landscaper_password_2024')
}

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(**DATABASE_CONFIG)

# API Routes
@app.route('/api/materials')
def get_materials():
    """Get all materials from database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM materials WHERE is_active = true")
        materials = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for material in materials:
            result.append({
                'id': str(material['id']),
                'name': material['name'],
                'material_type': material['material_type'],
                'description': material['description'],
                'price_per_unit': float(material['price_per_unit']) if material['price_per_unit'] else None,
                'unit_of_measure': material['unit_of_measure'],
                'supplier': material['supplier'],
                'supplier_part_number': material['supplier_part_number'],
                'use_case': material['use_case'],
                'installation_notes': material['installation_notes'],
                'is_active': material['is_active'],
                'created_at': material['created_at'].isoformat() if material['created_at'] else None,
                'updated_at': material['updated_at'].isoformat() if material['updated_at'] else None
            })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        return jsonify({'error': 'Failed to fetch materials'}), 500

@app.route('/api/materials/types')
def get_material_types():
    """Get available material types for the calculator."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT material_type FROM materials WHERE is_active = true")
        material_types = cur.fetchall()
        cur.close()
        conn.close()
        
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
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM equipment WHERE is_active = true")
        equipment = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for item in equipment:
            result.append({
                'id': str(item['id']),
                'name': item['name'],
                'equipment_type': item['equipment_type'],
                'brand': item['brand'],
                'model': item['model'],
                'serial_number': item['serial_number'],
                'status': item['status'],
                'purchase_date': item['purchase_date'].isoformat() if item['purchase_date'] else None,
                'purchase_price': float(item['purchase_price']) if item['purchase_price'] else None,
                'current_location': item['current_location'],
                'assigned_to': str(item['assigned_to']) if item['assigned_to'] else None,
                'last_maintenance_date': item['last_maintenance_date'].isoformat() if item['last_maintenance_date'] else None,
                'next_maintenance_date': item['next_maintenance_date'].isoformat() if item['next_maintenance_date'] else None,
                'maintenance_notes': item['maintenance_notes'],
                'is_active': item['is_active'],
                'created_at': item['created_at'].isoformat() if item['created_at'] else None,
                'updated_at': item['updated_at'].isoformat() if item['updated_at'] else None
            })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching equipment: {e}")
        return jsonify({'error': 'Failed to fetch equipment'}), 500

@app.route('/api/crew')
def get_crew():
    """Get all crew members from database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM crew_members WHERE is_active = true")
        crew = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for member in crew:
            result.append({
                'id': str(member['id']),
                'first_name': member['first_name'],
                'last_name': member['last_name'],
                'full_name': f"{member['first_name']} {member['last_name']}",
                'email': member['email'],
                'phone': member['phone'],
                'role': member['role'],
                'hire_date': member['hire_date'].isoformat() if member['hire_date'] else None,
                'hourly_rate': float(member['hourly_rate']) if member['hourly_rate'] else None,
                'is_active': member['is_active'],
                'emergency_contact_name': member['emergency_contact_name'],
                'emergency_contact_phone': member['emergency_contact_phone'],
                'notes': member['notes'],
                'created_at': member['created_at'].isoformat() if member['created_at'] else None,
                'updated_at': member['updated_at'].isoformat() if member['updated_at'] else None
            })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching crew: {e}")
        return jsonify({'error': 'Failed to fetch crew'}), 500

@app.route('/api/projects')
def get_projects():
    """Get all jobs/projects from database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM jobs")
        jobs = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dictionaries
        result = []
        for job in jobs:
            result.append({
                'id': str(job['id']),
                'job_number': job['job_number'],
                'client_id': str(job['client_id']),
                'title': job['title'],
                'description': job['description'],
                'job_type': job['job_type'],
                'status': job['status'],
                'priority': job['priority'],
                'site_address_line1': job['site_address_line1'],
                'site_address_line2': job['site_address_line2'],
                'site_city': job['site_city'],
                'site_state': job['site_state'],
                'site_postal_code': job['site_postal_code'],
                'site_notes': job['site_notes'],
                'estimated_start_date': job['estimated_start_date'].isoformat() if job['estimated_start_date'] else None,
                'estimated_end_date': job['estimated_end_date'].isoformat() if job['estimated_end_date'] else None,
                'actual_start_date': job['actual_start_date'].isoformat() if job['actual_start_date'] else None,
                'actual_end_date': job['actual_end_date'].isoformat() if job['actual_end_date'] else None,
                'estimated_cost': float(job['estimated_cost']) if job['estimated_cost'] else None,
                'actual_cost': float(job['actual_cost']) if job['actual_cost'] else None,
                'labor_hours_estimated': float(job['labor_hours_estimated']) if job['labor_hours_estimated'] else None,
                'labor_hours_actual': float(job['labor_hours_actual']) if job['labor_hours_actual'] else None,
                'supervisor_id': str(job['supervisor_id']) if job['supervisor_id'] else None,
                'lead_worker_id': str(job['lead_worker_id']) if job['lead_worker_id'] else None,
                'weather_dependent': job['weather_dependent'],
                'requires_permits': job['requires_permits'],
                'permit_numbers': job['permit_numbers'],
                'special_instructions': job['special_instructions'],
                'completion_notes': job['completion_notes'],
                'created_at': job['created_at'].isoformat() if job['created_at'] else None,
                'updated_at': job['updated_at'].isoformat() if job['updated_at'] else None,
                'created_by': str(job['created_by']) if job['created_by'] else None
            })
        
        return jsonify(result)
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
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create new job
        cur.execute("""
            INSERT INTO jobs (id, job_number, client_id, title, description, job_type, status, estimated_cost, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            str(uuid.uuid4()),
            job_number,
            data.get('client_id', str(uuid.uuid4())),
            data.get('name', 'New Project'),
            data.get('description', ''),
            'garden_design',
            'planning',
            data.get('budget', 0),
            None
        ))
        
        job_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'project': {'id': str(job_id), 'job_number': job_number}
        })
        
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to create project'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT id FROM jobs WHERE id = %s", (project_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Build update query
        updates = []
        values = []
        
        if 'name' in data:
            updates.append("title = %s")
            values.append(data['name'])
        if 'status' in data:
            updates.append("status = %s")
            values.append(data['status'])
        if 'budget' in data:
            updates.append("estimated_cost = %s")
            values.append(data['budget'])
        
        if updates:
            values.append(project_id)
            cur.execute(f"UPDATE jobs SET {', '.join(updates)} WHERE id = %s", values)
            conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Project updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to update project'}), 500

@app.route('/api/projects/<int:project_id>/materials', methods=['POST'])
def add_material_to_project(project_id):
    """Add materials to an existing project."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT id FROM jobs WHERE id = %s", (project_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        cur.close()
        conn.close()
        
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
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT id FROM jobs WHERE id = %s", (project_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        cur.close()
        conn.close()
        
        # For now, just return success (material tracking will be implemented later)
        return jsonify({
            'success': True,
            'message': 'Material removed from project'
        })
        
    except Exception as e:
        logger.error(f"Error removing material from project: {e}")
        return jsonify({'success': False, 'error': 'Failed to remove material from project'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
