#!/usr/bin/env python3
"""
Detailed Route Content Analysis for Landscaper Application

This script provides a detailed analysis of what content each route serves,
helping to identify any routing issues or content duplication.
"""

import requests
import json
import sys
from bs4 import BeautifulSoup
import re

def analyze_route_content(base_url="http://localhost:5000"):
    """Analyze content for each route in detail."""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    routes = [
        ("/", "Home Page"),
        ("/materials", "Materials Page"),
        ("/projects", "Projects Page"),
        ("/calculator", "Calculator Page"),
        ("/chat", "Chat Page"),
        ("/crew", "Crew Page"),
        ("/tools", "Tools Page"),
    ]
    
    print("🔍 DETAILED ROUTE CONTENT ANALYSIS")
    print("=" * 60)
    
    route_data = {}
    
    for route, route_name in routes:
        print(f"\n📄 {route_name} ({route})")
        print("-" * 40)
        
        try:
            response = session.get(f"{base_url}{route}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract key information
                title = soup.title.text.strip() if soup.title else "No title"
                h1 = soup.find('h1')
                h1_text = h1.text.strip() if h1 else "No H1"
                
                # Get main content area
                main_content = soup.find('main') or soup.find('div', class_='container')
                main_text = main_content.get_text().strip()[:200] + "..." if main_content else "No main content"
                
                # Count elements
                tables = len(soup.find_all('table'))
                forms = len(soup.find_all('form'))
                buttons = len(soup.find_all('button'))
                inputs = len(soup.find_all('input'))
                
                # Word count
                all_text = soup.get_text()
                word_count = len(all_text.split())
                
                print(f"Title: {title}")
                print(f"H1: {h1_text}")
                print(f"Word Count: {word_count}")
                print(f"Tables: {tables}")
                print(f"Forms: {forms}")
                print(f"Buttons: {buttons}")
                print(f"Inputs: {inputs}")
                print(f"Main Content Preview: {main_text}")
                
                # Store for comparison
                route_data[route] = {
                    "title": title,
                    "h1": h1_text,
                    "word_count": word_count,
                    "tables": tables,
                    "forms": forms,
                    "buttons": buttons,
                    "inputs": inputs,
                    "content_hash": hash(all_text)
                }
                
            else:
                print(f"❌ Status: {response.status_code}")
                route_data[route] = {"error": f"Status {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            route_data[route] = {"error": str(e)}
    
    # Content similarity analysis
    print(f"\n🔍 CONTENT SIMILARITY ANALYSIS")
    print("=" * 60)
    
    routes_list = list(route_data.keys())
    similarities = []
    
    for i, route1 in enumerate(routes_list):
        for route2 in routes_list[i+1:]:
            data1 = route_data[route1]
            data2 = route_data[route2]
            
            if "error" in data1 or "error" in data2:
                continue
            
            # Check for identical titles
            if data1["title"] == data2["title"]:
                similarities.append(f"Same title '{data1['title']}' on {route1} and {route2}")
            
            # Check for identical H1
            if data1["h1"] == data2["h1"]:
                similarities.append(f"Same H1 '{data1['h1']}' on {route1} and {route2}")
            
            # Check for identical content hash
            if data1["content_hash"] == data2["content_hash"]:
                similarities.append(f"Identical content on {route1} and {route2}")
            
            # Check for very similar word counts
            if data1["word_count"] > 0 and data2["word_count"] > 0:
                similarity = min(data1["word_count"], data2["word_count"]) / max(data1["word_count"], data2["word_count"])
                if similarity > 0.9:
                    similarities.append(f"Very similar word count: {route1} ({data1['word_count']}) vs {route2} ({data2['word_count']}) - {similarity:.1%}")
    
    if similarities:
        print("❌ SIMILARITY ISSUES FOUND:")
        for similarity in similarities:
            print(f"  • {similarity}")
    else:
        print("✅ No content similarities detected")
    
    # Route functionality summary
    print(f"\n📊 ROUTE FUNCTIONALITY SUMMARY")
    print("=" * 60)
    
    for route, data in route_data.items():
        if "error" in data:
            print(f"{route}: ❌ {data['error']}")
        else:
            functionality = []
            if data["tables"] > 0:
                functionality.append(f"Tables: {data['tables']}")
            if data["forms"] > 0:
                functionality.append(f"Forms: {data['forms']}")
            if data["buttons"] > 0:
                functionality.append(f"Buttons: {data['buttons']}")
            if data["inputs"] > 0:
                functionality.append(f"Inputs: {data['inputs']}")
            
            print(f"{route}: ✅ {data['word_count']} words - {', '.join(functionality)}")
    
    return route_data

def check_specific_issues():
    """Check for specific routing issues."""
    print(f"\n🔧 SPECIFIC ISSUE CHECKING")
    print("=" * 60)
    
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    # Check if all routes return the same template
    routes = ["/", "/materials", "/projects", "/calculator", "/chat"]
    
    templates_used = {}
    
    for route in routes:
        try:
            response = session.get(f"{base_url}{route}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for template indicators
                template_indicators = []
                
                # Check for specific page content
                if soup.find('table') and 'material' in str(soup).lower():
                    template_indicators.append("materials_template")
                if soup.find('form') and ('calculator' in str(soup).lower() or 'wall' in str(soup).lower()):
                    template_indicators.append("calculator_template")
                if 'project' in str(soup).lower() and ('active' in str(soup).lower() or 'completed' in str(soup).lower()):
                    template_indicators.append("projects_template")
                if 'chat' in str(soup).lower() or 'ai' in str(soup).lower():
                    template_indicators.append("chat_template")
                if not template_indicators:
                    template_indicators.append("generic_template")
                
                templates_used[route] = template_indicators
                print(f"{route}: {', '.join(template_indicators)}")
                
        except Exception as e:
            print(f"{route}: Error - {str(e)}")
    
    # Check for template reuse
    template_counts = {}
    for route, templates in templates_used.items():
        for template in templates:
            template_counts[template] = template_counts.get(template, 0) + 1
    
    print(f"\nTemplate Usage:")
    for template, count in template_counts.items():
        if count > 1:
            print(f"  ⚠️ {template}: used {count} times")
        else:
            print(f"  ✅ {template}: used {count} time")

if __name__ == "__main__":
    print("🚀 Starting Detailed Route Content Analysis")
    print("=" * 60)
    
    route_data = analyze_route_content()
    check_specific_issues()
    
    print(f"\n✅ Analysis Complete!")
    print("If you're seeing the same content on different routes,")
    print("the issue might be in the browser cache or a client-side routing problem.")
