#!/usr/bin/env python3
"""
Database seeding script for Landscaper Staff Application
"""

import uuid
from datetime import date
from models import init_database, db
from models import Material, MaterialType, Equipment, EquipmentStatus, CrewMember, CrewRole, Job, JobStatus, Client

def seed_database():
    """Seed the database with initial data."""
    
    # Create Flask app context
    from flask import Flask
    app = Flask(__name__)
    init_database(app)
    
    with app.app_context():
        print("🌱 Seeding database...")
        
        # Clear existing data
        print("🗑️ Clearing existing data...")
        Job.query.delete()
        Equipment.query.delete()
        CrewMember.query.delete()
        Material.query.delete()
        Client.query.delete()
        
        # Seed materials
        print("📦 Seeding materials...")
        materials_data = [
            {
                "name": "Concrete Block",
                "material_type": "concrete",
                "description": "Standard concrete block for retaining walls",
                "unit_of_measure": "piece",
                "price_per_unit": 2.50,
                "supplier": "ABC Supply",
                "supplier_part_number": "CB-001",
                "use_case": "Retaining walls, garden walls",
                "installation_notes": "Requires gravel base and proper drainage"
            },
            {
                "name": "Natural Stone",
                "material_type": "stone",
                "description": "Natural stone for decorative walls",
                "unit_of_measure": "ton",
                "price_per_unit": 150.00,
                "supplier": "Stone Works",
                "supplier_part_number": "NS-001",
                "use_case": "Decorative walls, landscaping features",
                "installation_notes": "Premium material, requires skilled installation"
            },
            {
                "name": "Concrete Pavers",
                "material_type": "concrete",
                "description": "Interlocking concrete pavers for patios",
                "unit_of_measure": "piece",
                "price_per_unit": 1.50,
                "supplier": "ABC Supply",
                "supplier_part_number": "CP-001",
                "use_case": "Patios, walkways, driveways",
                "installation_notes": "Requires sand base and edge restraints"
            },
            {
                "name": "Natural Stone Pavers",
                "material_type": "stone",
                "description": "Natural stone pavers for patios and walkways",
                "unit_of_measure": "piece",
                "price_per_unit": 8.00,
                "supplier": "Stone Works",
                "supplier_part_number": "NSP-001",
                "use_case": "Premium patios, walkways",
                "installation_notes": "Premium material, requires polymeric sand"
            },
            {
                "name": "Brick Pavers",
                "material_type": "brick",
                "description": "Clay brick pavers for traditional patios",
                "unit_of_measure": "piece",
                "price_per_unit": 2.25,
                "supplier": "Brick & Stone Co",
                "supplier_part_number": "BP-001",
                "use_case": "Traditional patios, walkways",
                "installation_notes": "Classic look, weather resistant"
            }
        ]
        
        for material_data in materials_data:
            material = Material(**material_data)
            db.session.add(material)
            db.session.flush()  # Flush after each insert
        
        # Seed crew members
        print("👥 Seeding crew members...")
        crew_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@landscaper.com",
                "phone": "555-0101",
                "role": "supervisor",
                "hire_date": date(2023, 1, 15),
                "hourly_rate": 25.00,
                "emergency_contact_name": "Jane Doe",
                "emergency_contact_phone": "555-0102"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@landscaper.com",
                "phone": "555-0103",
                "role": "lead",
                "hire_date": date(2023, 2, 1),
                "hourly_rate": 22.00,
                "emergency_contact_name": "Bob Smith",
                "emergency_contact_phone": "555-0104"
            }
        ]
        
        for crew_data_item in crew_data:
            crew_member = CrewMember(**crew_data_item)
            db.session.add(crew_member)
            db.session.flush()  # Flush after each insert
        
        # Seed equipment
        print("🔧 Seeding equipment...")
        equipment_data = [
            {
                "name": "Excavator",
                "equipment_type": "heavy_machinery",
                "brand": "Caterpillar",
                "model": "320",
                "serial_number": "CAT320-2023-001",
                "status": "available",
                "purchase_date": date(2023, 1, 1),
                "purchase_price": 85000.00,
                "current_location": "Yard A",
                "last_maintenance_date": date(2024, 1, 15),
                "next_maintenance_date": date(2024, 4, 15)
            },
            {
                "name": "Skid Steer",
                "equipment_type": "heavy_machinery",
                "brand": "Bobcat",
                "model": "S650",
                "serial_number": "BCS650-2023-002",
                "status": "in_use",
                "purchase_date": date(2023, 2, 1),
                "purchase_price": 45000.00,
                "current_location": "Job Site 1",
                "last_maintenance_date": date(2024, 1, 10),
                "next_maintenance_date": date(2024, 4, 10)
            }
        ]
        
        for equipment_item in equipment_data:
            equipment = Equipment(**equipment_item)
            db.session.add(equipment)
            db.session.flush()  # Flush after each insert
        
        # Seed clients
        print("👤 Seeding clients...")
        clients_data = [
            {
                "company_name": "Smith Family",
                "contact_first_name": "Robert",
                "contact_last_name": "Smith",
                "email": "robert.smith@email.com",
                "phone": "555-0201",
                "address_line1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "postal_code": "90210"
            },
            {
                "company_name": "Johnson Estate",
                "contact_first_name": "Elizabeth",
                "contact_last_name": "Johnson",
                "email": "elizabeth.johnson@email.com",
                "phone": "555-0202",
                "address_line1": "456 Oak Ave",
                "city": "Somewhere",
                "state": "CA",
                "postal_code": "90211"
            }
        ]
        
        for client_data in clients_data:
            client = Client(**client_data)
            db.session.add(client)
            db.session.flush()  # Flush after each insert
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Database seeding completed successfully!")
        print(f"📊 Seeded {len(materials_data)} materials")
        print(f"👥 Seeded {len(crew_data)} crew members")
        print(f"🔧 Seeded {len(equipment_data)} equipment items")
        print(f"👤 Seeded {len(clients_data)} clients")

if __name__ == "__main__":
    seed_database()
