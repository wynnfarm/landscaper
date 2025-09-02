#!/usr/bin/env python3
"""
DEFINITIVE ROUTING FIX VERIFICATION TEST

This test provides absolute proof that routing issues are fixed by:
1. Testing each route individually with detailed content analysis
2. Comparing headers, titles, and content between routes
3. Verifying no duplicate content exists
4. Confirming unique user experience for each page
"""

import requests
import json
import sys
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def test_routing_fixes_definitive(base_url="http://localhost:5000"):
    """Definitive test to prove routing issues are fixed."""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    print("🔍 DEFINITIVE ROUTING FIX VERIFICATION")
    print("=" * 60)
    print("This test will prove beyond doubt that routing issues are fixed.")
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
    
    # Store all page data for comparison
    page_data = {}
    all_headers = set()
    all_titles = set()
    all_content_hashes = set()
    
    print("📊 COLLECTING PAGE DATA")
    print("-" * 40)
    
    for route, route_name in routes:
        try:
            response = session.get(f"{base_url}{route}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract key data
                title = soup.title.text.strip() if soup.title else "NO TITLE"
                h1 = soup.find('h1')
                h1_text = h1.text.strip() if h1 else "NO H1"
                
                # Get main content (excluding header/nav/footer)
                main_content = soup.find('main') or soup.find('div', class_='container')
                main_text = main_content.get_text().strip() if main_content else ""
                
                # Create content hash for uniqueness check
                content_hash = hash(main_text)
                
                # Store data
                page_data[route] = {
                    "title": title,
                    "h1": h1_text,
                    "content_hash": content_hash,
                    "word_count": len(main_text.split()),
                    "route_name": route_name
                }
                
                # Collect for comparison
                all_headers.add(h1_text)
                all_titles.add(title)
                all_content_hashes.add(content_hash)
                
                print(f"✅ {route_name}:")
                print(f"   Title: {title}")
                print(f"   H1: {h1_text}")
                print(f"   Words: {len(main_text.split())}")
                print()
                
            else:
                print(f"❌ {route_name}: Status {response.status_code}")
                page_data[route] = {"error": f"Status {response.status_code}"}
                
        except Exception as e:
            print(f"❌ {route_name}: Error - {str(e)}")
            page_data[route] = {"error": str(e)}
    
    print("🔍 ANALYZING ROUTING FIXES")
    print("-" * 40)
    
    # Test 1: Unique Headers
    print("Test 1: Unique H1 Headers")
    print(f"   Expected: {len(routes)} unique headers")
    print(f"   Found: {len(all_headers)} unique headers")
    
    if len(all_headers) == len(routes):
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
    
    print()
    
    # Test 2: Unique Titles
    print("Test 2: Unique Page Titles")
    print(f"   Expected: {len(routes)} unique titles")
    print(f"   Found: {len(all_titles)} unique titles")
    
    if len(all_titles) == len(routes):
        print("   ✅ ALL TITLES ARE UNIQUE!")
    else:
        print("   ❌ DUPLICATE TITLES FOUND!")
        # Find duplicates
        title_counts = {}
        for route, data in page_data.items():
            if "error" not in data:
                title_counts[data["title"]] = title_counts.get(data["title"], 0) + 1
        
        for title, count in title_counts.items():
            if count > 1:
                print(f"      ❌ '{title}' appears {count} times")
    
    print()
    
    # Test 3: Unique Content
    print("Test 3: Unique Content")
    print(f"   Expected: {len(routes)} unique content hashes")
    print(f"   Found: {len(all_content_hashes)} unique content hashes")
    
    if len(all_content_hashes) == len(routes):
        print("   ✅ ALL CONTENT IS UNIQUE!")
    else:
        print("   ❌ DUPLICATE CONTENT FOUND!")
        # Find duplicates
        content_counts = {}
        for route, data in page_data.items():
            if "error" not in data:
                content_counts[data["content_hash"]] = content_counts.get(data["content_hash"], 0) + 1
        
        for content_hash, count in content_counts.items():
            if count > 1:
                print(f"      ❌ Content hash {content_hash} appears {count} times")
    
    print()
    
    # Test 4: Descriptive Headers
    print("Test 4: Descriptive Headers")
    print("   Checking if headers are descriptive and page-specific...")
    
    descriptive_headers = 0
    for route, data in page_data.items():
        if "error" not in data:
            h1 = data["h1"]
            route_name = data["route_name"]
            
            # Check if header contains relevant keywords
            if any(keyword in h1.lower() for keyword in route_name.lower().split()):
                descriptive_headers += 1
                print(f"      ✅ {route}: '{h1}' is descriptive")
            else:
                print(f"      ⚠️ {route}: '{h1}' may not be descriptive enough")
    
    print(f"   {descriptive_headers}/{len(routes)} headers are descriptive")
    print()
    
    # Test 5: Content Differentiation
    print("Test 5: Content Differentiation")
    print("   Checking if pages have sufficient content differences...")
    
    routes_list = list(page_data.keys())
    similar_pages = 0
    
    for i, route1 in enumerate(routes_list):
        for route2 in routes_list[i+1:]:
            data1 = page_data[route1]
            data2 = page_data[route2]
            
            if "error" not in data1 and "error" not in data2:
                # Check word count similarity
                word_count1 = data1["word_count"]
                word_count2 = data2["word_count"]
                
                if word_count1 > 0 and word_count2 > 0:
                    similarity = min(word_count1, word_count2) / max(word_count1, word_count2)
                    if similarity > 0.9:
                        similar_pages += 1
                        print(f"      ⚠️ {route1} vs {route2}: {similarity:.1%} similar word count")
    
    if similar_pages == 0:
        print("   ✅ ALL PAGES HAVE SUFFICIENT CONTENT DIFFERENCES!")
    else:
        print(f"   ⚠️ {similar_pages} page pairs have very similar content")
    
    print()
    
    # FINAL VERDICT
    print("🎯 FINAL VERDICT")
    print("=" * 60)
    
    # Calculate overall score
    tests_passed = 0
    total_tests = 5
    
    if len(all_headers) == len(routes):
        tests_passed += 1
    if len(all_titles) == len(routes):
        tests_passed += 1
    if len(all_content_hashes) == len(routes):
        tests_passed += 1
    if descriptive_headers >= len(routes) * 0.8:  # 80% threshold
        tests_passed += 1
    if similar_pages == 0:
        tests_passed += 1
    
    success_rate = (tests_passed / total_tests) * 100
    
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    print()
    
    if success_rate >= 90:
        print("🎉 ROUTING ISSUES ARE DEFINITIVELY FIXED!")
        print("✅ All pages have unique headers")
        print("✅ All pages have unique titles")
        print("✅ All pages have unique content")
        print("✅ Users can clearly distinguish between pages")
        return True
    elif success_rate >= 70:
        print("⚠️ ROUTING ISSUES ARE MOSTLY FIXED")
        print("Some minor issues remain but major problems are resolved")
        return False
    else:
        print("❌ ROUTING ISSUES ARE NOT FIXED")
        print("Significant problems remain")
        return False

if __name__ == "__main__":
    print("🚀 Starting Definitive Routing Fix Verification")
    print("=" * 60)
    
    success = test_routing_fixes_definitive()
    
    if success:
        print("\n✅ VERIFICATION COMPLETE: Routing issues are FIXED!")
        sys.exit(0)
    else:
        print("\n❌ VERIFICATION COMPLETE: Routing issues are NOT FIXED!")
        sys.exit(1)
