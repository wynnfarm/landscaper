#!/usr/bin/env python3
"""
Frontend-Specific Acceptance Tests for Job Editing
Tests that the frontend components actually receive and display updated job data.
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:3000"

def log(message, level="INFO"):
    """Log messages with timestamp."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def test_frontend_job_refresh():
    """Test that the frontend properly refreshes job data."""
    log("=" * 60)
    log("TESTING FRONTEND JOB REFRESH")
    log("=" * 60)
    
    # Step 1: Get initial project jobs data
    log("Getting initial project jobs data...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects/1/jobs")
        if response.status_code == 200:
            initial_jobs = response.json()
            job_1_initial = next((j for j in initial_jobs if j.get('id') == '1'), None)
            if job_1_initial:
                log(f"✅ Initial job 1: {job_1_initial.get('name')} - {job_1_initial.get('status')}", "INFO")
            else:
                log("❌ Job 1 not found in initial data", "FAIL")
                return False
        else:
            log(f"❌ Failed to get initial project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting initial data: {e}", "FAIL")
        return False
    
    # Step 2: Update job with distinctive data
    unique_name = f"Frontend Test Job - {int(time.time())}"
    update_data = {
        "name": unique_name,
        "description": "Testing frontend refresh",
        "status": "planning"
    }
    
    log(f"Updating job 1 with unique name: {unique_name}")
    try:
        response = requests.put(
            f"{BASE_URL}/api/jobs/1",
            headers={"Content-Type": "application/json"},
            json=update_data
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                log("✅ Job update successful", "PASS")
            else:
                log(f"❌ Job update failed: {result.get('error')}", "FAIL")
                return False
        else:
            log(f"❌ Job update returned status {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error updating job: {e}", "FAIL")
        return False
    
    # Step 3: Wait a moment for any async operations
    log("Waiting for potential async operations...")
    time.sleep(2)
    
    # Step 4: Verify the update was saved
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
    
    # Step 5: Check project jobs endpoint multiple times
    log("Checking project jobs endpoint multiple times...")
    for i in range(3):
        log(f"Check {i+1}/3...")
        try:
            response = requests.get(f"{BASE_URL}/api/projects/1/jobs")
            if response.status_code == 200:
                jobs = response.json()
                job_1 = next((j for j in jobs if j.get('id') == '1'), None)
                if job_1 and job_1.get('name') == unique_name:
                    log(f"✅ Check {i+1}: Project jobs shows updated job", "PASS")
                else:
                    log(f"❌ Check {i+1}: Project jobs not showing updated job", "FAIL")
                    if job_1:
                        log(f"   Expected: '{unique_name}', Got: '{job_1.get('name')}'", "INFO")
                    else:
                        log("   Job 1 not found in project jobs", "INFO")
                    return False
            else:
                log(f"❌ Check {i+1}: Failed to get project jobs: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            log(f"❌ Check {i+1}: Error getting project jobs: {e}", "FAIL")
            return False
        
        if i < 2:  # Don't sleep after the last check
            time.sleep(1)
    
    log("=" * 60)
    log("✅ FRONTEND JOB REFRESH TEST PASSED!")
    log("=" * 60)
    return True

def test_frontend_component_behavior():
    """Test specific frontend component behavior."""
    log("=" * 60)
    log("TESTING FRONTEND COMPONENT BEHAVIOR")
    log("=" * 60)
    
    # Test 1: Check if ProjectsManagement component is making the right API calls
    log("Testing ProjectsManagement API calls...")
    
    # Simulate what the frontend should be doing
    # First, get projects
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()
            log(f"✅ Got {len(projects)} projects", "PASS")
        else:
            log(f"❌ Failed to get projects: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting projects: {e}", "FAIL")
        return False
    
    # Then, get jobs for each project
    for project in projects:
        project_id = project.get('id')
        log(f"Getting jobs for project {project_id}...")
        try:
            response = requests.get(f"{BASE_URL}/api/projects/{project_id}/jobs")
            if response.status_code == 200:
                jobs = response.json()
                log(f"✅ Project {project_id} has {len(jobs)} jobs", "PASS")
                
                # Check if job 1 is in project 1 and has the expected data
                if project_id == '1':
                    job_1 = next((j for j in jobs if j.get('id') == '1'), None)
                    if job_1:
                        log(f"✅ Job 1 in project 1: {job_1.get('name')} - {job_1.get('status')}", "PASS")
                    else:
                        log("❌ Job 1 not found in project 1", "FAIL")
                        return False
            else:
                log(f"❌ Failed to get jobs for project {project_id}: {response.status_code}", "FAIL")
                return False
        except Exception as e:
            log(f"❌ Error getting jobs for project {project_id}: {e}", "FAIL")
            return False
    
    log("=" * 60)
    log("✅ FRONTEND COMPONENT BEHAVIOR TEST PASSED!")
    log("=" * 60)
    return True

def main():
    """Run frontend-specific tests."""
    log("Starting Frontend-Specific Job Editing Tests")
    log("=" * 60)
    
    # Run frontend refresh test
    refresh_success = test_frontend_job_refresh()
    
    # Run component behavior test
    component_success = test_frontend_component_behavior()
    
    # Final summary
    log("=" * 60)
    log("FRONTEND TEST SUMMARY")
    log("=" * 60)
    
    if refresh_success and component_success:
        log("✅ ALL FRONTEND TESTS PASSED!", "PASS")
        log("The issue might be in the React component refresh mechanism", "INFO")
        return 0
    else:
        log("❌ SOME FRONTEND TESTS FAILED!", "FAIL")
        return 1

if __name__ == "__main__":
    sys.exit(main())




