#!/usr/bin/env python3
"""
User Navigation Acceptance Tests for Landscaper Application

This test suite simulates real user interactions with the web application:
1. Navigating through different pages
2. Using web forms and interfaces
3. Testing user workflows
4. Verifying UI functionality
5. Checking responsive design elements
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List
import logging
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserNavigationTests:
    """Acceptance test suite that simulates real user navigation."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 10
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
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
    
    def get_page_content(self, url: str) -> Dict[str, Any]:
        """Get page content and parse with BeautifulSoup."""
        try:
            response = self.session.get(url)
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "content": response.text,
                "soup": BeautifulSoup(response.text, 'html.parser') if response.status_code == 200 else None,
                "url": response.url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": "",
                "soup": None,
                "url": url
            }
    
    def test_home_page_navigation(self) -> bool:
        """Test 1: User visits home page and can navigate."""
        logger.info("🏠 Testing Home Page Navigation")
        
        # Get home page
        result = self.get_page_content(f"{self.base_url}/")
        
        if not result["success"]:
            self.log_test_result("Home Page Navigation", False, f"Status: {result['status_code']}")
            return False
        
        soup = result["soup"]
        
        # Check for key elements
        checks = [
            ("Page Title", soup.title and "Landscaper" in soup.title.text),
            ("Navigation Menu", soup.find('nav') or soup.find('ul', class_='nav')),
            ("Main Content", soup.find('main') or soup.find('div', class_='container')),
            ("Mobile Responsive", 'viewport' in soup.find('meta', attrs={'name': 'viewport'}).get('content', '') if soup.find('meta', attrs={'name': 'viewport'}) else False)
        ]
        
        passed_checks = sum(1 for _, check in checks if check)
        
        if passed_checks >= 3:
            self.log_test_result("Home Page Navigation", True, f"{passed_checks}/4 elements found")
            return True
        else:
            failed_checks = [name for name, check in checks if not check]
            self.log_test_result("Home Page Navigation", False, f"Missing: {', '.join(failed_checks)}")
            return False
    
    def test_materials_page_user_workflow(self) -> bool:
        """Test 2: User navigates to materials page and views materials."""
        logger.info("📋 Testing Materials Page User Workflow")
        
        # Get materials page
        result = self.get_page_content(f"{self.base_url}/materials")
        
        if not result["success"]:
            self.log_test_result("Materials Page Workflow", False, f"Status: {result['status_code']}")
            return False
        
        soup = result["soup"]
        
        # Check for materials display
        checks = [
            ("Materials List", soup.find('table') or soup.find('div', class_='materials-list')),
            ("Material Items", len(soup.find_all('tr')) > 1 or len(soup.find_all('div', class_='material-item')) > 0),
            ("Material Names", any('concrete' in str(item).lower() or 'stone' in str(item).lower() for item in soup.find_all(['td', 'div']))),
            ("Prices Displayed", any('$' in str(item) for item in soup.find_all(['td', 'div']))),
        ]
        
        passed_checks = sum(1 for _, check in checks if check)
        
        if passed_checks >= 2:
            self.log_test_result("Materials Page Workflow", True, f"{passed_checks}/4 elements found")
            return True
        else:
            failed_checks = [name for name, check in checks if not check]
            self.log_test_result("Materials Page Workflow", False, f"Missing: {', '.join(failed_checks)}")
            return False
    
    def test_projects_page_user_workflow(self) -> bool:
        """Test 3: User navigates to projects page."""
        logger.info("📁 Testing Projects Page User Workflow")
        
        # Get projects page
        result = self.get_page_content(f"{self.base_url}/projects")
        
        if not result["success"]:
            self.log_test_result("Projects Page Workflow", False, f"Status: {result['status_code']}")
            return False
        
        soup = result["soup"]
        
        # Check for projects display
        checks = [
            ("Projects Section", soup.find('div', class_='projects') or soup.find('section', class_='projects')),
            ("Active Projects", 'active' in str(soup).lower() or 'planning' in str(soup).lower()),
            ("Completed Projects", 'completed' in str(soup).lower() or 'finished' in str(soup).lower()),
            ("Project List", soup.find('table') or soup.find('ul', class_='project-list')),
        ]
        
        passed_checks = sum(1 for _, check in checks if check)
        
        if passed_checks >= 2:
            self.log_test_result("Projects Page Workflow", True, f"{passed_checks}/4 elements found")
            return True
        else:
            failed_checks = [name for name, check in checks if not check]
            self.log_test_result("Projects Page Workflow", False, f"Missing: {', '.join(failed_checks)}")
            return False
    
    def test_materials_calculator_web_interface(self) -> bool:
        """Test 4: User uses the materials calculator through web interface."""
        logger.info("🧮 Testing Materials Calculator Web Interface")
        
        # First, check if there's a calculator page
        calculator_urls = [
            f"{self.base_url}/calculator",
            f"{self.base_url}/materials-calculator",
            f"{self.base_url}/calculate",
            f"{self.base_url}/tools/calculator"
        ]
        
        calculator_page = None
        for url in calculator_urls:
            result = self.get_page_content(url)
            if result["success"]:
                calculator_page = result
                break
        
        if not calculator_page:
            # Try to find calculator on materials page
            result = self.get_page_content(f"{self.base_url}/materials")
            if result["success"]:
                soup = result["soup"]
                if soup.find('form') or soup.find('input', type='number'):
                    calculator_page = result
                    logger.info("  Found calculator form on materials page")
        
        if not calculator_page:
            self.log_test_result("Materials Calculator Web Interface", False, "No calculator page found")
            return False
        
        soup = calculator_page["soup"]
        
        # Check for calculator elements
        checks = [
            ("Calculator Form", soup.find('form')),
            ("Wall Height Input", soup.find('input', attrs={'id': 'wall-height'}) or soup.find('input', attrs={'name': 'wall_height'}) or soup.find('input', attrs={'placeholder': 'height'})),
            ("Wall Length Input", soup.find('input', attrs={'id': 'wall-length'}) or soup.find('input', attrs={'name': 'wall_length'}) or soup.find('input', attrs={'placeholder': 'length'})),
            ("Material Selection", soup.find('select', attrs={'id': 'material-type'}) or soup.find('select', attrs={'id': 'specific-material'}) or soup.find('select')),
            ("Calculate Button", soup.find('button', string=re.compile('calculate', re.I)) or soup.find('input', type='submit')),
        ]
        
        passed_checks = sum(1 for _, check in checks if check)
        
        if passed_checks >= 3:
            self.log_test_result("Materials Calculator Web Interface", True, f"{passed_checks}/5 elements found")
            return True
        else:
            failed_checks = [name for name, check in checks if not check]
            self.log_test_result("Materials Calculator Web Interface", False, f"Missing: {', '.join(failed_checks)}")
            return False
    
    def test_materials_calculator_form_submission(self) -> bool:
        """Test 5: User submits calculator form and gets results."""
        logger.info("📝 Testing Materials Calculator Form Submission")
        
        # First get available materials via API
        try:
            response = self.session.get(f"{self.base_url}/api/materials")
            if response.status_code != 200:
                self.log_test_result("Calculator Form Submission", False, "Cannot get materials")
                return False
            
            materials = response.json()
            if not materials:
                self.log_test_result("Calculator Form Submission", False, "No materials available")
                return False
            
            material_id = materials[0]["id"]
            
            # Try to submit form data
            form_data = {
                "wall_height": 4,
                "wall_length": 20,
                "material_id": material_id
            }
            
            # Try different form submission endpoints
            submission_urls = [
                f"{self.base_url}/calculate",
                f"{self.base_url}/calculator",
                f"{self.base_url}/materials-calculator",
                f"{self.base_url}/api/calculate-materials"  # API endpoint as fallback
            ]
            
            success = False
            for url in submission_urls:
                try:
                    if url.endswith('/api/calculate-materials'):
                        # API endpoint
                        response = self.session.post(url, json=form_data, headers={'Content-Type': 'application/json'})
                    else:
                        # Web form endpoint
                        response = self.session.post(url, data=form_data)
                    
                    if response.status_code == 200:
                        # Check if response contains calculation results
                        if 'total_estimated_cost' in response.text or 'materials_needed' in response.text:
                            success = True
                            logger.info(f"  Form submission successful via {url}")
                            break
                        
                except Exception as e:
                    continue
            
            if success:
                self.log_test_result("Calculator Form Submission", True, "Form submitted successfully")
                return True
            else:
                self.log_test_result("Calculator Form Submission", False, "No working form submission found")
                return False
                
        except Exception as e:
            self.log_test_result("Calculator Form Submission", False, f"Error: {str(e)}")
            return False
    
    def test_responsive_design_elements(self) -> bool:
        """Test 6: Check for responsive design elements."""
        logger.info("📱 Testing Responsive Design Elements")
        
        # Get home page
        result = self.get_page_content(f"{self.base_url}/")
        
        if not result["success"]:
            self.log_test_result("Responsive Design", False, f"Status: {result['status_code']}")
            return False
        
        soup = result["soup"]
        
        # Check for responsive design elements
        checks = [
            ("Viewport Meta Tag", soup.find('meta', attrs={'name': 'viewport'})),
            ("CSS Framework", 'bootstrap' in str(soup).lower() or 'tailwind' in str(soup).lower() or 'css' in str(soup).lower()),
            ("Mobile Menu", soup.find('button', class_='navbar-toggler') or soup.find('div', class_='mobile-menu')),
            ("Responsive Images", soup.find('img', attrs={'class': re.compile('responsive|img-fluid', re.I)})),
        ]
        
        passed_checks = sum(1 for _, check in checks if check)
        
        if passed_checks >= 2:
            self.log_test_result("Responsive Design", True, f"{passed_checks}/4 elements found")
            return True
        else:
            failed_checks = [name for name, check in checks if not check]
            self.log_test_result("Responsive Design", False, f"Missing: {', '.join(failed_checks)}")
            return False
    
    def test_navigation_menu_functionality(self) -> bool:
        """Test 7: Test navigation menu links and functionality."""
        logger.info("🧭 Testing Navigation Menu Functionality")
        
        # Get home page
        result = self.get_page_content(f"{self.base_url}/")
        
        if not result["success"]:
            self.log_test_result("Navigation Menu", False, f"Status: {result['status_code']}")
            return False
        
        soup = result["soup"]
        
        # Find navigation links
        nav_links = []
        
        # Look for common navigation patterns
        nav_selectors = [
            'nav a',
            '.navbar a',
            '.nav a',
            'ul.nav li a',
            'header a',
            '.menu a'
        ]
        
        for selector in nav_selectors:
            links = soup.select(selector)
            if links:
                nav_links.extend(links)
                break
        
        if not nav_links:
            # Fallback: look for any links that might be navigation
            all_links = soup.find_all('a', href=True)
            nav_links = [link for link in all_links if not link.get('href', '').startswith('http')]
        
        if nav_links:
            # Test a few key navigation links
            key_pages = ['/materials', '/projects', '/calculator', '/about', '/contact']
            working_links = 0
            
            for link in nav_links[:5]:  # Test first 5 links
                href = link.get('href', '')
                if href:
                    # Test if link works
                    test_url = f"{self.base_url}{href}" if href.startswith('/') else href
                    if test_url.startswith(self.base_url):
                        try:
                            response = self.session.get(test_url, timeout=5)
                            if response.status_code == 200:
                                working_links += 1
                        except:
                            pass
            
            if working_links >= 2:
                self.log_test_result("Navigation Menu", True, f"{working_links} working links found")
                return True
            else:
                self.log_test_result("Navigation Menu", False, f"Only {working_links} working links")
                return False
        else:
            self.log_test_result("Navigation Menu", False, "No navigation links found")
            return False
    
    def test_page_load_performance(self) -> bool:
        """Test 8: Test page load performance for user experience."""
        logger.info("⚡ Testing Page Load Performance")
        
        # Test multiple pages
        test_pages = ['/', '/materials', '/projects']
        total_time = 0
        successful_loads = 0
        
        for page in test_pages:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{page}")
                end_time = time.time()
                
                if response.status_code == 200:
                    load_time = end_time - start_time
                    total_time += load_time
                    successful_loads += 1
                    logger.info(f"  {page}: {load_time:.2f}s")
                else:
                    logger.info(f"  {page}: Failed (status {response.status_code})")
                    
            except Exception as e:
                logger.info(f"  {page}: Error - {str(e)}")
        
        if successful_loads >= 2:
            avg_load_time = total_time / successful_loads
            if avg_load_time < 3.0:  # 3 second threshold
                self.log_test_result("Page Load Performance", True, f"Average: {avg_load_time:.2f}s")
                return True
            else:
                self.log_test_result("Page Load Performance", False, f"Slow: {avg_load_time:.2f}s")
                return False
        else:
            self.log_test_result("Page Load Performance", False, f"Only {successful_loads} pages loaded")
            return False
    
    def test_user_workflow_complete(self) -> bool:
        """Test 9: Complete user workflow from home to calculation."""
        logger.info("🔄 Testing Complete User Workflow")
        
        workflow_steps = [
            ("Home Page", f"{self.base_url}/"),
            ("Materials Page", f"{self.base_url}/materials"),
            ("Projects Page", f"{self.base_url}/projects"),
            ("Calculator", f"{self.base_url}/calculator"),
        ]
        
        successful_steps = 0
        
        for step_name, url in workflow_steps:
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    successful_steps += 1
                    logger.info(f"  ✅ {step_name}: Accessible")
                else:
                    logger.info(f"  ❌ {step_name}: Status {response.status_code}")
            except Exception as e:
                logger.info(f"  ❌ {step_name}: Error - {str(e)}")
        
        if successful_steps >= 3:
            self.log_test_result("Complete User Workflow", True, f"{successful_steps}/4 steps successful")
            return True
        else:
            self.log_test_result("Complete User Workflow", False, f"Only {successful_steps}/4 steps successful")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all user navigation tests and return results."""
        logger.info("🚀 Starting User Navigation Acceptance Tests")
        logger.info("=" * 60)
        
        tests = [
            ("Home Page Navigation", self.test_home_page_navigation),
            ("Materials Page Workflow", self.test_materials_page_user_workflow),
            ("Projects Page Workflow", self.test_projects_page_user_workflow),
            ("Calculator Web Interface", self.test_materials_calculator_web_interface),
            ("Calculator Form Submission", self.test_materials_calculator_form_submission),
            ("Responsive Design", self.test_responsive_design_elements),
            ("Navigation Menu", self.test_navigation_menu_functionality),
            ("Page Load Performance", self.test_page_load_performance),
            ("Complete User Workflow", self.test_user_workflow_complete),
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
        logger.info("\n" + "=" * 60)
        logger.info("📊 USER NAVIGATION TEST SUMMARY")
        logger.info("=" * 60)
        
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            logger.info(f"{status} - {result['test']}")
            if result["details"]:
                logger.info(f"   {result['details']}")
        
        success_rate = (passed_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            logger.info("🎉 USER NAVIGATION TESTS PASSED - Application is user-friendly!")
        elif success_rate >= 60:
            logger.info("⚠️  USER NAVIGATION TESTS PARTIALLY PASSED - Some UX issues need attention")
        else:
            logger.error("❌ USER NAVIGATION TESTS FAILED - Major UX issues need to be addressed")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "results": self.test_results,
            "overall_passed": success_rate >= 80
        }

def main():
    """Main function to run user navigation tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Landscaper User Navigation Tests")
    parser.add_argument("--url", default="http://localhost:5000", 
                       help="Base URL of the application")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run tests
    tester = UserNavigationTests(args.url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_passed"] else 1)

if __name__ == "__main__":
    main()
