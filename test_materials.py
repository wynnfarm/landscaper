#!/usr/bin/env python3

from app import app
from landscaping_materials import LandscapingMaterials

with app.app_context():
    print("Testing materials loading...")
    calc = LandscapingMaterials()
    calc._ensure_materials_loaded()
    print(f"Materials loaded: {len(calc.materials)}")
    print(f"Available IDs: {list(calc.materials.keys())[:3]}")
    
    # Test with a specific material ID
    test_id = "fca399e6-9290-410b-8ecc-e2f23172353f"
    material = calc.get_material(test_id)
    print(f"Material {test_id}: {material.name if material else 'Not found'}")
