#!/usr/bin/env python3
"""
Acceptance Tests for Job Editing Functionality
Tests the complete workflow from editing a job to seeing changes in the project view.
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

def test_backend_health():
    """Test that the backend is running and healthy."""
    log("Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            log("✅ Backend is healthy", "PASS")
            return True
        else:
            log(f"❌ Backend returned status {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Backend connection failed: {e}", "FAIL")
        return False

def test_frontend_health():
    """Test that the frontend is running."""
    log("Testing frontend health...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            log("✅ Frontend is healthy", "PASS")
            return True
        else:
            log(f"❌ Frontend returned status {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Frontend connection failed: {e}", "FAIL")
        return False

def get_initial_job_data():
    """Get the initial state of job 1."""
    log("Getting initial job 1 data...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/1")
        if response.status_code == 200:
            job_data = response.json()
            log(f"✅ Initial job 1: {job_data.get('name')} - {job_data.get('status')}", "INFO")
            return job_data
        else:
            log(f"❌ Failed to get job 1: {response.status_code}", "FAIL")
            return None
    except Exception as e:
        log(f"❌ Error getting job 1: {e}", "FAIL")
        return None

def update_job(job_id, update_data):
    """Update a job with new data."""
    log(f"Updating job {job_id} with: {update_data}")
    try:
        response = requests.put(
            f"{BASE_URL}/api/jobs/{job_id}",
            headers={"Content-Type": "application/json"},
            json=update_data
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                log(f"✅ Job {job_id} updated successfully", "PASS")
                return result.get('job')
            else:
                log(f"❌ Job update failed: {result.get('error')}", "FAIL")
                return None
        else:
            log(f"❌ Job update returned status {response.status_code}", "FAIL")
            return None
    except Exception as e:
        log(f"❌ Error updating job: {e}", "FAIL")
        return None

def verify_job_update(job_id, expected_data):
    """Verify that a job was updated correctly."""
    log(f"Verifying job {job_id} update...")
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
        if response.status_code == 200:
            job_data = response.json()
            success = True
            for key, expected_value in expected_data.items():
                if job_data.get(key) != expected_value:
                    log(f"❌ Job {key} mismatch: expected '{expected_value}', got '{job_data.get(key)}'", "FAIL")
                    success = False
            
            if success:
                log(f"✅ Job {job_id} verification passed", "PASS")
            return success
        else:
            log(f"❌ Failed to get job {job_id}: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error verifying job: {e}", "FAIL")
        return False

def verify_project_jobs_refresh(project_id, job_id, expected_data):
    """Verify that project jobs endpoint reflects the updated job."""
    log(f"Verifying project {project_id} jobs refresh for job {job_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/projects/{project_id}/jobs")
        if response.status_code == 200:
            jobs = response.json()
            job = next((j for j in jobs if j.get('id') == str(job_id)), None)
            
            if job:
                success = True
                for key, expected_value in expected_data.items():
                    if job.get(key) != expected_value:
                        log(f"❌ Project job {key} mismatch: expected '{expected_value}', got '{job.get(key)}'", "FAIL")
                        success = False
                
                if success:
                    log(f"✅ Project jobs refresh verification passed", "PASS")
                return success
            else:
                log(f"❌ Job {job_id} not found in project {project_id} jobs", "FAIL")
                return False
        else:
            log(f"❌ Failed to get project jobs: {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"❌ Error verifying project jobs: {e}", "FAIL")
        return False

def test_complete_job_editing_workflow():
    """Test the complete job editing workflow."""
    log("=" * 60)
    log("STARTING COMPLETE JOB EDITING WORKFLOW TEST")
    log("=" * 60)
    
    # Step 1: Health checks
    if not test_backend_health():
        return False
    if not test_frontend_health():
        return False
    
    # Step 2: Get initial job state
    initial_job = get_initial_job_data()
    if not initial_job:
        return False
    
    # Step 3: Update job with new data
    update_data = {
        "name": f"Acceptance Test Job - {int(time.time())}",
        "description": "This job was updated by acceptance tests",
        "status": "in_progress"
    }
    
    updated_job = update_job(1, update_data)
    if not updated_job:
        return False
    
    # Step 4: Verify job was updated
    if not verify_job_update(1, update_data):
        return False
    
    # Step 5: Verify project jobs reflect the change
    if not verify_project_jobs_refresh(1, 1, update_data):
        return False
    
    # Step 6: Test another update to ensure consistency
    second_update = {
        "name": f"Second Test Update - {int(time.time())}",
        "status": "completed"
    }
    
    second_updated_job = update_job(1, second_update)
    if not second_updated_job:
        return False
    
    if not verify_job_update(1, second_update):
        return False
    
    if not verify_project_jobs_refresh(1, 1, second_update):
        return False
    
    log("=" * 60)
    log("✅ ALL JOB EDITING TESTS PASSED!")
    log("=" * 60)
    return True

def test_job_editing_edge_cases():
    """Test edge cases for job editing."""
    log("=" * 60)
    log("STARTING JOB EDITING EDGE CASES TEST")
    log("=" * 60)
    
    # Test 1: Update non-existent job
    log("Testing update of non-existent job...")
    response = requests.put(
        f"{BASE_URL}/api/jobs/999",
        headers={"Content-Type": "application/json"},
        json={"name": "Non-existent job"}
    )
    if response.status_code == 404:
        log("✅ Correctly handled non-existent job", "PASS")
    else:
        log(f"❌ Expected 404 for non-existent job, got {response.status_code}", "FAIL")
        return False
    
    # Test 2: Update with invalid data
    log("Testing update with invalid data...")
    response = requests.put(
        f"{BASE_URL}/api/jobs/1",
        headers={"Content-Type": "application/json"},
        json={"invalid_field": "invalid_value"}
    )
    if response.status_code == 200:
        log("✅ Correctly handled invalid field (ignored)", "PASS")
    else:
        log(f"❌ Expected 200 for invalid field, got {response.status_code}", "FAIL")
        return False
    
    # Test 3: Update with empty data
    log("Testing update with empty data...")
    response = requests.put(
        f"{BASE_URL}/api/jobs/1",
        headers={"Content-Type": "application/json"},
        json={}
    )
    if response.status_code == 200:
        log("✅ Correctly handled empty update data", "PASS")
    else:
        log(f"❌ Expected 200 for empty data, got {response.status_code}", "FAIL")
        return False
    
    log("=" * 60)
    log("✅ ALL EDGE CASE TESTS PASSED!")
    log("=" * 60)
    return True

def main():
    """Run all acceptance tests."""
    log("Starting Job Editing Acceptance Tests")
    log("=" * 60)
    
    # Run main workflow test
    workflow_success = test_complete_job_editing_workflow()
    
    # Run edge case tests
    edge_case_success = test_job_editing_edge_cases()
    
    # Final summary
    log("=" * 60)
    log("ACCEPTANCE TEST SUMMARY")
    log("=" * 60)
    
    if workflow_success and edge_case_success:
        log("✅ ALL TESTS PASSED - Job editing functionality is working correctly!", "PASS")
        return 0
    else:
        log("❌ SOME TESTS FAILED - Job editing functionality needs fixes", "FAIL")
        return 1

if __name__ == "__main__":
    sys.exit(main())




