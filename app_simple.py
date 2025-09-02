#!/usr/bin/env python3
"""
Simple Flask app for landscaping management system.
"""

from flask import Flask, render_template, jsonify, request
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple in-memory data for testing
materials_data = [
    {
        "id": 1,
        "name": "Concrete Block",
        "material_type": "concrete",
        "description": "Standard concrete block for retaining walls",
        "unit_of_measure": "piece",
        "cost_per_unit": 2.50,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "Available in gray and tan"
    },
    {
        "id": 2,
        "name": "Natural Stone",
        "material_type": "stone",
        "description": "Natural stone for decorative walls",
        "unit_of_measure": "ton",
        "cost_per_unit": 150.00,
        "supplier": "Stone Works",
        "supplier_contact": "555-0456",
        "notes": "Various colors available"
    },
    {
        "id": 3,
        "name": "Concrete Pavers",
        "material_type": "concrete",
        "description": "Interlocking concrete pavers for patios",
        "unit_of_measure": "piece",
        "cost_per_unit": 1.50,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "Available in multiple colors and patterns"
    },
    {
        "id": 4,
        "name": "Natural Stone Pavers",
        "material_type": "stone",
        "description": "Natural stone pavers for patios and walkways",
        "unit_of_measure": "piece",
        "cost_per_unit": 8.00,
        "supplier": "Stone Works",
        "supplier_contact": "555-0456",
        "notes": "Premium quality, various stone types"
    },
    {
        "id": 5,
        "name": "Brick Pavers",
        "material_type": "brick",
        "description": "Clay brick pavers for traditional patios",
        "unit_of_measure": "piece",
        "cost_per_unit": 2.25,
        "supplier": "Brick & Stone Co",
        "supplier_contact": "555-0789",
        "notes": "Classic red brick, weather resistant"
    },
    {
        "id": 6,
        "name": "Sand Base",
        "material_type": "concrete",
        "description": "Sand for paver base and leveling",
        "unit_of_measure": "cubic_yard",
        "cost_per_unit": 35.00,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "Clean, washed sand"
    },
    {
        "id": 7,
        "name": "Edge Restraints",
        "material_type": "concrete",
        "description": "Plastic edge restraints for paver installations",
        "unit_of_measure": "piece",
        "cost_per_unit": 8.00,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "4-foot sections, easy installation"
    },
    {
        "id": 8,
        "name": "Polymeric Sand",
        "material_type": "stone",
        "description": "Polymeric sand for paver joints",
        "unit_of_measure": "bag",
        "cost_per_unit": 25.00,
        "supplier": "Stone Works",
        "supplier_contact": "555-0456",
        "notes": "Prevents weed growth, stabilizes joints"
    },
    {
        "id": 9,
        "name": "Gravel Base",
        "material_type": "concrete",
        "description": "Crushed gravel for wall foundations",
        "unit_of_measure": "cubic_yard",
        "cost_per_unit": 45.00,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "3/4 inch crushed stone"
    },
    {
        "id": 10,
        "name": "Cap Blocks",
        "material_type": "concrete",
        "description": "Decorative cap blocks for wall tops",
        "unit_of_measure": "piece",
        "cost_per_unit": 3.25,
        "supplier": "ABC Supply",
        "supplier_contact": "555-0123",
        "notes": "Available in multiple colors"
    }
]

equipment_data = [
    {
        "id": 1,
        "name": "Excavator",
        "equipment_type": "heavy_machinery",
        "status": "available",
        "current_location": "Yard A",
        "last_maintenance_date": "2024-01-15"
    },
    {
        "id": 2,
        "name": "Skid Steer",
        "equipment_type": "heavy_machinery", 
        "status": "in_use",
        "current_location": "Job Site 1",
        "last_maintenance_date": "2024-01-10"
    }
]

projects_data = [
    {
        "id": 1,
        "name": "Retaining Wall Project",
        "client_name": "Smith Family",
        "status": "in_progress",
        "start_date": "2024-01-01",
        "end_date": "2024-02-15",
        "budget": 15000
    },
    {
        "id": 2,
        "name": "Garden Design",
        "client_name": "Johnson Estate",
        "status": "planning",
        "start_date": "2024-02-01",
        "end_date": "2024-03-01",
        "budget": 8000
    }
]

crew_data = [
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "position": "Foreman",
        "status": "active",
        "phone": "555-0101",
        "email": "john@landscaper.com",
        "hire_date": "2023-01-15"
    },
    {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "position": "Landscaper",
        "status": "active",
        "phone": "555-0102",
        "email": "jane@landscaper.com",
        "hire_date": "2023-03-01"
    }
]

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/materials')
def materials():
    """Materials page."""
    return render_template('materials.html', materials=materials_data)

@app.route('/tools')
def tools():
    """Tools/Equipment page."""
    return render_template('tools.html', equipment=equipment_data)

@app.route('/projects')
def projects():
    """Projects page."""
    return render_template('projects.html', projects=projects_data)

@app.route('/crew')
def crew():
    """Crew page."""
    return render_template('crew.html', crew=crew_data)

# API Endpoints
@app.route('/api/materials')
def api_materials():
    """Get all materials."""
    return jsonify(materials_data)

@app.route('/api/equipment/status')
def api_equipment_status():
    """Get equipment status."""
    return jsonify(equipment_data)

@app.route('/api/projects')
def api_projects():
    """Get all projects."""
    return jsonify(projects_data)

@app.route('/api/crew')
def api_crew():
    """Get all crew members."""
    return jsonify(crew_data)

@app.route('/api/materials/add', methods=['POST'])
def api_add_material():
    """Add a new material."""
    try:
        data = request.get_json()
        new_material = {
            "id": len(materials_data) + 1,
            "name": data.get('name', ''),
            "material_type": data.get('material_type', ''),
            "description": data.get('description', ''),
            "unit_of_measure": data.get('unit_of_measure', ''),
            "cost_per_unit": float(data.get('cost_per_unit', 0)),
            "supplier": data.get('supplier', ''),
            "supplier_contact": data.get('supplier_contact', ''),
            "notes": data.get('notes', '')
        }
        materials_data.append(new_material)
        return jsonify({'success': True, 'message': 'Material added successfully'})
    except Exception as e:
        logger.error(f"Error adding material: {e}")
        return jsonify({'success': False, 'error': 'Failed to add material'}), 500

@app.route('/api/materials/edit/<material_id>', methods=['POST'])
def api_edit_material(material_id):
    """Edit a material."""
    try:
        data = request.get_json()
        material_id = int(material_id)
        
        for material in materials_data:
            if material['id'] == material_id:
                material.update({
                    "name": data.get('name', material['name']),
                    "material_type": data.get('material_type', material['material_type']),
                    "description": data.get('description', material['description']),
                    "unit_of_measure": data.get('unit_of_measure', material['unit_of_measure']),
                    "cost_per_unit": float(data.get('cost_per_unit', material['cost_per_unit'])),
                    "supplier": data.get('supplier', material['supplier']),
                    "supplier_contact": data.get('supplier_contact', material['supplier_contact']),
                    "notes": data.get('notes', material['notes'])
                })
                return jsonify({'success': True, 'message': 'Material updated successfully'})
        
        return jsonify({'success': False, 'error': 'Material not found'}), 404
    except Exception as e:
        logger.error(f"Error editing material: {e}")
        return jsonify({'success': False, 'error': 'Failed to edit material'}), 500

@app.route('/api/materials/delete/<material_id>', methods=['POST'])
def api_delete_material(material_id):
    """Delete a material."""
    try:
        material_id = int(material_id)
        global materials_data
        materials_data = [m for m in materials_data if m['id'] != material_id]
        return jsonify({'success': True, 'message': 'Material deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting material: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete material'}), 500

@app.route('/api/materials/types')
def get_material_types():
    """Get available material types for the calculator."""
    try:
        # Get unique material types from the materials data
        material_types = list(set(material["material_type"] for material in materials_data))
        
        # Create a mapping of material types to their display names
        material_type_mapping = {
            "concrete": "Concrete",
            "stone": "Natural Stone", 
            "brick": "Brick"
        }
        
        # Format the response with display names
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

# Project Designer API endpoints
@app.route('/api/designer/templates')
def get_design_templates():
    """Get available project design templates."""
    templates = [
        {
            "id": "residential_backyard",
            "name": "Residential Backyard",
            "description": "Complete backyard transformation with patio, retaining wall, and garden beds",
            "thumbnail": "🏡",
            "elements": [
                {"type": "patio", "x": 20, "y": 30, "width": 15, "height": 12, "material": "concrete_pavers"},
                {"type": "retaining_wall", "x": 10, "y": 50, "width": 25, "height": 4, "material": "versa_lok_standard"},
                {"type": "garden_bed", "x": 5, "y": 10, "width": 8, "height": 6, "plants": ["roses", "lavender"]},
                {"type": "pathway", "x": 35, "y": 20, "width": 3, "height": 15, "material": "stone_pavers"}
            ]
        },
        {
            "id": "commercial_entrance",
            "name": "Commercial Entrance",
            "description": "Professional entrance design with hardscaping and seasonal plants",
            "thumbnail": "🏢",
            "elements": [
                {"type": "entrance_patio", "x": 15, "y": 25, "width": 20, "height": 10, "material": "concrete"},
                {"type": "retaining_wall", "x": 5, "y": 40, "width": 30, "height": 3, "material": "natural_stone"},
                {"type": "planting_area", "x": 40, "y": 15, "width": 12, "height": 8, "plants": ["boxwood", "annuals"]},
                {"type": "lighting", "x": 18, "y": 28, "type": "path_lights", "quantity": 6}
            ]
        },
        {
            "id": "garden_retreat",
            "name": "Garden Retreat",
            "description": "Peaceful garden space with water features and native plants",
            "thumbnail": "🌿",
            "elements": [
                {"type": "water_feature", "x": 25, "y": 25, "width": 8, "height": 6, "style": "pond"},
                {"type": "garden_path", "x": 20, "y": 35, "width": 2, "height": 10, "material": "gravel"},
                {"type": "seating_area", "x": 15, "y": 15, "width": 6, "height": 4, "material": "stone"},
                {"type": "planting_beds", "x": 35, "y": 20, "width": 10, "height": 15, "plants": ["native_grasses", "wildflowers"]}
            ]
        }
    ]
    return jsonify(templates)

@app.route('/api/designer/elements')
def get_design_elements():
    """Get available design elements library."""
    elements = [
        {
            "category": "Hardscaping",
            "elements": [
                {"type": "patio", "name": "Patio", "icon": "🏠", "materials": ["concrete", "pavers", "stone"]},
                {"type": "retaining_wall", "name": "Retaining Wall", "icon": "🧱", "materials": ["concrete_blocks", "natural_stone", "timber"]},
                {"type": "pathway", "name": "Pathway", "icon": "🛤️", "materials": ["pavers", "gravel", "stone"]},
                {"type": "steps", "name": "Steps", "icon": "📶", "materials": ["stone", "concrete", "wood"]}
            ]
        },
        {
            "category": "Landscaping",
            "elements": [
                {"type": "garden_bed", "name": "Garden Bed", "icon": "🌱", "plants": ["annuals", "perennials", "shrubs"]},
                {"type": "tree", "name": "Tree", "icon": "🌳", "varieties": ["oak", "maple", "cherry", "pine"]},
                {"type": "hedge", "name": "Hedge", "icon": "🌿", "plants": ["boxwood", "privet", "holly"]},
                {"type": "lawn", "name": "Lawn", "icon": "🌾", "grass_types": ["fescue", "bermuda", "zoysia"]}
            ]
        },
        {
            "category": "Features",
            "elements": [
                {"type": "water_feature", "name": "Water Feature", "icon": "💧", "styles": ["fountain", "pond", "stream"]},
                {"type": "fire_pit", "name": "Fire Pit", "icon": "🔥", "materials": ["stone", "metal", "concrete"]},
                {"type": "lighting", "name": "Lighting", "icon": "💡", "types": ["path_lights", "spotlights", "string_lights"]},
                {"type": "seating", "name": "Seating", "icon": "🪑", "materials": ["wood", "stone", "metal"]}
            ]
        }
    ]
    return jsonify(elements)

@app.route('/api/designer/project/save', methods=['POST'])
def save_project():
    """Save a project design."""
    try:
        data = request.get_json()
        # In a real app, this would save to database
        # For now, just return success
        return jsonify({
            'success': True,
            'message': 'Project saved successfully',
            'project_id': f"proj_{int(data.get('totalCost', 0))}"
        })
    except Exception as e:
        logger.error(f"Error saving project: {e}")
        return jsonify({'success': False, 'error': 'Failed to save project'}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project with materials."""
    try:
        data = request.get_json()
        
        # Generate a unique project ID
        project_id = len(projects_data) + 1
        
        new_project = {
            "id": project_id,
            "name": data.get('name', 'New Project'),
            "client_name": "TBD",
            "status": data.get('status', 'planning'),
            "start_date": None,
            "end_date": None,
            "budget": data.get('estimated_cost', 0),
            "materials": data.get('materials', []),
            "calculation_data": data.get('calculation_data', {})
        }
        
        projects_data.append(new_project)
        
        return jsonify({
            'success': True,
            'message': 'Project created successfully',
            'project_id': project_id
        })
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to create project'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project."""
    try:
        data = request.get_json()
        
        # Find the project
        project = next((p for p in projects_data if p['id'] == project_id), None)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Update project fields
        project['name'] = data.get('name', project['name'])
        project['status'] = data.get('status', project['status'])
        project['budget'] = data.get('budget', project['budget'])
        
        return jsonify({
            'success': True,
            'message': 'Project updated successfully',
            'project_id': project_id
        })
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        return jsonify({'success': False, 'error': 'Failed to update project'}), 500

@app.route('/api/projects/<int:project_id>/materials/<int:material_index>', methods=['DELETE'])
def remove_material_from_project(project_id, material_index):
    """Remove a material from a project."""
    try:
        # Find the project
        project = next((p for p in projects_data if p['id'] == project_id), None)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Check if materials exist
        if 'materials' not in project or not project['materials']:
            return jsonify({'success': False, 'error': 'No materials found'}), 404
        
        # Check if material index is valid
        if material_index < 0 or material_index >= len(project['materials']):
            return jsonify({'success': False, 'error': 'Invalid material index'}), 404
        
        # Remove the material
        removed_material = project['materials'].pop(material_index)
        
        # Update project budget
        project['budget'] = project.get('budget', 0) - removed_material.get('total_cost', 0)
        
        return jsonify({
            'success': True,
            'message': 'Material removed successfully',
            'project_id': project_id,
            'removed_material': removed_material
        })
    except Exception as e:
        logger.error(f"Error removing material: {e}")
        return jsonify({'success': False, 'error': 'Failed to remove material'}), 500

@app.route('/api/projects/<int:project_id>/materials', methods=['POST'])
def add_materials_to_project(project_id):
    """Add materials to an existing project."""
    try:
        data = request.get_json()
        
        # Find the project
        project = next((p for p in projects_data if p['id'] == project_id), None)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Add materials to project
        new_materials = data.get('materials', [])
        if 'materials' not in project:
            project['materials'] = []
        
        project['materials'].extend(new_materials)
        
        # Update project budget
        total_material_cost = sum(material.get('total_cost', 0) for material in new_materials)
        project['budget'] = project.get('budget', 0) + total_material_cost
        
        return jsonify({
            'success': True,
            'message': 'Materials added to project successfully',
            'project_id': project_id,
            'materials_added': len(new_materials)
        })
    except Exception as e:
        logger.error(f"Error adding materials to project: {e}")
        return jsonify({'success': False, 'error': 'Failed to add materials to project'}), 500

@app.route('/api/designer/project/calculate', methods=['POST'])
def calculate_project_cost():
    """Calculate total cost for a project design."""
    try:
        data = request.get_json()
        elements = data.get('elements', [])
        
        material_costs = {
            'concrete': 8.50,
            'pavers': 12.00,
            'stone': 25.00,
            'concrete_blocks': 4.50,
            'natural_stone': 150.00,
            'timber': 15.00,
            'gravel': 35.00
        }
        
        total_cost = 0
        for element in elements:
            if element.get('material') and material_costs.get(element['material']):
                area = element.get('width', 0) * element.get('height', 0)
                total_cost += area * material_costs[element['material']]
        
        return jsonify({
            'success': True,
            'total_cost': total_cost,
            'element_count': len(elements)
        })
    except Exception as e:
        logger.error(f"Error calculating project cost: {e}")
        return jsonify({'success': False, 'error': 'Failed to calculate cost'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
