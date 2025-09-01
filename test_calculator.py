#!/usr/bin/env python3
"""
Test script for the landscaping calculator functionality.
"""

import requests
import json
import time

def test_calculator_apis():
    """Test the calculator API endpoints."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Landscaping Calculator APIs")
    print("=" * 50)
    
    # Test 1: Materials API
    print("\n1. Testing Materials API...")
    try:
        response = requests.get(f"{base_url}/api/materials", timeout=10)
        if response.status_code == 200:
            materials = response.json()
            print(f"✅ Materials API working! Found {len(materials)} materials")
            
            # Show first few materials
            for i, (material_id, material) in enumerate(list(materials.items())[:3]):
                print(f"   {i+1}. {material['name']} ({material['type']})")
        else:
            print(f"❌ Materials API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Materials API error: {e}")
        return False
    
    # Test 2: Calculation API
    print("\n2. Testing Calculation API...")
    try:
        calc_data = {
            "wall_length": 20,
            "wall_height": 4,
            "material_id": "versa_lok_standard",
            "include_base": True,
            "include_cap": True
        }
        
        response = requests.post(f"{base_url}/api/calculate-materials", 
                               json=calc_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            print("✅ Calculation API working!")
            print(f"   Wall: {data['wall_specifications']['length_feet']}' x {data['wall_specifications']['height_feet']}'")
            print(f"   Material: {data['primary_material']['name']}")
            print(f"   Total cost: ${data['total_estimated_cost']}")
            print(f"   Blocks needed: {data['materials_needed']['primary_blocks']}")
        else:
            print(f"❌ Calculation API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Calculation API error: {e}")
        return False
    
    # Test 3: Different material types
    print("\n3. Testing different material types...")
    test_cases = [
        {"material_id": "gabion_basket_3x3x6", "name": "Gabion Wall"},
        {"material_id": "standard_brick", "name": "Brick Wall"},
        {"material_id": "landscape_timber_6x6", "name": "Timber Wall"}
    ]
    
    for test_case in test_cases:
        try:
            calc_data = {
                "wall_length": 15,
                "wall_height": 3,
                "material_id": test_case["material_id"],
                "include_base": True,
                "include_cap": False
            }
            
            response = requests.post(f"{base_url}/api/calculate-materials", 
                                   json=calc_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                cost = result["data"]["total_estimated_cost"]
                print(f"   ✅ {test_case['name']}: ${cost}")
            else:
                print(f"   ❌ {test_case['name']}: Failed")
        except Exception as e:
            print(f"   ❌ {test_case['name']}: Error - {e}")
    
    print("\n🎉 Calculator API tests completed!")
    return True

def test_direct_calculator():
    """Test the calculator directly without API."""
    print("\n🔧 Testing Direct Calculator...")
    print("=" * 30)
    
    try:
        from landscaping_materials import LandscapingMaterials
        materials = LandscapingMaterials()
        
        # Test various wall configurations
        test_walls = [
            (10, 3, "versa_lok_standard", "Small Retaining Wall"),
            (25, 5, "allan_block_standard", "Large Retaining Wall"),
            (30, 4, "gabion_basket_3x3x6", "Gabion Wall"),
            (12, 2, "standard_brick", "Brick Wall"),
            (20, 3, "landscape_timber_6x6", "Timber Wall")
        ]
        
        for length, height, material_id, description in test_walls:
            try:
                result = materials.calculate_wall_materials(length, height, material_id)
                cost = result["total_estimated_cost"]
                primary_material = result["primary_material"]["name"]
                print(f"✅ {description}: {length}' x {height}' = ${cost} ({primary_material})")
            except Exception as e:
                print(f"❌ {description}: Error - {e}")
        
        print("\n✅ Direct calculator tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Direct calculator test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧱 Landscaping Calculator Test Suite")
    print("=" * 50)
    
    # Test direct calculator first
    direct_success = test_direct_calculator()
    
    # Wait a moment for server to be ready
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test API endpoints
    api_success = test_calculator_apis()
    
    print("\n📊 Test Results Summary:")
    print(f"   Direct Calculator: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"   API Endpoints: {'✅ PASS' if api_success else '❌ FAIL'}")
    
    if direct_success and api_success:
        print("\n🎉 All tests passed! Calculator is ready for use.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
