#!/usr/bin/env python3
"""
Comprehensive landscaping materials database seed script
Contains real-world materials with specifications, pricing, and usage information
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.base import init_database, db
from models.material import Material
from models.job_material import JobMaterial
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_materials_data():
    """Create comprehensive materials database with real-world data"""
    
    materials_data = [
        # RETAINING WALL BLOCKS
        {
            'name': 'Allan Block AB Collection - Charcoal',
            'material_type': 'block',
            'description': 'Interlocking concrete retaining wall block with natural stone texture finish',
            'length_inches': 18.0,
            'width_inches': 12.0,
            'height_inches': 8.0,
            'weight_lbs': 75.0,
            'price_per_unit': 6.25,
            'unit_of_measure': 'each',
            'supplier': 'Allan Block Corporation',
            'supplier_part_number': 'AB-CHARCOAL-18x12x8',
            'use_case': 'Retaining walls, garden walls, raised planters, outdoor kitchens',
            'installation_notes': 'Requires 6" compacted base, geogrid for walls over 3 feet, proper drainage behind wall'
        },
        {
            'name': 'Versa-Lok Standard - Tan',
            'material_type': 'block',
            'description': 'Modular concrete block system for freestanding and retaining walls',
            'length_inches': 18.0,
            'width_inches': 12.0,
            'height_inches': 6.0,
            'weight_lbs': 65.0,
            'price_per_unit': 5.95,
            'unit_of_measure': 'each',
            'supplier': 'Versa-Lok Retaining Wall Systems',
            'supplier_part_number': 'VL-STD-TAN-18x12x6',
            'use_case': 'Retaining walls, seat walls, fire pits, outdoor living spaces',
            'installation_notes': '4" compacted base required, geogrid reinforcement for walls over 4 feet'
        },
        {
            'name': 'Keystone Country Manor - Buff',
            'material_type': 'block',
            'description': 'Natural stone appearance concrete block with split-face texture',
            'length_inches': 18.0,
            'width_inches': 12.0,
            'height_inches': 8.0,
            'weight_lbs': 78.0,
            'price_per_unit': 7.15,
            'unit_of_measure': 'each',
            'supplier': 'Keystone Retaining Wall Systems',
            'supplier_part_number': 'KS-CM-BUFF-18x12x8',
            'use_case': 'Retaining walls, garden borders, raised beds, outdoor kitchens',
            'installation_notes': '6" compacted base, proper drainage, geogrid for walls over 3.5 feet'
        },

        # NATURAL STONE
        {
            'name': 'Pennsylvania Bluestone - Thermal Finish',
            'material_type': 'stone',
            'description': 'Premium bluestone with thermal finish for smooth, even surface',
            'length_inches': 24.0,
            'width_inches': 18.0,
            'height_inches': 2.0,
            'weight_lbs': 45.0,
            'price_per_unit': 12.50,
            'unit_of_measure': 'sq_ft',
            'supplier': 'Pennsylvania Bluestone Company',
            'supplier_part_number': 'PA-BLUE-THERMAL-2"',
            'use_case': 'Patios, walkways, pool decks, outdoor kitchens, fire pit surrounds',
            'installation_notes': '4" compacted base, polymeric sand joints, seal after installation'
        },
        {
            'name': 'Limestone Flagstone - Natural',
            'material_type': 'stone',
            'description': 'Natural limestone with irregular edges and natural cleft finish',
            'length_inches': 36.0,
            'width_inches': 24.0,
            'height_inches': 2.5,
            'weight_lbs': 65.0,
            'price_per_unit': 8.75,
            'unit_of_measure': 'sq_ft',
            'supplier': 'Midwest Stone Supply',
            'supplier_part_number': 'LIM-FLAG-NAT-2.5"',
            'use_case': 'Patios, walkways, garden paths, stepping stones',
            'installation_notes': '3" compacted base, irregular joints, polymeric sand'
        },
        {
            'name': 'Granite Cobblestone - Gray',
            'material_type': 'stone',
            'description': 'Natural granite cobblestones with rounded edges',
            'length_inches': 4.0,
            'width_inches': 4.0,
            'height_inches': 4.0,
            'weight_lbs': 8.0,
            'price_per_unit': 2.25,
            'unit_of_measure': 'each',
            'supplier': 'Granite Works',
            'supplier_part_number': 'GR-COBBLE-GRAY-4x4x4',
            'use_case': 'Driveways, walkways, edging, decorative borders',
            'installation_notes': '6" compacted base, sand joints, compact after installation'
        },

        # CONCRETE PAVERS
        {
            'name': 'Unilock Brussels Block - Charcoal',
            'material_type': 'concrete',
            'description': 'Interlocking concrete paver with natural stone texture',
            'length_inches': 7.875,
            'width_inches': 3.875,
            'height_inches': 3.125,
            'weight_lbs': 12.0,
            'price_per_unit': 3.85,
            'unit_of_measure': 'sq_ft',
            'supplier': 'Unilock',
            'supplier_part_number': 'UNI-BRUSSELS-CHARCOAL',
            'use_case': 'Driveways, patios, walkways, pool decks',
            'installation_notes': '4" compacted base, edge restraints, polymeric sand joints'
        },
        {
            'name': 'Belgard Mega-Arbel - Sierra',
            'material_type': 'concrete',
            'description': 'Large format concrete paver with slate-like appearance',
            'length_inches': 11.75,
            'width_inches': 11.75,
            'height_inches': 2.375,
            'weight_lbs': 18.0,
            'price_per_unit': 4.25,
            'unit_of_measure': 'sq_ft',
            'supplier': 'Belgard',
            'supplier_part_number': 'BEL-MEGA-ARBEL-SIERRA',
            'use_case': 'Patios, walkways, pool decks, outdoor living areas',
            'installation_notes': '4" compacted base, edge restraints, polymeric sand'
        },

        # MULCH & GROUND COVER
        {
            'name': 'Premium Hardwood Mulch - Natural',
            'material_type': 'other',
            'description': 'Double-ground hardwood mulch with natural brown color',
            'length_inches': None,
            'width_inches': None,
            'height_inches': None,
            'weight_lbs': None,
            'price_per_unit': 35.00,
            'unit_of_measure': 'cubic_yard',
            'supplier': 'Local Mulch Supply',
            'supplier_part_number': 'HW-MULCH-NAT-CY',
            'use_case': 'Garden beds, tree rings, landscape borders, erosion control',
            'installation_notes': 'Apply 2-3" depth, keep away from plant stems, refresh annually'
        },
        {
            'name': 'Red Cedar Mulch - Premium',
            'material_type': 'other',
            'description': 'Aromatic red cedar mulch with natural insect repellent properties',
            'length_inches': None,
            'width_inches': None,
            'height_inches': None,
            'weight_lbs': None,
            'price_per_unit': 42.00,
            'unit_of_measure': 'cubic_yard',
            'supplier': 'Cedar Mulch Company',
            'supplier_part_number': 'CEDAR-RED-PREM-CY',
            'use_case': 'Garden beds, playgrounds, pet areas, natural pest control',
            'installation_notes': 'Apply 2-3" depth, natural pest deterrent, lasts 2-3 years'
        },
        {
            'name': 'Pea Gravel - Natural',
            'material_type': 'stone',
            'description': 'Small, rounded gravel stones in natural earth tones',
            'length_inches': 0.5,
            'width_inches': 0.5,
            'height_inches': 0.5,
            'weight_lbs': 2800.0,
            'price_per_unit': 45.00,
            'unit_of_measure': 'ton',
            'supplier': 'Aggregate Supply',
            'supplier_part_number': 'PEA-GRAVEL-NAT-TON',
            'use_case': 'Drainage, walkways, decorative borders, playgrounds',
            'installation_notes': '2-3" depth, landscape fabric underneath, compact lightly'
        },

        # BRICK & CLAY PRODUCTS
        {
            'name': 'Clay Brick - Red',
            'material_type': 'brick',
            'description': 'Traditional red clay brick with smooth finish',
            'length_inches': 8.0,
            'width_inches': 4.0,
            'height_inches': 2.25,
            'weight_lbs': 4.5,
            'price_per_unit': 0.85,
            'unit_of_measure': 'each',
            'supplier': 'Brick Works',
            'supplier_part_number': 'CLAY-BRICK-RED-8x4x2.25',
            'use_case': 'Patios, walkways, edging, decorative walls',
            'installation_notes': '2" sand base, polymeric sand joints, edge restraints'
        },
        {
            'name': 'Fire Brick - High Heat',
            'material_type': 'brick',
            'description': 'Dense fire brick designed for high-temperature applications',
            'length_inches': 9.0,
            'width_inches': 4.5,
            'height_inches': 2.5,
            'weight_lbs': 6.0,
            'price_per_unit': 3.25,
            'unit_of_measure': 'each',
            'supplier': 'Fire Brick Supply',
            'supplier_part_number': 'FIRE-BRICK-HIGH-HEAT',
            'use_case': 'Fire pits, outdoor fireplaces, pizza ovens, kilns',
            'installation_notes': 'High-temperature mortar required, proper ventilation needed'
        },

        # DRAINAGE MATERIALS
        {
            'name': 'Perforated Drain Pipe - 4"',
            'material_type': 'other',
            'description': 'Corrugated perforated drain pipe with geotextile sock',
            'length_inches': 120.0,
            'width_inches': 4.0,
            'height_inches': 4.0,
            'weight_lbs': 8.0,
            'price_per_unit': 12.50,
            'unit_of_measure': 'linear_foot',
            'supplier': 'Drainage Solutions',
            'supplier_part_number': 'PERF-PIPE-4"-SOCK',
            'use_case': 'French drains, foundation drainage, yard drainage',
            'installation_notes': 'Install with 1% slope, wrap in gravel, cover with landscape fabric'
        },
        {
            'name': 'Catch Basin - 12" x 12"',
            'material_type': 'other',
            'description': 'Precast concrete catch basin with grate',
            'length_inches': 12.0,
            'width_inches': 12.0,
            'height_inches': 18.0,
            'weight_lbs': 85.0,
            'price_per_unit': 125.00,
            'unit_of_measure': 'each',
            'supplier': 'Concrete Products',
            'supplier_part_number': 'CATCH-BASIN-12x12x18',
            'use_case': 'Surface water collection, drainage systems, downspout connections',
            'installation_notes': 'Install with proper slope, connect to drain pipe, secure grate'
        },

        # LIGHTING & ELECTRICAL
        {
            'name': 'LED Path Light - Bronze',
            'material_type': 'other',
            'description': 'Low-voltage LED path light with bronze finish',
            'length_inches': 6.0,
            'width_inches': 6.0,
            'height_inches': 24.0,
            'weight_lbs': 3.5,
            'price_per_unit': 45.00,
            'unit_of_measure': 'each',
            'supplier': 'Landscape Lighting Co',
            'supplier_part_number': 'LED-PATH-BRONZE-24"',
            'use_case': 'Path lighting, accent lighting, safety lighting',
            'installation_notes': 'Low-voltage transformer required, 12V system, 18" spacing'
        },
        {
            'name': 'Solar Spot Light - Black',
            'material_type': 'other',
            'description': 'Solar-powered LED spot light with motion sensor',
            'length_inches': 4.0,
            'width_inches': 4.0,
            'height_inches': 18.0,
            'weight_lbs': 2.0,
            'price_per_unit': 28.00,
            'unit_of_measure': 'each',
            'supplier': 'Solar Lighting Solutions',
            'supplier_part_number': 'SOLAR-SPOT-BLACK-18"',
            'use_case': 'Security lighting, accent lighting, motion-activated lighting',
            'installation_notes': 'Full sun exposure required, 6-8 hours charge time, weatherproof'
        },

        # IRRIGATION
        {
            'name': 'Rotary Sprinkler Head - 15ft Radius',
            'material_type': 'other',
            'description': 'Pop-up rotary sprinkler with adjustable radius and pattern',
            'length_inches': 4.0,
            'width_inches': 4.0,
            'height_inches': 4.0,
            'weight_lbs': 0.5,
            'price_per_unit': 18.50,
            'unit_of_measure': 'each',
            'supplier': 'Irrigation Supply',
            'supplier_part_number': 'ROTARY-15FT-POPUP',
            'use_case': 'Lawn irrigation, large area coverage, commercial applications',
            'installation_notes': 'Requires 1/2" threaded connection, 30-50 PSI operating pressure'
        },
        {
            'name': 'Drip Emitter - 1 GPH',
            'material_type': 'other',
            'description': 'Pressure-compensating drip emitter with barb connection',
            'length_inches': 1.0,
            'width_inches': 0.5,
            'height_inches': 0.5,
            'weight_lbs': 0.1,
            'price_per_unit': 0.75,
            'unit_of_measure': 'each',
            'supplier': 'Drip Irrigation Systems',
            'supplier_part_number': 'DRIP-EMITTER-1GPH',
            'use_case': 'Plant watering, garden irrigation, water conservation',
            'installation_notes': 'Install on 1/4" tubing, 12-18" spacing, filter required'
        },

        # PLANT MATERIALS
        {
            'name': 'Red Maple Tree - 2" Caliper',
            'material_type': 'other',
            'description': 'Acer rubrum - Native red maple with excellent fall color',
            'length_inches': None,
            'width_inches': None,
            'height_inches': None,
            'weight_lbs': 150.0,
            'price_per_unit': 125.00,
            'unit_of_measure': 'each',
            'supplier': 'Tree Farm Nursery',
            'supplier_part_number': 'RED-MAPLE-2CAL',
            'use_case': 'Shade trees, street trees, fall color, wildlife habitat',
            'installation_notes': 'Plant in full sun to partial shade, well-drained soil, water regularly first year'
        },
        {
            'name': 'Boxwood Shrub - 3 Gallon',
            'material_type': 'other',
            'description': 'Buxus sempervirens - Evergreen shrub for formal hedges',
            'length_inches': 18.0,
            'width_inches': 18.0,
            'height_inches': 24.0,
            'weight_lbs': 25.0,
            'price_per_unit': 35.00,
            'unit_of_measure': 'each',
            'supplier': 'Shrub Specialists',
            'supplier_part_number': 'BOXWOOD-3GAL',
            'use_case': 'Formal hedges, topiary, foundation plantings, borders',
            'installation_notes': 'Plant 18-24" apart for hedge, well-drained soil, regular pruning'
        },
        {
            'name': 'Hostas - Mixed Variety',
            'material_type': 'other',
            'description': 'Hosta varieties - Shade-loving perennials with attractive foliage',
            'length_inches': 12.0,
            'width_inches': 12.0,
            'height_inches': 18.0,
            'weight_lbs': 2.0,
            'price_per_unit': 8.50,
            'unit_of_measure': 'each',
            'supplier': 'Perennial Gardens',
            'supplier_part_number': 'HOSTA-MIXED-1GAL',
            'use_case': 'Shade gardens, woodland gardens, container plantings, borders',
            'installation_notes': 'Plant in partial to full shade, rich soil, protect from slugs'
        },

        # SPECIALTY MATERIALS
        {
            'name': 'Gabion Basket - 3ft x 3ft x 3ft',
            'material_type': 'other',
            'description': 'Galvanized wire mesh basket for stone fill',
            'length_inches': 36.0,
            'width_inches': 36.0,
            'height_inches': 36.0,
            'weight_lbs': 25.0,
            'price_per_unit': 85.00,
            'unit_of_measure': 'each',
            'supplier': 'Gabion Solutions',
            'supplier_part_number': 'GABION-3x3x3-GALV',
            'use_case': 'Retaining walls, erosion control, decorative walls, seating',
            'installation_notes': 'Fill with 4-8" stone, secure with wire ties, level installation'
        },
        {
            'name': 'Rubber Mulch - Black',
            'material_type': 'other',
            'description': 'Recycled rubber mulch for playgrounds and high-traffic areas',
            'length_inches': None,
            'width_inches': None,
            'height_inches': None,
            'weight_lbs': None,
            'price_per_unit': 55.00,
            'unit_of_measure': 'cubic_yard',
            'supplier': 'Rubber Mulch Supply',
            'supplier_part_number': 'RUBBER-MULCH-BLACK-CY',
            'use_case': 'Playgrounds, dog runs, high-traffic areas, weed suppression',
            'installation_notes': 'Apply 3-4" depth, landscape fabric underneath, long-lasting'
        }
    ]
    
    return materials_data

def seed_materials():
    """Seed the database with materials data"""
    with app.app_context():
        try:
            # Clear existing job materials first (foreign key constraint)
            JobMaterial.query.delete()
            db.session.commit()
            logger.info("Cleared existing job materials")
            
            # Clear existing materials
            Material.query.delete()
            db.session.commit()
            logger.info("Cleared existing materials")
            
            # Get materials data
            materials_data = create_materials_data()
            
            # Create material objects
            materials = []
            for data in materials_data:
                material = Material(**data)
                materials.append(material)
            
            # Add to database
            db.session.add_all(materials)
            db.session.commit()
            
            logger.info(f"Successfully seeded {len(materials)} materials")
            
            # Print summary by category
            categories = {}
            for material in materials:
                category = material.material_type
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            logger.info("Materials by category:")
            for category, count in categories.items():
                logger.info(f"  {category}: {count} items")
                
        except Exception as e:
            logger.error(f"Error seeding materials: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    seed_materials()
