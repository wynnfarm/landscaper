#!/usr/bin/env python3
"""
Comprehensive Route Content Acceptance Tests for Landscaper Application

This test suite specifically checks for routing issues and content differentiation:
1. Verifies each route serves different content
2. Checks for proper page titles and headers
3. Validates route-specific functionality
4. Identifies duplicate or missing content
5. Tests navigation between different sections
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List, Set
import logging
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RouteContentTests:
    """Comprehensive test suite for route content differentiation."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 10
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.page_contents = {}  # Store page contents for comparison
        
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
                "url": response.url,
                "final_url": response.url  # Track redirects
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": "",
                "soup": None,
                "url": url,
                "final_url": url
            }
    
    def extract_page_signature(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract unique identifiers for a page."""
        if not soup:
            return {}
        
        # Get page title
        title = soup.title.text.strip() if soup.title else ""
        
        # Get main heading
        h1 = soup.find('h1')
        h1_text = h1.text.strip() if h1 else ""
        
        # Get page-specific content indicators
        content_indicators = {
            "has_materials_table": bool(soup.find('table') and 'material' in str(soup).lower()),
            "has_calculator_form": bool(soup.find('form') and ('calculator' in str(soup).lower() or 'wall' in str(soup).lower())),
            "has_projects_section": bool('project' in str(soup).lower() and ('active' in str(soup).lower() or 'completed' in str(soup).lower())),
            "has_navigation": bool(soup.find('nav') or soup.find('ul', class_='nav')),
            "has_footer": bool(soup.find('footer')),
            "word_count": len(soup.get_text().split()),
            "unique_words": len(set(soup.get_text().lower().split()))
        }
        
        return {
            "title": title,
            "h1": h1_text,
            "content_indicators": content_indicators,
            "url_path": urlparse(soup.find('base')['href']).path if soup.find('base') else ""
        }
    
    def test_route_content_differentiation(self) -> bool:
        """Test 1: Verify each route serves different content."""
        logger.info("🛣️ Testing Route Content Differentiation")
        
        routes = [
            ("/", "Home Page"),
            ("/materials", "Materials Page"),
            ("/projects", "Projects Page"),
            ("/calculator", "Calculator Page"),
            ("/chat", "Chat Page"),
        ]
        
        page_signatures = {}
        content_similarities = []
        
        # Get content for all routes
        for route, route_name in routes:
            result = self.get_page_content(f"{self.base_url}{route}")
            if result["success"]:
                signature = self.extract_page_signature(result["soup"])
                page_signatures[route] = signature
                self.page_contents[route] = result["content"]
                logger.info(f"  📄 {route_name}: '{signature['title']}' - {signature['content_indicators']['word_count']} words")
            else:
                logger.info(f"  ❌ {route_name}: Failed to load (status {result['status_code']})")
        
        # Compare content between routes
        routes_list = list(page_signatures.keys())
        for i, route1 in enumerate(routes_list):
            for route2 in routes_list[i+1:]:
                sig1 = page_signatures[route1]
                sig2 = page_signatures[route2]
                
                # Check for identical titles
                if sig1["title"] == sig2["title"] and sig1["title"]:
                    content_similarities.append(f"Same title '{sig1['title']}' on {route1} and {route2}")
                
                # Check for identical content
                if self.page_contents[route1] == self.page_contents[route2]:
                    content_similarities.append(f"Identical content on {route1} and {route2}")
                
                # Check for very similar word counts (within 10%)
                word_count1 = sig1["content_indicators"]["word_count"]
                word_count2 = sig2["content_indicators"]["word_count"]
                if word_count1 > 0 and word_count2 > 0:
                    similarity = min(word_count1, word_count2) / max(word_count1, word_count2)
                    if similarity > 0.9:
                        content_similarities.append(f"Very similar content length on {route1} ({word_count1} words) and {route2} ({word_count2} words)")
        
        if content_similarities:
            self.log_test_result("Route Content Differentiation", False, f"Found {len(content_similarities)} content similarities: {'; '.join(content_similarities[:3])}")
            return False
        else:
            self.log_test_result("Route Content Differentiation", True, f"All {len(routes)} routes have unique content")
            return True
    
    def test_page_titles_and_headers(self) -> bool:
        """Test 2: Verify each page has appropriate title and header."""
        logger.info("📝 Testing Page Titles and Headers")
        
        expected_titles = {
            "/": "Landscaper",
            "/materials": "Materials",
            "/projects": "Projects", 
            "/calculator": "Calculator",
            "/chat": "Chat"
        }
        
        passed_checks = 0
        total_checks = len(expected_titles)
        
        for route, expected_keyword in expected_titles.items():
            result = self.get_page_content(f"{self.base_url}{route}")
            if result["success"]:
                soup = result["soup"]
                title = soup.title.text.strip() if soup.title else ""
                h1 = soup.find('h1')
                h1_text = h1.text.strip() if h1 else ""
                
                # Check if title contains expected keyword
                title_match = expected_keyword.lower() in title.lower()
                h1_match = expected_keyword.lower() in h1_text.lower()
                
                if title_match or h1_match:
                    passed_checks += 1
                    logger.info(f"  ✅ {route}: Title='{title[:50]}...' H1='{h1_text[:30]}...'")
                else:
                    logger.info(f"  ❌ {route}: Title='{title[:50]}...' H1='{h1_text[:30]}...' (missing '{expected_keyword}')")
            else:
                logger.info(f"  ❌ {route}: Failed to load")
        
        success = passed_checks >= total_checks * 0.8  # 80% threshold
        self.log_test_result("Page Titles and Headers", success, f"{passed_checks}/{total_checks} pages have appropriate titles/headers")
        return success
    
    def test_route_specific_functionality(self) -> bool:
        """Test 3: Verify each route has its specific functionality."""
        logger.info("🔧 Testing Route-Specific Functionality")
        
        functionality_tests = [
            ("/materials", [
                ("Materials Table", lambda soup: bool(soup.find('table'))),
                ("Search Input", lambda soup: bool(soup.find('input', attrs={'placeholder': re.compile('search', re.I)}))),
                ("Add Material Button", lambda soup: bool(soup.find('button', string=re.compile('add', re.I)))),
                ("Material Types", lambda soup: bool(soup.find('select') or 'material' in str(soup).lower()))
            ]),
            ("/calculator", [
                ("Calculator Form", lambda soup: bool(soup.find('form'))),
                ("Wall Length Input", lambda soup: bool(soup.find('input', attrs={'id': 'wall-length'}))),
                ("Wall Height Input", lambda soup: bool(soup.find('input', attrs={'id': 'wall-height'}))),
                ("Calculate Button", lambda soup: bool(soup.find('button', string=re.compile('calculate', re.I))))
            ]),
            ("/projects", [
                ("Projects Section", lambda soup: bool('project' in str(soup).lower())),
                ("Active Projects", lambda soup: bool('active' in str(soup).lower())),
                ("Completed Projects", lambda soup: bool('completed' in str(soup).lower()))
            ])
        ]
        
        total_passed = 0
        total_checks = 0
        
        for route, tests in functionality_tests:
            result = self.get_page_content(f"{self.base_url}{route}")
            if result["success"]:
                soup = result["soup"]
                route_passed = 0
                
                for test_name, test_func in tests:
                    total_checks += 1
                    if test_func(soup):
                        route_passed += 1
                        total_passed += 1
                        logger.info(f"  ✅ {route} - {test_name}")
                    else:
                        logger.info(f"  ❌ {route} - {test_name}")
                
                logger.info(f"  📊 {route}: {route_passed}/{len(tests)} functionality checks passed")
            else:
                logger.info(f"  ❌ {route}: Failed to load")
                total_checks += len(tests)
        
        success = total_passed >= total_checks * 0.7  # 70% threshold
        self.log_test_result("Route-Specific Functionality", success, f"{total_passed}/{total_checks} functionality checks passed")
        return success
    
    def test_navigation_consistency(self) -> bool:
        """Test 4: Verify navigation links work and lead to different pages."""
        logger.info("🧭 Testing Navigation Consistency")
        
        # Get home page to extract navigation links
        result = self.get_page_content(f"{self.base_url}/")
        if not result["success"]:
            self.log_test_result("Navigation Consistency", False, "Cannot load home page")
            return False
        
        soup = result["soup"]
        
        # Find navigation links
        nav_links = []
        nav_selectors = ['nav a', '.navbar a', '.nav a', 'ul.nav li a', 'header a']
        
        for selector in nav_selectors:
            links = soup.select(selector)
            if links:
                nav_links.extend(links)
                break
        
        if not nav_links:
            # Fallback: look for any links
            nav_links = soup.find_all('a', href=True)
        
        # Test navigation links
        working_links = 0
        link_destinations = {}
        
        for link in nav_links[:6]:  # Test first 6 links
            href = link.get('href', '')
            if href:
                # Normalize URL
                if href.startswith('/'):
                    test_url = f"{self.base_url}{href}"
                elif href.startswith(self.base_url):
                    test_url = href
                else:
                    continue
                
                try:
                    response = self.session.get(test_url, timeout=5)
                    if response.status_code == 200:
                        working_links += 1
                        link_destinations[href] = response.url
                        logger.info(f"  ✅ {href} -> {response.url}")
                    else:
                        logger.info(f"  ❌ {href} -> Status {response.status_code}")
                except Exception as e:
                    logger.info(f"  ❌ {href} -> Error: {str(e)}")
        
        # Check if links lead to different destinations
        unique_destinations = len(set(link_destinations.values()))
        if unique_destinations < len(link_destinations) * 0.8:  # 80% should be unique
            self.log_test_result("Navigation Consistency", False, f"Only {unique_destinations} unique destinations from {len(link_destinations)} links")
            return False
        
        success = working_links >= 3  # At least 3 working links
        self.log_test_result("Navigation Consistency", success, f"{working_links} working navigation links, {unique_destinations} unique destinations")
        return success
    
    def test_content_uniqueness_detailed(self) -> bool:
        """Test 5: Detailed content uniqueness analysis."""
        logger.info("🔍 Testing Content Uniqueness (Detailed)")
        
        if not self.page_contents:
            self.log_test_result("Content Uniqueness Detailed", False, "No page contents available")
            return False
        
        # Analyze content similarity
        routes = list(self.page_contents.keys())
        similarity_issues = []
        
        for i, route1 in enumerate(routes):
            for route2 in routes[i+1:]:
                content1 = self.page_contents[route1]
                content2 = self.page_contents[route2]
                
                # Check for exact content match
                if content1 == content2:
                    similarity_issues.append(f"EXACT MATCH: {route1} and {route2}")
                    continue
                
                # Check for high similarity (>90% same words)
                words1 = set(re.findall(r'\b\w+\b', content1.lower()))
                words2 = set(re.findall(r'\b\w+\b', content2.lower()))
                
                if words1 and words2:
                    common_words = words1.intersection(words2)
                    similarity = len(common_words) / max(len(words1), len(words2))
                    
                    if similarity > 0.9:
                        similarity_issues.append(f"HIGH SIMILARITY ({similarity:.1%}): {route1} and {route2}")
                
                # Check for same main content structure
                soup1 = BeautifulSoup(content1, 'html.parser')
                soup2 = BeautifulSoup(content2, 'html.parser')
                
                # Compare main content areas
                main1 = soup1.find('main') or soup1.find('div', class_='container')
                main2 = soup2.find('main') or soup2.find('div', class_='container')
                
                if main1 and main2:
                    main_text1 = main1.get_text().strip()
                    main_text2 = main2.get_text().strip()
                    
                    if main_text1 == main_text2 and len(main_text1) > 100:
                        similarity_issues.append(f"SAME MAIN CONTENT: {route1} and {route2}")
        
        if similarity_issues:
            self.log_test_result("Content Uniqueness Detailed", False, f"Found {len(similarity_issues)} similarity issues: {'; '.join(similarity_issues[:3])}")
            return False
        else:
            self.log_test_result("Content Uniqueness Detailed", True, f"All {len(routes)} routes have unique content")
            return True
    
    def test_route_redirects_and_status(self) -> bool:
        """Test 6: Check for proper redirects and status codes."""
        logger.info("🔄 Testing Route Redirects and Status")
        
        routes = ["/", "/materials", "/projects", "/calculator", "/chat", "/nonexistent"]
        
        proper_responses = 0
        redirect_issues = []
        
        for route in routes:
            try:
                response = self.session.get(f"{self.base_url}{route}", allow_redirects=False)
                
                if response.status_code == 200:
                    proper_responses += 1
                    logger.info(f"  ✅ {route}: 200 OK")
                elif response.status_code in [301, 302, 307, 308]:
                    # Check if redirect is appropriate
                    redirect_url = response.headers.get('Location', '')
                    if redirect_url and redirect_url != f"{self.base_url}{route}":
                        logger.info(f"  ⚠️ {route}: {response.status_code} -> {redirect_url}")
                    else:
                        redirect_issues.append(f"Invalid redirect on {route}")
                        logger.info(f"  ❌ {route}: Invalid redirect")
                elif response.status_code == 404:
                    if route == "/nonexistent":
                        proper_responses += 1  # Expected 404
                        logger.info(f"  ✅ {route}: 404 (expected)")
                    else:
                        logger.info(f"  ❌ {route}: 404 (unexpected)")
                else:
                    logger.info(f"  ❌ {route}: {response.status_code}")
                    
            except Exception as e:
                logger.info(f"  ❌ {route}: Error - {str(e)}")
        
        success = proper_responses >= len(routes) * 0.8 and not redirect_issues
        self.log_test_result("Route Redirects and Status", success, f"{proper_responses}/{len(routes)} proper responses")
        return success
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all route content tests and return results."""
        logger.info("🚀 Starting Comprehensive Route Content Tests")
        logger.info("=" * 70)
        
        tests = [
            ("Route Content Differentiation", self.test_route_content_differentiation),
            ("Page Titles and Headers", self.test_page_titles_and_headers),
            ("Route-Specific Functionality", self.test_route_specific_functionality),
            ("Navigation Consistency", self.test_navigation_consistency),
            ("Content Uniqueness Detailed", self.test_content_uniqueness_detailed),
            ("Route Redirects and Status", self.test_route_redirects_and_status),
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
        logger.info("\n" + "=" * 70)
        logger.info("📊 ROUTE CONTENT TEST SUMMARY")
        logger.info("=" * 70)
        
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            logger.info(f"{status} - {result['test']}")
            if result["details"]:
                logger.info(f"   {result['details']}")
        
        success_rate = (passed_tests / total_tests) * 100
        logger.info(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            logger.info("🎉 ROUTE CONTENT TESTS PASSED - Routes are properly differentiated!")
        elif success_rate >= 60:
            logger.info("⚠️  ROUTE CONTENT TESTS PARTIALLY PASSED - Some routing issues need attention")
        else:
            logger.error("❌ ROUTE CONTENT TESTS FAILED - Major routing issues need to be addressed")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "results": self.test_results,
            "overall_passed": success_rate >= 80
        }

def main():
    """Main function to run route content tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Landscaper Route Content Tests")
    parser.add_argument("--url", default="http://localhost:5000", 
                       help="Base URL of the application")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run tests
    tester = RouteContentTests(args.url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_passed"] else 1)

if __name__ == "__main__":
    main()
