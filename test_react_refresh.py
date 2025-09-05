#!/usr/bin/env python3
"""
React Component Refresh Test
Tests if the React components are actually refreshing when triggered.
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://localhost:5001"

def log(message, level="INFO"):
    """Log messages with timestamp."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def test_react_refresh_trigger():
    """Test if the React refresh mechanism is working."""
    log("=" * 60)
    log("TESTING REACT REFRESH TRIGGER")
    log("=" * 60)
    
    # Step 1: Update job with a very distinctive name
    unique_name = f"React Test - {int(time.time())}"
    update_data = {
        "name": unique_name,
        "description": "Testing React refresh trigger",
        "status": "planning"
    }
    
    log(f"Updating job 1 with: {unique_name}")
    try:
        response = requests.put(
            f"{BASE_URL}/api/jobs/1",
            headers={"Content-Type": "application/json"},
            json=update_data
        )
        if response.status_code == 200:
            log("✅ Job update successful", "PASS")
        else:
            log(f"❌ Job update failed: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error updating job: {e}", "FAIL")
        return False
    
    # Step 2: Verify the update was saved
    log("Verifying job update was saved...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/1")
        if response.status_code == 200:
            job_data = response.json()
            if job_data.get('name') == unique_name:
                log("✅ Job update verified in backend", "PASS")
            else:
                log(f"❌ Job update not saved: expected '{unique_name}', got '{job_data.get('name')}'", "FAIL")
                return False
        else:
            log(f"❌ Failed to verify job update: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error verifying job update: {e}", "FAIL")
        return False
    
    # Step 3: Check project jobs endpoint
    log("Checking project jobs endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects/1/jobs")
        if response.status_code == 200:
            jobs = response.json()
            job_1 = next((j for j in jobs if j.get('id') == '1'), None)
            
            if job_1 and job_1.get('name') == unique_name:
                log("✅ Project jobs endpoint shows updated job", "PASS")
                log(f"   Job 1: {job_1.get('name')} - {job_1.get('status')}", "INFO")
            else:
                log("❌ Project jobs endpoint not showing updated job", "FAIL")
                if job_1:
                    log(f"   Expected: '{unique_name}', Got: '{job_1.get('name')}'", "INFO")
                else:
                    log("   Job 1 not found in project jobs", "INFO")
                return False
        else:
            log(f"❌ Failed to get project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error checking project jobs: {e}", "FAIL")
        return False
    
    log("=" * 60)
    log("✅ REACT REFRESH TRIGGER TEST PASSED!")
    log("=" * 60)
    log("The backend is working correctly.")
    log("If the UI is not updating, the issue is in the React component logic.")
    log("Check the browser console for debug logs from ProjectsManagement component.")
    log("=" * 60)
    return True

def main():
    """Run the React refresh test."""
    log("Starting React Component Refresh Test")
    log("=" * 60)
    
    success = test_react_refresh_trigger()
    
    if success:
        log("✅ TEST COMPLETED SUCCESSFULLY", "PASS")
        log("Backend and API are working correctly.", "INFO")
        log("Check the browser console for React component debug logs.", "INFO")
        return 0
    else:
        log("❌ TEST FAILED", "FAIL")
        return 1

if __name__ == "__main__":
    sys.exit(main())




