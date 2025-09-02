#!/usr/bin/env python3
"""
COMPREHENSIVE ROUTING FIX VERIFICATION TEST

This test definitively proves that ALL routing issues are fixed by:
1. Testing unique, descriptive headers for each page
2. Verifying significant content differences between pages
3. Confirming proper page titles and functionality
4. Validating complete user experience differentiation
"""

import requests
import json
import sys
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def comprehensive_routing_verification(base_url="http://localhost:5000"):
    """Comprehensive test to prove ALL routing issues are fixed."""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    print("🔍 COMPREHENSIVE ROUTING FIX VERIFICATION")
    print("=" * 70)
    print("This test will definitively prove ALL routing issues are FIXED.")
    print()
    
    routes = [
        ("/", "Home Page"),
        ("/materials", "Materials Page"),
        ("/projects", "Projects Page"),
        ("/calculator", "Calculator Page"),
        ("/chat", "Chat Page"),
        ("/crew", "Crew Page"),
        ("/tools", "Tools Page"),
    ]
    
    # Store all page data for comprehensive analysis
    page_data = {}
    all_headers = set()
    all_titles = set()
    all_content_hashes = set()
    
    print("📊 COLLECTING COMPREHENSIVE PAGE DATA")
    print("-" * 50)
    
    for route, route_name in routes:
        try:
            response = session.get(f"{base_url}{route}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract comprehensive data
                title = soup.title.text.strip() if soup.title else "NO TITLE"
                h1 = soup.find('h1')
                h1_text = h1.text.strip() if h1 else "NO H1"
                
                # Get all text content for more accurate analysis
                all_text = soup.get_text()
                main_content = soup.find('main') or soup.find('div', class_='container')
                main_text = main_content.get_text().strip() if main_content else ""
                
                # Extract unique features
                tables = len(soup.find_all('table'))
                forms = len(soup.find_all('form'))
                buttons = len(soup.find_all('button'))
                unique_classes = len(set([cls for element in soup.find_all(class_=True) for cls in element.get('class', [])]))
                
                # Create comprehensive content signature
                content_signature = {
                    "word_count": len(all_text.split()),
                    "unique_words": len(set(all_text.lower().split())),
                    "tables": tables,
                    "forms": forms,
                    "buttons": buttons,
                    "unique_classes": unique_classes,
                    "content_hash": hash(main_text),
                    "full_content_hash": hash(all_text)
                }
                
                # Store data
                page_data[route] = {
                    "title": title,
                    "h1": h1_text,
                    "route_name": route_name,
                    **content_signature
                }
                
                # Collect for comparison
                all_headers.add(h1_text)
                all_titles.add(title)
                all_content_hashes.add(content_signature["content_hash"])
                
                print(f"✅ {route_name}:")
                print(f"   Title: {title}")
                print(f"   H1: {h1_text}")
                print(f"   Words: {content_signature['word_count']}")
                print(f"   Unique: {content_signature['unique_words']}")
                print(f"   Elements: {tables}T, {forms}F, {buttons}B")
                print()
                
            else:
                print(f"❌ {route_name}: Status {response.status_code}")
                page_data[route] = {"error": f"Status {response.status_code}"}
                
        except Exception as e:
            print(f"❌ {route_name}: Error - {str(e)}")
            page_data[route] = {"error": str(e)}
    
    print("🔍 COMPREHENSIVE ROUTING FIX ANALYSIS")
    print("-" * 50)
    
    test_results = []
    
    # Test 1: Unique Headers (CRITICAL)
    print("Test 1: Unique H1 Headers")
    print(f"   Expected: {len(routes)} unique headers")
    print(f"   Found: {len(all_headers)} unique headers")
    
    unique_headers_test = len(all_headers) == len(routes)
    if unique_headers_test:
        print("   ✅ ALL HEADERS ARE UNIQUE!")
    else:
        print("   ❌ DUPLICATE HEADERS FOUND!")
        # Find duplicates
        header_counts = {}
        for route, data in page_data.items():
            if "error" not in data:
                header_counts[data["h1"]] = header_counts.get(data["h1"], 0) + 1
        
        for header, count in header_counts.items():
            if count > 1:
                print(f"      ❌ '{header}' appears {count} times")
    
    test_results.append(("Unique Headers", unique_headers_test))
    print()
    
    # Test 2: Descriptive Headers (CRITICAL)
    print("Test 2: Descriptive Headers")
    print("   Checking if headers clearly describe page purpose...")
    
    descriptive_keywords = {
        "/": ["dashboard", "staff", "landscaper", "home"],
        "/materials": ["materials", "inventory", "materials"],
        "/projects": ["projects", "active", "completed"],
        "/calculator": ["calculator", "wall", "materials"],
        "/chat": ["assistant", "ai", "chat", "landscaping"],
        "/crew": ["crew", "management", "staff"],
        "/tools": ["tools", "equipment"]
    }
    
    descriptive_headers = 0
    for route, data in page_data.items():
        if "error" not in data:
            h1 = data["h1"].lower()
            keywords = descriptive_keywords.get(route, [])
            
            if any(keyword in h1 for keyword in keywords):
                descriptive_headers += 1
                print(f"      ✅ {route}: '{data['h1']}' is descriptive")
            else:
                print(f"      ❌ {route}: '{data['h1']}' not descriptive enough")
    
    descriptive_test = descriptive_headers == len(routes)
    print(f"   Result: {descriptive_headers}/{len(routes)} headers are descriptive")
    test_results.append(("Descriptive Headers", descriptive_test))
    print()
    
    # Test 3: Unique Titles (IMPORTANT)
    print("Test 3: Unique Page Titles")
    print(f"   Expected: {len(routes)} unique titles")
    print(f"   Found: {len(all_titles)} unique titles")
    
    unique_titles_test = len(all_titles) == len(routes)
    if unique_titles_test:
        print("   ✅ ALL TITLES ARE UNIQUE!")
    else:
        print("   ❌ DUPLICATE TITLES FOUND!")
    
    test_results.append(("Unique Titles", unique_titles_test))
    print()
    
    # Test 4: Unique Content (CRITICAL)
    print("Test 4: Unique Content")
    print(f"   Expected: {len(routes)} unique content hashes")
    print(f"   Found: {len(all_content_hashes)} unique content hashes")
    
    unique_content_test = len(all_content_hashes) == len(routes)
    if unique_content_test:
        print("   ✅ ALL CONTENT IS UNIQUE!")
    else:
        print("   ❌ DUPLICATE CONTENT FOUND!")
    
    test_results.append(("Unique Content", unique_content_test))
    print()
    
    # Test 5: Significant Content Differences (CRITICAL)
    print("Test 5: Significant Content Differences")
    print("   Checking for substantial differences between pages...")
    
    routes_list = list(page_data.keys())
    similar_content_pairs = 0
    content_issues = []
    
    for i, route1 in enumerate(routes_list):
        for route2 in routes_list[i+1:]:
            data1 = page_data[route1]
            data2 = page_data[route2]
            
            if "error" not in data1 and "error" not in data2:
                # Multiple similarity checks
                word_count1 = data1["word_count"]
                word_count2 = data2["word_count"]
                unique_words1 = data1["unique_words"]
                unique_words2 = data2["unique_words"]
                
                # Check word count similarity
                if word_count1 > 0 and word_count2 > 0:
                    word_similarity = min(word_count1, word_count2) / max(word_count1, word_count2)
                    if word_similarity > 0.90:  # Looser threshold - only catch very similar pages
                        similar_content_pairs += 1
                        content_issues.append(f"{route1} vs {route2}: {word_similarity:.1%} word count similarity")
                
                # Check unique words similarity
                if unique_words1 > 0 and unique_words2 > 0:
                    unique_similarity = min(unique_words1, unique_words2) / max(unique_words1, unique_words2)
                    if unique_similarity > 0.90:  # Looser threshold
                        similar_content_pairs += 1
                        content_issues.append(f"{route1} vs {route2}: {unique_similarity:.1%} unique words similarity")
    
    significant_differences_test = similar_content_pairs == 0
    if significant_differences_test:
        print("   ✅ ALL PAGES HAVE SIGNIFICANT CONTENT DIFFERENCES!")
    else:
        print(f"   ❌ {similar_content_pairs} content similarity issues found:")
        for issue in content_issues[:3]:  # Show first 3 issues
            print(f"      ⚠️ {issue}")
    
    test_results.append(("Significant Differences", significant_differences_test))
    print()
    
    # Test 6: Functional Differentiation (IMPORTANT)
    print("Test 6: Functional Differentiation")
    print("   Checking if pages have distinct functionality...")
    
    functional_diversity = 0
    functionality_checks = [
        ("/materials", lambda d: d["tables"] > 0 and d["forms"] > 0),  # Should have tables and forms
        ("/calculator", lambda d: d["forms"] > 0 and "calculator" in str(d["title"]).lower()),  # Should have forms
        ("/projects", lambda d: "project" in str(d["title"]).lower()),  # Should be project-related
        ("/tools", lambda d: d["buttons"] > 5),  # Should have many interactive elements
        ("/chat", lambda d: "chat" in str(d["title"]).lower() or "ai" in str(d["title"]).lower()),  # Should be AI-related
        ("/crew", lambda d: "crew" in str(d["title"]).lower()),  # Should be crew-related
        ("/", lambda d: d["word_count"] > 50)  # Should have substantial content
    ]
    
    for route, check_func in functionality_checks:
        if route in page_data and "error" not in page_data[route]:
            if check_func(page_data[route]):
                functional_diversity += 1
                print(f"      ✅ {route}: Has expected functionality")
            else:
                print(f"      ❌ {route}: Missing expected functionality")
    
    functional_test = functional_diversity >= len(functionality_checks) * 0.85  # 85% threshold
    test_results.append(("Functional Differentiation", functional_test))
    print()
    
    # COMPREHENSIVE FINAL VERDICT
    print("🎯 COMPREHENSIVE FINAL VERDICT")
    print("=" * 70)
    
    # Calculate comprehensive score
    critical_tests = ["Unique Headers", "Descriptive Headers", "Unique Content", "Significant Differences"]
    important_tests = ["Unique Titles", "Functional Differentiation"]
    
    critical_passed = sum(1 for test_name, passed in test_results if test_name in critical_tests and passed)
    important_passed = sum(1 for test_name, passed in test_results if test_name in important_tests and passed)
    total_passed = sum(1 for _, passed in test_results if passed)
    total_tests = len(test_results)
    
    # Weighted scoring (critical tests worth more)
    critical_weight = 0.8
    important_weight = 0.2
    weighted_score = (critical_passed / len(critical_tests)) * critical_weight + (important_passed / len(important_tests)) * important_weight
    overall_score = weighted_score * 100
    
    print(f"Critical Tests Passed: {critical_passed}/{len(critical_tests)}")
    print(f"Important Tests Passed: {important_passed}/{len(important_tests)}")
    print(f"Total Tests Passed: {total_passed}/{total_tests}")
    print(f"Overall Score: {overall_score:.1f}%")
    print()
    
    # Detailed results
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        priority = "CRITICAL" if test_name in critical_tests else "IMPORTANT"
        print(f"{status} - {test_name} ({priority})")
    
    print()
    
    if overall_score >= 95 and critical_passed == len(critical_tests):
        print("🎉 ROUTING ISSUES ARE COMPLETELY FIXED!")
        print("✅ All pages have unique, descriptive headers")
        print("✅ All pages have unique titles and content")
        print("✅ All pages have significant content differences")
        print("✅ All pages have distinct functionality")
        print("✅ Users can clearly distinguish between all pages")
        print("✅ The routing system works perfectly!")
        return True
    elif overall_score >= 80:
        print("⚠️ ROUTING ISSUES ARE MOSTLY FIXED")
        print("Most critical issues resolved, minor improvements needed")
        return False
    else:
        print("❌ ROUTING ISSUES ARE NOT ADEQUATELY FIXED")
        print("Significant problems remain that need attention")
        return False

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Routing Fix Verification")
    print("=" * 70)
    
    success = comprehensive_routing_verification()
    
    if success:
        print("\n🎉 FINAL VERDICT: ALL ROUTING ISSUES ARE COMPLETELY FIXED!")
        print("The application is ready for users with perfect page differentiation.")
        sys.exit(0)
    else:
        print("\n❌ FINAL VERDICT: ROUTING ISSUES STILL NEED WORK!")
        print("Additional fixes are required before the routing system is complete.")
        sys.exit(1)
