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

# Import database models and initialization
from models.base import init_database
from models import *

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

# Initialize Database
try:
    db = init_database(app)
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    db = None

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
    return render_template('index.html', 
                         page_title="Landscaper Staff Dashboard",
                         page_header="🏠 Landscaper Staff Dashboard",
                         page_subtitle="Tools and resources for landscape professionals")

@app.route('/projects')
def projects():
    """Projects page - current and completed landscaping projects."""
    if not db:
        return render_template('projects.html', 
                             projects={'active_projects': [], 'completed_projects': []},
                             page_title="Project Management - Staff Dashboard",
                             page_header="📁 Active & Completed Projects",
                             page_subtitle="Track active and completed projects")
    
    try:
        # Get active projects (planning, in_progress, on_hold)
        active_projects = Job.query.filter(
            Job.status.in_(['planning', 'in_progress', 'on_hold'])
        ).order_by(Job.priority.asc(), Job.estimated_start_date.asc()).all()
        
        # Get completed projects
        completed_projects = Job.query.filter(
            Job.status == 'completed'
        ).order_by(Job.actual_end_date.desc()).limit(10).all()
        
        projects_data = {
            'active_projects': [project.to_dict() for project in active_projects],
            'completed_projects': [project.to_dict() for project in completed_projects]
        }
        
        return render_template('projects.html', 
                             projects=projects_data,
                             page_title="Project Management - Staff Dashboard",
                             page_header="📁 Active & Completed Projects",
                             page_subtitle="Track active and completed projects")
        
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return render_template('projects.html', 
                             projects={'active_projects': [], 'completed_projects': []},
                             page_title="Project Management - Staff Dashboard",
                             page_header="📁 Active & Completed Projects",
                             page_subtitle="Track active and completed projects")

@app.route('/materials')
def materials():
    """Materials management page - inventory and material information."""
    if not db:
        return render_template('materials.html', 
                             materials=[],
                             page_title="Materials Management",
                             page_header="📦 Materials Inventory",
                             page_subtitle="Manage landscaping materials and inventory")
    
    try:
        # Get all active materials
        materials = Material.query.filter(Material.is_active == True).order_by(Material.name.asc()).all()
        
        return render_template('materials.html', 
                             materials=[material.to_dict() for material in materials],
                             page_title="Materials Management",
                             page_header="📦 Materials Inventory",
                             page_subtitle="Manage landscaping materials and inventory")
        
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        return render_template('materials.html', 
                             materials=[],
                             page_title="Materials Management",
                             page_header="📦 Materials Inventory",
                             page_subtitle="Manage landscaping materials and inventory")

@app.route('/tools')
def tools():
    """Tools page - landscaping tools and equipment management."""
    if not db:
        return render_template('tools.html', 
                             tools={'equipment': [], 'hand_tools': []},
                             page_title="Equipment & Tools - Staff Dashboard",
                             page_header="🔧 Equipment & Tools",
                             page_subtitle="Manage landscaping equipment and tools")
    
    try:
        # Get all equipment
        equipment = Equipment.query.filter(Equipment.is_active == True).all()
        
        # For now, we'll simulate hand tools data since we don't have a separate hand_tools table
        # In a real implementation, you might want to create a separate HandTool model
        hand_tools = [
            {'name': 'Shovel - Round Point', 'count': 5, 'status': 'Available'},
            {'name': 'Rake - Leaf Rake', 'count': 3, 'status': 'Available'},
            {'name': 'Pruning Shears', 'count': 8, 'status': 'Available'},
            {'name': 'Hoe - Garden Hoe', 'count': 2, 'status': 'In Use'}
        ]
        
        tools_data = {
            'equipment': [eq.to_dict() for eq in equipment],
            'hand_tools': hand_tools
        }
        
        return render_template('tools.html', 
                             tools=tools_data,
                             page_title="Equipment & Tools - Staff Dashboard",
                             page_header="🔧 Equipment & Tools",
                             page_subtitle="Manage landscaping equipment and tools")
        
    except Exception as e:
        logger.error(f"Error fetching tools: {e}")
        return render_template('tools.html', 
                             tools={'equipment': [], 'hand_tools': []},
                             page_title="Equipment & Tools - Staff Dashboard",
                             page_header="🔧 Equipment & Tools",
                             page_subtitle="Manage landscaping equipment and tools")

@app.route('/chat')
def chat():
    """AI Chat page - interactive AI assistant."""
    return render_template('chat.html',
                         page_title="AI Assistant - Landscaper",
                         page_header="🤖 AI Landscaping Assistant",
                         page_subtitle="Ask me anything about our landscaping services!")

@app.route('/calculator')
def calculator():
    """Wall Material Calculator page."""
    return render_template('calculator.html',
                         page_title="Wall Material Calculator - Landscaper",
                         page_header="🧮 Wall Calculator",
                         page_subtitle="Calculate materials needed for your landscape wall project")

@app.route('/crew')
def crew():
    """Crew management page - staff information and schedules."""
    if not db:
        return render_template('crew.html', 
                             crew={'active_crew': [], 'schedule': {}},
                             page_title="Crew Management - Staff Dashboard",
                             page_header="👥 Crew Management",
                             page_subtitle="Manage staff schedules and assignments")
    
    try:
        # Get active crew members
        active_crew = CrewMember.query.filter(CrewMember.is_active == True).all()
        
        # Get today's schedule information
        from datetime import date
        today = date.today()
        
        # Get today's job assignments
        today_assignments = JobCrewAssignment.query.filter(
            JobCrewAssignment.assigned_date == today
        ).all()
        
        # Get today's tasks from active jobs
        active_jobs = Job.query.filter(
            Job.status.in_(['planning', 'in_progress'])
        ).all()
        
        tasks = []
        for job in active_jobs:
            if job.estimated_start_date and job.estimated_start_date <= today:
                tasks.append(f"Work on {job.title} at {job.full_site_address or 'site'}")
        
        crew_data = {
            'active_crew': [member.to_dict() for member in active_crew],
            'schedule': {
                'today': today.isoformat(),
                'weather': 'Sunny, 75°F',  # This could be integrated with a weather API
                'tasks': tasks[:5]  # Limit to 5 tasks
            }
        }
        
        return render_template('crew.html', 
                             crew=crew_data,
                             page_title="Crew Management - Staff Dashboard",
                             page_header="👥 Crew Management",
                             page_subtitle="Manage staff schedules and assignments")
        
    except Exception as e:
        logger.error(f"Error fetching crew data: {e}")
        return render_template('crew.html', 
                             crew={'active_crew': [], 'schedule': {}},
                             page_title="Crew Management - Staff Dashboard",
                             page_header="👥 Crew Management",
                             page_subtitle="Manage staff schedules and assignments")

@app.route('/api/project/update', methods=['POST'])
def update_project():
    """Update project status or information."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        status = data.get('status')
        
        if not project_id or not status:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find project
        project = Job.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Update project status
        project.status = status
        if status == 'completed':
            project.actual_end_date = datetime.now().date()
        
        db.session.commit()
        
        logger.info(f"Project {project.title} status updated to {status}")
        return jsonify({'success': True, 'message': 'Project updated successfully'})
        
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update project'}), 500

@app.route('/api/project/assign-crew', methods=['POST'])
def assign_crew_to_project():
    """API endpoint for assigning crew members to projects."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        crew_member = data.get('crew_member')
        role = data.get('role')
        
        if not all([project_id, crew_member, role]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find project
        project = Job.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Find crew member
        crew = CrewMember.query.filter(CrewMember.full_name.ilike(f'%{crew_member}%')).first()
        if not crew:
            return jsonify({'success': False, 'error': 'Crew member not found'}), 404
        
        # Create assignment
        assignment = JobCrewAssignment(
            job_id=project_id,
            crew_member_id=crew.id,
            role=role,
            assigned_date=datetime.now().date()
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        logger.info(f"Crew member {crew_member} assigned to project {project.title}")
        return jsonify({'success': True, 'message': 'Crew member assigned successfully'})
        
    except Exception as e:
        logger.error(f"Error assigning crew member: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to assign crew member'}), 500

@app.route('/api/project/log-time', methods=['POST'])
def log_project_time():
    """API endpoint for logging time on projects."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        project_id = data.get('project_id')
        hours = data.get('hours')
        description = data.get('description')
        
        if not all([project_id, hours, description]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find project
        project = Job.query.get(project_id)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Create time entry
        time_entry = JobTimeEntry(
            job_id=project_id,
            hours_worked=hours,
            work_description=description,
            date_worked=datetime.now().date()
        )
        
        db.session.add(time_entry)
        db.session.commit()
        
        logger.info(f"Time logged for project {project.title}: {hours} hours")
        return jsonify({'success': True, 'message': 'Time logged successfully'})
        
    except Exception as e:
        logger.error(f"Error logging time: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to log time'}), 500

@app.route('/api/crew/update', methods=['POST'])
def update_crew_member():
    """API endpoint for updating crew member status."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        crew_id = data.get('crew_id')
        status = data.get('status')
        
        if not all([crew_id, status]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find crew member
        crew = CrewMember.query.get(crew_id)
        if not crew:
            return jsonify({'success': False, 'error': 'Crew member not found'}), 404
        
        # Update crew member status
        crew.is_active = (status == 'active')
        
        db.session.commit()
        
        logger.info(f"Crew member {crew.full_name} status updated to {status}")
        return jsonify({'success': True, 'message': 'Crew member updated successfully'})
        
    except Exception as e:
        logger.error(f"Error updating crew member: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update crew member'}), 500

@app.route('/api/crew/assign-project', methods=['POST'])
def assign_crew_to_project_from_crew():
    """API endpoint for assigning crew members to projects from crew page."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        crew_id = data.get('crew_id')
        project = data.get('project')
        
        if not all([crew_id, project]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find crew member
        crew = CrewMember.query.get(crew_id)
        if not crew:
            return jsonify({'success': False, 'error': 'Crew member not found'}), 404
        
        # Find project by name
        job = Job.query.filter(Job.title.ilike(f'%{project}%')).first()
        if not job:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Create assignment
        assignment = JobCrewAssignment(
            job_id=job.id,
            crew_member_id=crew_id,
            role='laborer',  # Default role
            assigned_date=datetime.now().date()
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        logger.info(f"Crew member {crew.full_name} assigned to project {job.title}")
        return jsonify({'success': True, 'message': 'Crew member assigned successfully'})
        
    except Exception as e:
        logger.error(f"Error assigning crew member: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to assign crew member'}), 500

# Materials API Routes
@app.route('/api/materials/add', methods=['POST'])
def add_material():
    """Add a new material to the database."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
    
        # Validate required fields
        required_fields = ['name', 'material_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Create new material
        material = Material(
            name=data['name'],
            material_type=data['material_type'],
            description=data.get('description', ''),
            unit_of_measure=data.get('unit_of_measure', 'each'),
            price_per_unit=float(data.get('price_per_unit', 0)),
            supplier=data.get('supplier', ''),
            supplier_part_number=data.get('supplier_part_number', ''),
            use_case=data.get('use_case', ''),
            installation_notes=data.get('installation_notes', '')
        )
        
        db.session.add(material)
        db.session.commit()
        
        logger.info(f"Added new material: {material.name}")
        return jsonify({'success': True, 'message': 'Material added successfully', 'material_id': str(material.id)})
        
    except Exception as e:
        logger.error(f"Error adding material: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to add material'}), 500

@app.route('/api/materials/edit/<material_id>', methods=['POST'])
def edit_material(material_id):
    """Edit an existing material."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'success': False, 'error': 'Material not found'}), 404
        
        data = request.get_json()
        
        # Update material fields
        material.name = data.get('name', material.name)
        material.material_type = data.get('material_type', material.material_type)
        material.description = data.get('description', material.description)
        material.unit_of_measure = data.get('unit_of_measure', material.unit_of_measure)
        material.cost_per_unit = float(data.get('cost_per_unit', material.cost_per_unit))
        material.supplier = data.get('supplier', material.supplier)
        material.supplier_contact = data.get('supplier_contact', material.supplier_contact)
        material.notes = data.get('notes', material.notes)
        
        db.session.commit()
        
        logger.info(f"Updated material: {material.name}")
        return jsonify({'success': True, 'message': 'Material updated successfully'})
        
    except Exception as e:
        logger.error(f"Error updating material: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update material'}), 500

@app.route('/api/materials/delete/<material_id>', methods=['POST'])
def delete_material(material_id):
    """Delete a material (soft delete by setting is_active to False)."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'success': False, 'error': 'Material not found'}), 404
        
        # Soft delete - set is_active to False
        material.is_active = False
        db.session.commit()
        
        logger.info(f"Deleted material: {material.name}")
        return jsonify({'success': True, 'message': 'Material deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting material: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to delete material'}), 500

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

@app.route('/api/equipment/status')
def equipment_status():
    """API endpoint for equipment status data."""
    if not db:
        return jsonify([])
    
    try:
        equipment = Equipment.query.filter(Equipment.is_active == True).all()
        return jsonify([eq.to_dict() for eq in equipment])
    except Exception as e:
        logger.error(f"Error getting equipment: {e}")
        return jsonify([])

@app.route('/api/equipment/checkout', methods=['POST'])
def equipment_checkout():
    """API endpoint for checking out equipment."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        crew_member = data.get('crew_member')
        project = data.get('project')
        
        if not all([equipment_id, crew_member, project]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find equipment
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'success': False, 'error': 'Equipment not found'}), 404
        
        # Update equipment status
        equipment.status = 'in_use'
        equipment.current_location = f"Project {project}"
        equipment.assigned_to = crew_member
        
        db.session.commit()
        
        logger.info(f"Equipment {equipment.name} checked out to {crew_member} for {project}")
        return jsonify({'success': True, 'message': 'Equipment checked out successfully'})
        
    except Exception as e:
        logger.error(f"Error checking out equipment: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to check out equipment'}), 500

@app.route('/api/equipment/checkin', methods=['POST'])
def equipment_checkin():
    """API endpoint for checking in equipment."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        
        if not equipment_id:
            return jsonify({'success': False, 'error': 'Missing equipment ID'}), 400
        
        # Find equipment
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'success': False, 'error': 'Equipment not found'}), 404
        
        # Update equipment status
        equipment.status = 'available'
        equipment.current_location = 'Shop'
        equipment.assigned_to = None
        
        db.session.commit()
        
        logger.info(f"Equipment {equipment.name} checked in")
        return jsonify({'success': True, 'message': 'Equipment checked in successfully'})
        
    except Exception as e:
        logger.error(f"Error checking in equipment: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to check in equipment'}), 500

@app.route('/api/equipment/repair', methods=['POST'])
def equipment_repair():
    """API endpoint for marking equipment as repaired."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        notes = data.get('notes', '')
        
        if not equipment_id:
            return jsonify({'success': False, 'error': 'Missing equipment ID'}), 400
        
        # Find equipment
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'success': False, 'error': 'Equipment not found'}), 404
        
        # Update equipment status
        equipment.status = 'available'
        equipment.maintenance_notes = notes
        equipment.needs_maintenance = False
        
        db.session.commit()
        
        logger.info(f"Equipment {equipment.name} marked as repaired")
        return jsonify({'success': True, 'message': 'Equipment marked as repaired'})
        
    except Exception as e:
        logger.error(f"Error updating equipment repair status: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update equipment status'}), 500

@app.route('/api/equipment/maintenance', methods=['POST'])
def equipment_maintenance():
    """API endpoint for scheduling equipment maintenance."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 503
    
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        date = data.get('date')
        notes = data.get('notes', '')
        
        if not all([equipment_id, date]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Find equipment
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return jsonify({'success': False, 'error': 'Equipment not found'}), 404
        
        # Update maintenance schedule
        equipment.next_maintenance_date = date
        equipment.maintenance_notes = notes
        equipment.needs_maintenance = True
        
        db.session.commit()
        
        logger.info(f"Maintenance scheduled for equipment {equipment.name} on {date}")
        return jsonify({'success': True, 'message': 'Maintenance scheduled successfully'})
        
    except Exception as e:
        logger.error(f"Error scheduling maintenance: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to schedule maintenance'}), 500

@app.route('/api/materials/types', methods=['GET'])
def api_materials_types():
    """API endpoint for getting material types."""
    if not db:
        return jsonify([])
    
    try:
        # Get unique material types from the database
        material_types = db.session.query(Material.material_type).distinct().all()
        types = [mt[0] for mt in material_types if mt[0]]
        
        return jsonify({
            'success': True,
            'types': types
        })
    except Exception as e:
        logger.error(f"Error getting material types: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/materials')
def api_materials():
    """API endpoint for materials data."""
    if not db:
        return jsonify([])
    
    try:
        materials = Material.query.filter(Material.is_active == True).all()
        return jsonify([material.to_dict() for material in materials])
    except Exception as e:
        logger.error(f"Error getting materials: {e}")
        return jsonify([])

@app.route('/api/projects')
def api_projects():
    """API endpoint for projects data."""
    if not db:
        return jsonify([])
    
    try:
        projects = Job.query.all()
        return jsonify([project.to_dict() for project in projects])
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return jsonify([])

@app.route('/api/crew')
def api_crew():
    """API endpoint for crew data."""
    if not db:
        return jsonify([])
    
    try:
        crew = CrewMember.query.all()
        return jsonify([member.to_dict() for member in crew])
    except Exception as e:
        logger.error(f"Error getting crew: {e}")
        return jsonify([])

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
        
        # Ensure materials are loaded from database
        materials_calculator._ensure_materials_loaded()
        
        # Calculate materials
        result = materials_calculator.calculate_wall_materials(
            wall_length=float(data['wall_length']),
            wall_height=float(data['wall_height']),
            material_id=data['material_id'],
            include_base=data.get('include_base', True),
            include_cap=data.get('include_cap', True)
        )
        
        # Log the calculation for AI agent context
        if ai_agent and hasattr(ai_agent, 'add_conversation_entry'):
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

# Job-specific API endpoints
@app.route('/api/jobs', methods=['GET', 'POST'])
def api_jobs():
    """API endpoint for jobs - GET all jobs or POST new job."""
    if not db:
        return jsonify([])
    
    if request.method == 'GET':
        try:
            jobs = Job.query.all()
            return jsonify([job.to_dict() for job in jobs])
        except Exception as e:
            logger.error(f"Error getting jobs: {e}")
            return jsonify([])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Create new job
            job = Job(
                job_number=data.get('job_number', f"JOB-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                client_id=data.get('client_id'),
                title=data.get('name', data.get('title', 'New Job')),
                description=data.get('description', ''),
                job_type=data.get('job_type', 'general'),
                status=data.get('status', 'planning'),
                priority=data.get('priority', 3),
                site_address_line1=data.get('site_address_line1'),
                site_city=data.get('site_city'),
                site_state=data.get('site_state'),
                site_postal_code=data.get('site_postal_code'),
                estimated_start_date=data.get('estimated_start_date'),
                estimated_end_date=data.get('estimated_end_date'),
                estimated_cost=data.get('estimated_cost'),
                labor_hours_estimated=data.get('labor_hours_estimated'),
                weather_dependent=data.get('weather_dependent', False),
                requires_permits=data.get('requires_permits', False),
                special_instructions=data.get('special_instructions')
            )
            
            db.session.add(job)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'job': job.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Error creating job: {e}")
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<job_id>', methods=['GET', 'PUT', 'DELETE'])
def api_job_by_id(job_id):
    """API endpoint for specific job operations."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 500
    
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        if request.method == 'GET':
            return jsonify(job.to_dict())
        
        elif request.method == 'PUT':
            data = request.get_json()
            
            # Update job fields
            if 'name' in data or 'title' in data:
                job.title = data.get('name', data.get('title', job.title))
            if 'description' in data:
                job.description = data.get('description')
            if 'job_type' in data:
                job.job_type = data.get('job_type')
            if 'status' in data:
                job.status = data.get('status')
            if 'priority' in data:
                job.priority = data.get('priority')
            if 'estimated_start_date' in data:
                job.estimated_start_date = data.get('estimated_start_date')
            if 'estimated_end_date' in data:
                job.estimated_end_date = data.get('estimated_end_date')
            if 'estimated_cost' in data:
                job.estimated_cost = data.get('estimated_cost')
            if 'labor_hours_estimated' in data:
                job.labor_hours_estimated = data.get('labor_hours_estimated')
            if 'special_instructions' in data:
                job.special_instructions = data.get('special_instructions')
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'job': job.to_dict()
            })
        
        elif request.method == 'DELETE':
            db.session.delete(job)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Job deleted successfully'})
            
    except Exception as e:
        logger.error(f"Error with job {job_id}: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>/jobs', methods=['GET'])
def api_project_jobs(project_id):
    """API endpoint for getting jobs for a specific project."""
    if not db:
        return jsonify([])
    
    try:
        # For now, we'll treat project_id as client_id since we don't have a separate projects table
        # In a real system, you'd have a Project model and join tables
        jobs = Job.query.filter_by(client_id=project_id).all()
        return jsonify([job.to_dict() for job in jobs])
    except Exception as e:
        logger.error(f"Error getting jobs for project {project_id}: {e}")
        return jsonify([])

@app.route('/api/projects/<project_id>/materials', methods=['GET', 'POST'])
def api_project_materials(project_id):
    """API endpoint for project materials."""
    if not db:
        return jsonify([])
    
    if request.method == 'GET':
        try:
            # For now, return empty array since we don't have materials linked to projects
            # In a real system, you'd query materials for this project
            return jsonify([])
        except Exception as e:
            logger.error(f"Error getting materials for project {project_id}: {e}")
            return jsonify([])
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            # For now, just return success since we don't have materials storage
            # In a real system, you'd save materials to the database
            return jsonify({'success': True, 'message': 'Materials added successfully'})
        except Exception as e:
            logger.error(f"Error adding materials to project {project_id}: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<job_id>/recalculate', methods=['POST'])
def api_recalculate_job(job_id):
    """API endpoint for recalculating a job."""
    if not db:
        return jsonify({'success': False, 'error': 'Database not available'}), 500
    
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
        
        # For now, just return success since we don't have calculation logic here
        # In a real system, you'd recalculate based on job measurements
        return jsonify({
            'success': True,
            'message': 'Job recalculated successfully',
            'job': job.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error recalculating job {job_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Job Calculator API endpoints
@app.route('/api/job-calculator/types', methods=['GET'])
def get_job_types():
    """Get available job types"""
    try:
        from job_calculator import JobCalculator
        job_calculator = JobCalculator()
        job_types = job_calculator.get_job_types()
        return jsonify({
            'success': True,
            'types': job_types,
            'descriptions': {
                'pavers': 'Paver installation with base layers',
                'walls': 'Wall construction with blocks and mortar',
                'stairs': 'Stair construction with treads and risers',
                'steps': 'Individual step installation'
            }
        })
    except Exception as e:
        logger.error(f"Error getting job types: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/job-calculator/calculate', methods=['POST'])
def calculate_job():
    """Calculate job requirements"""
    try:
        from job_calculator import JobCalculator
        job_calculator = JobCalculator()
        
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
        logger.error(f"Error calculating job: {e}")
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

# Materials calculation endpoint
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
        mortar_needed = surface_area * 0.05  # 0.05 cubic yards per sqft
        gravel_needed = volume_cubic_yards * 0.5  # 50% gravel for base
        
        return jsonify({
            'success': True,
            'materials': {
                'concrete_blocks': {
                    'quantity': round(blocks_needed),
                    'unit': 'blocks',
                    'description': 'Concrete retaining wall blocks'
                },
                'mortar': {
                    'quantity': round(mortar_needed, 2),
                    'unit': 'cubic yards',
                    'description': 'Mortar for block installation'
                },
                'gravel_base': {
                    'quantity': round(gravel_needed, 2),
                    'unit': 'cubic yards',
                    'description': 'Gravel for base layer'
                }
            },
            'calculations': {
                'surface_area_sqft': round(surface_area, 2),
                'volume_cubic_yards': round(volume_cubic_yards, 2)
            }
        })
    else:
        return jsonify({'error': 'Unsupported material type for retaining wall'}), 400

def calculate_patio(dimensions, material_type):
    """Calculate materials for patio."""
    length = dimensions.get('length', 0)
    width = dimensions.get('width', 0)
    depth = dimensions.get('depth', 0)
    
    # Calculate area and volume
    area_sqft = length * width
    volume_cubic_feet = area_sqft * depth
    volume_cubic_yards = volume_cubic_feet / 27
    
    if material_type == 'concrete':
        concrete_needed = volume_cubic_yards
        gravel_needed = volume_cubic_yards * 0.5  # 50% gravel for base
        
        return jsonify({
            'success': True,
            'materials': {
                'concrete': {
                    'quantity': round(concrete_needed, 2),
                    'unit': 'cubic yards',
                    'description': 'Ready-mix concrete'
                },
                'gravel_base': {
                    'quantity': round(gravel_needed, 2),
                    'unit': 'cubic yards',
                    'description': 'Gravel for base layer'
                }
            },
            'calculations': {
                'area_sqft': round(area_sqft, 2),
                'volume_cubic_yards': round(volume_cubic_yards, 2)
            }
        })
    else:
        return jsonify({'error': 'Unsupported material type for patio'}), 400

if __name__ == '__main__':
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
