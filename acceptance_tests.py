#!/usr/bin/env python3
"""
Acceptance Tests for Landscaper Application

This test suite verifies that the application meets the core requirements:
1. Materials Calculator functionality
2. Database connectivity and material management
3. API endpoints and responses
4. Error handling and edge cases
5. Basic application functionality
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LandscaperAcceptanceTests:
    """Acceptance test suite for the Landscaper application."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 10  # 10 second timeout
        
    def log_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result with details."""
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if details:
            logger.info(f"   Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
    
    def test_application_health(self) -> bool:
        """Test 1: Application is running and responding."""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test_result("Application Health", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test_result("Application Health", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test_result("Application Health", False, f"Error: {str(e)}")
            return False
    
    def test_materials_api_endpoint(self) -> bool:
        """Test 2: Materials API endpoint returns data."""
        try:
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code == 200:
                materials = response.json()
                if isinstance(materials, list) and len(materials) > 0:
                    self.log_test_result("Materials API", True, f"Found {len(materials)} materials")
                    return True
                else:
                    self.log_test_result("Materials API", False, "No materials returned")
                    return False
            else:
                self.log_test_result("Materials API", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test_result("Materials API", False, f"Error: {str(e)}")
            return False
    
    def test_materials_calculator_basic(self) -> bool:
        """Test 3: Basic materials calculation functionality."""
        try:
            # Get available materials first
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code != 200:
                self.log_test_result("Materials Calculator Basic", False, "Cannot fetch materials")
                return False
            
            materials = response.json()
            if not materials:
                self.log_test_result("Materials Calculator Basic", False, "No materials available")
                return False
            
            # Use the first material for testing
            material_id = materials[0]["id"]
            
            # Test basic calculation
            payload = {
                "wall_height": 4,
                "wall_length": 20,
                "material_id": material_id
            }
            
            response = self.session.post(
                f"{self.base_url}/api/calculate-materials",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and "data" in result:
                    data = result["data"]
                    required_fields = ["wall_specifications", "primary_material", "materials_needed", "total_estimated_cost"]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    if not missing_fields:
                        self.log_test_result("Materials Calculator Basic", True, 
                                           f"Cost: ${data['total_estimated_cost']}")
                        return True
                    else:
                        self.log_test_result("Materials Calculator Basic", False, 
                                           f"Missing fields: {missing_fields}")
                        return False
                else:
                    self.log_test_result("Materials Calculator Basic", False, 
                                       f"Response: {result}")
                    return False
            else:
                self.log_test_result("Materials Calculator Basic", False, 
                                   f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Materials Calculator Basic", False, f"Error: {str(e)}")
            return False
    
    def test_materials_calculator_edge_cases(self) -> bool:
        """Test 4: Edge cases and error handling."""
        test_cases = [
            {
                "name": "Zero Dimensions",
                "payload": {"wall_height": 0, "wall_length": 0, "material_id": "test"},
                "expected_status": 400
            },
            {
                "name": "Negative Dimensions", 
                "payload": {"wall_height": -1, "wall_length": 10, "material_id": "test"},
                "expected_status": 400
            },
            {
                "name": "Missing Material ID",
                "payload": {"wall_height": 4, "wall_length": 20},
                "expected_status": 400
            },
            {
                "name": "Invalid Material ID",
                "payload": {"wall_height": 4, "wall_length": 20, "material_id": "invalid-uuid"},
                "expected_status": 400
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/calculate-materials",
                    json=test_case["payload"],
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == test_case["expected_status"]:
                    passed_tests += 1
                    logger.info(f"  ✅ {test_case['name']}: Expected status {test_case['expected_status']}")
                else:
                    logger.info(f"  ❌ {test_case['name']}: Got {response.status_code}, expected {test_case['expected_status']}")
                    
            except Exception as e:
                logger.info(f"  ❌ {test_case['name']}: Error {str(e)}")
        
        success = passed_tests == total_tests
        self.log_test_result("Materials Calculator Edge Cases", success, 
                           f"{passed_tests}/{total_tests} edge cases passed")
        return success
    
    def test_materials_calculator_different_materials(self) -> bool:
        """Test 5: Test calculation with different material types."""
        try:
            # Get available materials
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code != 200:
                self.log_test_result("Materials Calculator Different Types", False, "Cannot fetch materials")
                return False
            
            materials = response.json()
            if len(materials) < 2:
                self.log_test_result("Materials Calculator Different Types", False, "Need at least 2 materials")
                return False
            
            # Test with first two different materials
            test_materials = materials[:2]
            passed_tests = 0
            
            for material in test_materials:
                payload = {
                    "wall_height": 4,
                    "wall_length": 20,
                    "material_id": material["id"]
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/calculate-materials",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        passed_tests += 1
                        logger.info(f"  ✅ {material['name']}: ${result['data']['total_estimated_cost']}")
                    else:
                        logger.info(f"  ❌ {material['name']}: Calculation failed")
                else:
                    logger.info(f"  ❌ {material['name']}: Status {response.status_code}")
            
            success = passed_tests == len(test_materials)
            self.log_test_result("Materials Calculator Different Types", success,
                               f"{passed_tests}/{len(test_materials)} materials tested")
            return success
            
        except Exception as e:
            self.log_test_result("Materials Calculator Different Types", False, f"Error: {str(e)}")
            return False
    
    def test_database_connectivity(self) -> bool:
        """Test 6: Database connectivity and data integrity."""
        try:
            # Test materials endpoint (requires database)
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code == 200:
                materials = response.json()
                
                # Check data structure
                if materials and len(materials) > 0:
                    material = materials[0]
                    required_fields = ["id", "name", "material_type", "price_per_unit"]
                    missing_fields = [field for field in required_fields if field not in material]
                    
                    if not missing_fields:
                        self.log_test_result("Database Connectivity", True, 
                                           f"Connected, {len(materials)} materials loaded")
                        return True
                    else:
                        self.log_test_result("Database Connectivity", False,
                                           f"Missing fields: {missing_fields}")
                        return False
                else:
                    self.log_test_result("Database Connectivity", False, "No materials in database")
                    return False
            else:
                self.log_test_result("Database Connectivity", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Database Connectivity", False, f"Error: {str(e)}")
            return False
    
    def test_api_response_format(self) -> bool:
        """Test 7: API response format consistency."""
        try:
            # Test materials endpoint
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code == 200:
                materials = response.json()
                
                # Check if it's a list
                if not isinstance(materials, list):
                    self.log_test_result("API Response Format", False, "Materials should be a list")
                    return False
                
                # Check each material has required structure
                if materials:
                    material = materials[0]
                    if not isinstance(material, dict):
                        self.log_test_result("API Response Format", False, "Material should be a dict")
                        return False
                    
                    # Check for required fields
                    required_fields = ["id", "name", "material_type", "price_per_unit"]
                    for field in required_fields:
                        if field not in material:
                            self.log_test_result("API Response Format", False, f"Missing field: {field}")
                            return False
                
                self.log_test_result("API Response Format", True, "Consistent JSON structure")
                return True
            else:
                self.log_test_result("API Response Format", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("API Response Format", False, f"Error: {str(e)}")
            return False
    
    def test_performance_basic(self) -> bool:
        """Test 8: Basic performance - response times."""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/materials")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200 and response_time < 5.0:  # 5 second threshold
                self.log_test_result("Performance Basic", True, f"Response time: {response_time:.2f}s")
                return True
            elif response_time >= 5.0:
                self.log_test_result("Performance Basic", False, f"Slow response: {response_time:.2f}s")
                return False
            else:
                self.log_test_result("Performance Basic", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Performance Basic", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all acceptance tests and return results."""
        logger.info("🚀 Starting Landscaper Acceptance Tests")
        logger.info("=" * 50)
        
        tests = [
            ("Application Health", self.test_application_health),
            ("Materials API Endpoint", self.test_materials_api_endpoint),
            ("Materials Calculator Basic", self.test_materials_calculator_basic),
            ("Materials Calculator Edge Cases", self.test_materials_calculator_edge_cases),
            ("Materials Calculator Different Types", self.test_materials_calculator_different_materials),
            ("Database Connectivity", self.test_database_connectivity),
            ("API Response Format", self.test_api_response_format),
            ("Performance Basic", self.test_performance_basic),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\n📋 Running: {test_name}")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                logger.error(f"❌ Test {test_name} crashed: {str(e)}")
        
        # Summary
        logger.info("\n" + "=" * 50)
        logger.info("📊 ACCEPTANCE TEST SUMMARY")
        logger.info("=" * 50)
        
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            logger.info(f"{status} - {result['test']}")
            if result["details"]:
                logger.info(f"   {result['details']}")
        
        success_rate = (passed_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            logger.info("🎉 ACCEPTANCE TESTS PASSED - Application meets requirements!")
        elif success_rate >= 60:
            logger.info("⚠️  ACCEPTANCE TESTS PARTIALLY PASSED - Some issues need attention")
        else:
            logger.error("❌ ACCEPTANCE TESTS FAILED - Major issues need to be addressed")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "results": self.test_results,
            "overall_passed": success_rate >= 80
        }

def main():
    """Main function to run acceptance tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Landscaper Acceptance Tests")
    parser.add_argument("--url", default="http://localhost:5000", 
                       help="Base URL of the application")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run tests
    tester = LandscaperAcceptanceTests(args.url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_passed"] else 1)

if __name__ == "__main__":
    main()
