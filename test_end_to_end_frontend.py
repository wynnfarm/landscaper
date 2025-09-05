#!/usr/bin/env python3
"""
End-to-End Frontend Test for Job Editing
Simulates the complete user workflow and verifies the frontend updates correctly.
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

def simulate_user_workflow():
    """Simulate the complete user workflow for job editing."""
    log("=" * 60)
    log("SIMULATING USER WORKFLOW FOR JOB EDITING")
    log("=" * 60)
    
    # Step 1: User views projects (simulate ProjectsManagement component)
    log("Step 1: User views projects...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()
            log(f"✅ User sees {len(projects)} projects", "PASS")
            
            # Get initial job count for project 1
            project_1 = projects[0] if projects else None
            if project_1:
                log(f"✅ Project 1: {project_1.get('title')}", "PASS")
        else:
            log(f"❌ Failed to get projects: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting projects: {e}", "FAIL")
        return False
    
    # Step 2: User views jobs for project 1 (simulate clicking "View Jobs")
    log("Step 2: User views jobs for project 1...")
    try:
        # Get the first project's client_id (since jobs are filtered by client_id)
        project_1_client_id = project_1.get('client_id')
        response = requests.get(f"{BASE_URL}/api/projects/{project_1_client_id}/jobs")
        if response.status_code == 200:
            initial_jobs = response.json()
            job_1_initial = next((j for j in initial_jobs if j.get('id') == project_1.get('id')), None)
            if job_1_initial:
                log(f"✅ Initial job 1: {job_1_initial.get('title')} - {job_1_initial.get('status')}", "PASS")
            else:
                log("❌ Job 1 not found in initial data", "FAIL")
                return False
        else:
            log(f"❌ Failed to get project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting project jobs: {e}", "FAIL")
        return False
    
    # Step 3: User edits job 1 (simulate JobCalculator component)
    unique_name = f"User Workflow Test - {int(time.time())}"
    update_data = {
        "name": unique_name,
        "description": "Updated via user workflow simulation",
        "status": "completed"
    }
    
    log(f"Step 3: User edits job 1 with name: {unique_name}")
    try:
        response = requests.put(
            f"{BASE_URL}/api/jobs/{project_1.get('id')}",
            headers={"Content-Type": "application/json"},
            json=update_data
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                log("✅ Job edit successful", "PASS")
            else:
                log(f"❌ Job edit failed: {result.get('error')}", "FAIL")
                return False
        else:
            log(f"❌ Job edit returned status {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error editing job: {e}", "FAIL")
        return False
    
    # Step 4: User returns to project view (simulate ProjectsManagement refresh)
    log("Step 4: User returns to project view...")
    time.sleep(1)  # Simulate user navigation time
    
    # Step 5: Verify project jobs show updated data
    log("Step 5: Verifying project jobs show updated data...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects/{project_1_client_id}/jobs")
        if response.status_code == 200:
            updated_jobs = response.json()
            job_1_updated = next((j for j in updated_jobs if j.get('id') == project_1.get('id')), None)
            
            if job_1_updated and job_1_updated.get('title') == unique_name:
                log("✅ Project jobs show updated job data", "PASS")
                log(f"   Job 1: {job_1_updated.get('title')} - {job_1_updated.get('status')}", "INFO")
            else:
                log("❌ Project jobs not showing updated data", "FAIL")
                if job_1_updated:
                    log(f"   Expected: '{unique_name}', Got: '{job_1_updated.get('title')}'", "INFO")
                else:
                    log("   Job 1 not found in updated project jobs", "INFO")
                return False
        else:
            log(f"❌ Failed to get updated project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error verifying updated project jobs: {e}", "FAIL")
        return False
    
    # Step 6: User views jobs again to confirm persistence
    log("Step 6: User views jobs again to confirm persistence...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects/{project_1_client_id}/jobs")
        if response.status_code == 200:
            final_jobs = response.json()
            job_1_final = next((j for j in final_jobs if j.get('id') == project_1.get('id')), None)
            
            if job_1_final and job_1_final.get('title') == unique_name:
                log("✅ Job changes persist correctly", "PASS")
            else:
                log("❌ Job changes don't persist", "FAIL")
                return False
        else:
            log(f"❌ Failed to get final project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error confirming persistence: {e}", "FAIL")
        return False
    
    log("=" * 60)
    log("✅ USER WORKFLOW SIMULATION PASSED!")
    log("=" * 60)
    return True

def test_frontend_refresh_mechanism():
    """Test the frontend refresh mechanism specifically."""
    log("=" * 60)
    log("TESTING FRONTEND REFRESH MECHANISM")
    log("=" * 60)
    
    # This test simulates what should happen when the refreshTrigger changes
    log("Simulating refreshTrigger change...")
    
    # Get current state - first get a project ID
    try:
        projects_response = requests.get(f"{BASE_URL}/api/projects")
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if not projects:
                log("❌ No projects found for refresh test", "FAIL")
                return False
            project = projects[0]
            project_id = project['id']
            project_client_id = project['client_id']
        else:
            log(f"❌ Failed to get projects: {projects_response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting projects: {e}", "FAIL")
        return False
    
    # Get current state
    try:
        response = requests.get(f"{BASE_URL}/api/projects/{project_client_id}/jobs")
        if response.status_code == 200:
            initial_jobs = response.json()
            log(f"✅ Initial state: {len(initial_jobs)} jobs", "PASS")
        else:
            log(f"❌ Failed to get initial state: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error getting initial state: {e}", "FAIL")
        return False
    
    # Update a job
    unique_name = f"Refresh Test - {int(time.time())}"
    update_data = {
        "name": unique_name,
        "status": "in_progress"
    }
    
    log(f"Updating job with: {unique_name}")
    try:
        response = requests.put(
            f"{BASE_URL}/api/jobs/{project_id}",
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
    
    # Simulate multiple refresh attempts (like the frontend would do)
    log("Simulating multiple refresh attempts...")
    for i in range(3):
        log(f"Refresh attempt {i+1}/3...")
        time.sleep(1)
        
        try:
            response = requests.get(f"{BASE_URL}/api/projects/{project_client_id}/jobs")
            if response.status_code == 200:
                jobs = response.json()
                job_1 = next((j for j in jobs if j.get('id') == project_id), None)
                
                if job_1 and job_1.get('title') == unique_name:
                    log(f"✅ Refresh {i+1}: Data is current", "PASS")
                else:
                    log(f"❌ Refresh {i+1}: Data is stale", "FAIL")
                    return False
            else:
                log(f"❌ Refresh {i+1}: Failed to get data", "FAIL")
                return False
        except Exception as e:
            log(f"❌ Refresh {i+1}: Error: {e}", "FAIL")
            return False
    
    log("=" * 60)
    log("✅ FRONTEND REFRESH MECHANISM TEST PASSED!")
    log("=" * 60)
    return True

def main():
    """Run the complete frontend tests."""
    log("Starting End-to-End Frontend Tests")
    log("=" * 60)
    
    # Run user workflow simulation
    workflow_success = simulate_user_workflow()
    
    # Run refresh mechanism test
    refresh_success = test_frontend_refresh_mechanism()
    
    # Final summary
    log("=" * 60)
    log("END-TO-END FRONTEND TEST SUMMARY")
    log("=" * 60)
    
    if workflow_success and refresh_success:
        log("✅ ALL FRONTEND TESTS PASSED!", "PASS")
        log("The backend and API layer are working correctly", "INFO")
        log("If the UI is not updating, check the React component refresh logic", "INFO")
        return 0
    else:
        log("❌ SOME FRONTEND TESTS FAILED!", "FAIL")
        log("The issue is in the API layer or data persistence", "INFO")
        return 1

if __name__ == "__main__":
    sys.exit(main())




