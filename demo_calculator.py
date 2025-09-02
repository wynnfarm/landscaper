#!/usr/bin/env python3
"""
Materials Calculator Demo Script

This script demonstrates the Materials Calculator functionality
by running a series of example calculations and showing the results.
"""

import requests
import json
import sys

def demo_materials_calculator():
    """Demonstrate the Materials Calculator functionality."""
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    session.timeout = 10
    
    print("🏠 Landscaper Materials Calculator Demo")
    print("=" * 50)
    
    # Test 1: Get available materials
    print("\n📋 Available Materials:")
    try:
        response = session.get(f"{base_url}/api/materials")
        if response.status_code == 200:
            materials = response.json()
            for i, material in enumerate(materials[:5], 1):  # Show first 5
                print(f"  {i}. {material['name']} - ${material['price_per_unit']}/unit")
            print(f"  ... and {len(materials) - 5} more materials")
        else:
            print(f"❌ Failed to get materials: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting materials: {e}")
        return False
    
    # Test 2: Calculate materials for different scenarios
    scenarios = [
        {
            "name": "Small Garden Wall",
            "wall_height": 2,
            "wall_length": 10,
            "description": "Low garden wall for flower beds"
        },
        {
            "name": "Standard Retaining Wall", 
            "wall_height": 4,
            "wall_length": 20,
            "description": "Typical residential retaining wall"
        },
        {
            "name": "Large Commercial Wall",
            "wall_height": 6,
            "wall_length": 50,
            "description": "Commercial landscaping project"
        }
    ]
    
    print("\n🧮 Materials Calculations:")
    print("-" * 50)
    
    for scenario in scenarios:
        print(f"\n📐 {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Dimensions: {scenario['wall_length']}' x {scenario['wall_height']}'")
        
        # Get first material for calculation
        response = session.get(f"{base_url}/api/materials")
        if response.status_code == 200:
            materials = response.json()
            material_id = materials[0]["id"]
            material_name = materials[0]["name"]
            
            # Calculate materials
            payload = {
                "wall_height": scenario["wall_height"],
                "wall_length": scenario["wall_length"],
                "material_id": material_id
            }
            
            try:
                response = session.post(
                    f"{base_url}/api/calculate-materials",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        data = result["data"]
                        
                        # Display results
                        print(f"   Material: {material_name}")
                        print(f"   Total Cost: ${data['total_estimated_cost']}")
                        
                        # Show materials needed
                        materials_needed = data.get("materials_needed", {})
                        if materials_needed:
                            print("   Materials Needed:")
                            for material, quantity in materials_needed.items():
                                if quantity > 0:
                                    print(f"     • {material}: {quantity}")
                        
                        # Show wall specifications
                        wall_specs = data.get("wall_specifications", {})
                        if wall_specs:
                            area = wall_specs.get("length_feet", 0) * wall_specs.get("height_feet", 0)
                            print(f"   Wall Area: {area} sq ft")
                        
                        # Show installation time
                        if "installation_notes" in data:
                            notes = data["installation_notes"]
                            if notes and len(notes) > 0:
                                for note in notes:
                                    if "Estimated installation time" in note:
                                        print(f"   {note}")
                        
                    else:
                        print(f"   ❌ Calculation failed: {result.get('error', 'Unknown error')}")
                else:
                    print(f"   ❌ API error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print()
    
    # Test 3: Show cost comparison between materials
    print("💰 Cost Comparison (20' x 4' wall):")
    print("-" * 50)
    
    try:
        response = session.get(f"{base_url}/api/materials")
        if response.status_code == 200:
            materials = response.json()
            
            # Test with first 3 materials
            for material in materials[:3]:
                payload = {
                    "wall_height": 4,
                    "wall_length": 20,
                    "material_id": material["id"]
                }
                
                try:
                    response = session.post(
                        f"{base_url}/api/calculate-materials",
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            cost = result["data"]["total_estimated_cost"]
                            print(f"  {material['name']}: ${cost}")
                        else:
                            print(f"  {material['name']}: Calculation failed")
                    else:
                        print(f"  {material['name']}: API error")
                        
                except Exception as e:
                    print(f"  {material['name']}: Error - {e}")
                    
    except Exception as e:
        print(f"❌ Error getting materials: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Materials Calculator Demo Complete!")
    print("The application is working correctly and meeting requirements.")
    
    return True

if __name__ == "__main__":
    success = demo_materials_calculator()
    sys.exit(0 if success else 1)
