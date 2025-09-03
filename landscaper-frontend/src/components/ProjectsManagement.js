import React, { useState, useEffect } from "react";

const ProjectsManagement = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showMaterialsModal, setShowMaterialsModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [editFormData, setEditFormData] = useState({
    name: "",
    status: "planning",
    budget: 0,
  });
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [confirmAction, setConfirmAction] = useState(null);
  const [projectJobs, setProjectJobs] = useState({});
  const [showJobsModal, setShowJobsModal] = useState(false);
  const [selectedProjectJobs, setSelectedProjectJobs] = useState([]);
  const [showEditJobModal, setShowEditJobModal] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [editJobFormData, setEditJobFormData] = useState({
    name: "",
    description: "",
    status: "planned",
  });

  // Fetch projects from API
  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/projects");
      if (response.ok) {
        const data = await response.json();
        setProjects(data);
      } else {
        console.error("Failed to fetch projects");
      }
    } catch (error) {
      console.error("Error fetching projects:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // Handle project status update
  const handleStatusUpdate = async (projectId, newStatus) => {
    try {
      const response = await fetch("/api/project/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          project_id: projectId,
          status: newStatus,
        }),
      });

      if (response.ok) {
        await fetchProjects(); // Refresh the list
      } else {
        console.error("Failed to update project status");
      }
    } catch (error) {
      console.error("Error updating project status:", error);
    }
  };

  const handleViewMaterials = (project) => {
    setSelectedProject(project);
    setShowMaterialsModal(true);
  };

  const handleEditProject = (project) => {
    setEditingProject(project);
    setEditFormData({
      name: project.name,
      status: project.status,
      budget: project.budget || 0,
    });
    setShowEditModal(true);
  };

  const handleEditFormChange = (e) => {
    const { name, value } = e.target;
    setEditFormData((prev) => ({
      ...prev,
      [name]: name === "budget" ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSaveProject = async () => {
    try {
      const response = await fetch(`/api/projects/${editingProject.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editFormData),
      });

      if (response.ok) {
        await fetchProjects(); // Refresh the list
        setShowEditModal(false);
        setEditingProject(null);
        alert("Project updated successfully!");
      } else {
        console.error("Failed to update project");
      }
    } catch (error) {
      console.error("Error updating project:", error);
    }
  };

  const handleAddMaterialToProject = async (projectId) => {
    // This will open the materials calculator with the project pre-selected
    // For now, we'll show a simple form to add materials manually
    const materialName = prompt("Enter material name:");
    const quantity = parseFloat(prompt("Enter quantity:"));
    const unit = prompt("Enter unit (e.g., blocks, sq ft, tons):");
    const costPerUnit = parseFloat(prompt("Enter cost per unit:"));

    if (materialName && quantity && unit && costPerUnit) {
      try {
        const response = await fetch(`/api/projects/${projectId}/materials`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            materials: [
              {
                name: materialName,
                quantity: quantity,
                unit: unit,
                cost_per_unit: costPerUnit,
                total_cost: quantity * costPerUnit,
              },
            ],
          }),
        });

        if (response.ok) {
          await fetchProjects(); // Refresh the list
          alert("Material added successfully!");
        } else {
          console.error("Failed to add material");
        }
      } catch (error) {
        console.error("Error adding material:", error);
      }
    }
  };

  const handleRemoveMaterial = async (projectId, materialIndex) => {
    setConfirmAction({
      type: "remove_material",
      projectId,
      materialIndex,
      message: "Are you sure you want to remove this material?",
    });
    setShowConfirmModal(true);
  };

  const handleConfirmAction = async () => {
    if (!confirmAction) return;

    try {
      if (confirmAction.type === "remove_material") {
        const response = await fetch(
          `/api/projects/${confirmAction.projectId}/materials/${confirmAction.materialIndex}`,
          {
            method: "DELETE",
          },
        );

        if (response.ok) {
          await fetchProjects(); // Refresh the list
          alert("Material removed successfully!");
        } else {
          console.error("Failed to remove material");
        }
      } else if (confirmAction.type === "delete_job") {
        const response = await fetch(`/api/jobs/${confirmAction.job.id}`, {
          method: "DELETE",
        });

        if (response.ok) {
          await fetchProjectJobs(confirmAction.job.project_id);
          alert("Job deleted successfully!");
        } else {
          console.error("Failed to delete job");
        }
      }
    } catch (error) {
      console.error("Error performing action:", error);
    } finally {
      setShowConfirmModal(false);
      setConfirmAction(null);
    }
  };

  const getTotalMaterialsCost = (materials) => {
    if (!materials || !Array.isArray(materials)) return 0;
    return materials.reduce((sum, material) => sum + (material.total_cost || 0), 0);
  };

  // Job Management Functions
  const fetchProjectJobs = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/jobs`);
      if (response.ok) {
        const jobs = await response.json();
        setProjectJobs((prev) => ({ ...prev, [projectId]: jobs }));
        return jobs;
      } else {
        console.error("Failed to fetch project jobs");
        return [];
      }
    } catch (error) {
      console.error("Error fetching project jobs:", error);
      return [];
    }
  };

  const handleViewJobs = async (project) => {
    setSelectedProject(project);
    const jobs = await fetchProjectJobs(project.id);
    setSelectedProjectJobs(jobs);
    setShowJobsModal(true);
  };

  const handleEditJob = (job) => {
    setEditingJob(job);
    setEditJobFormData({
      name: job.name,
      description: job.description,
      status: job.status,
    });
    setShowEditJobModal(true);
  };

  const handleEditJobFormChange = (e) => {
    const { name, value } = e.target;
    setEditJobFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSaveJob = async () => {
    try {
      const response = await fetch(`/api/jobs/${editingJob.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editJobFormData),
      });

      if (response.ok) {
        await fetchProjectJobs(editingJob.project_id);
        setShowEditJobModal(false);
        setEditingJob(null);
        alert("Job updated successfully!");
      } else {
        console.error("Failed to update job");
      }
    } catch (error) {
      console.error("Error updating job:", error);
    }
  };

  const handleRecalculateJob = async (job) => {
    try {
      const response = await fetch(`/api/jobs/${job.id}/recalculate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          await fetchProjectJobs(job.project_id);
          alert("Job recalculated successfully!");
        } else {
          alert("Failed to recalculate job: " + data.error);
        }
      } else {
        console.error("Failed to recalculate job");
      }
    } catch (error) {
      console.error("Error recalculating job:", error);
    }
  };

  const handleDeleteJob = async (job) => {
    setConfirmAction({
      type: "delete_job",
      job,
      message: "Are you sure you want to delete this job?",
    });
    setShowConfirmModal(true);
  };

  const getJobStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "#28a745";
      case "in_progress":
        return "#ffc107";
      case "planned":
        return "#17a2b8";
      default:
        return "#6c757d";
    }
  };

  const getMaterialsCount = (materials) => {
    if (!materials || !Array.isArray(materials)) return 0;
    return materials.length;
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="projects-management">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🏗️ Projects Management</h2>
          <button className="btn btn-primary" onClick={fetchProjects}>
            🔄 Refresh
          </button>
        </div>

        {/* Projects Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Project Name</th>
                <th>Client</th>
                <th>Status</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Budget</th>
                <th>Materials</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td>{project.name}</td>
                  <td>{project.client_name}</td>
                  <td>
                    <span
                      className={`status-badge ${
                        project.status === "completed"
                          ? "status-completed"
                          : project.status === "in_progress"
                          ? "status-pending"
                          : project.status === "planning"
                          ? "status-warning"
                          : "status-inactive"
                      }`}
                    >
                      {project.status}
                    </span>
                  </td>
                  <td>{project.start_date ? new Date(project.start_date).toLocaleDateString() : "N/A"}</td>
                  <td>{project.end_date ? new Date(project.end_date).toLocaleDateString() : "N/A"}</td>
                  <td>${project.budget || "N/A"}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleViewMaterials(project)}
                      disabled={!project.materials || project.materials.length === 0}
                    >
                      📦 {getMaterialsCount(project.materials)} items
                    </button>
                  </td>
                  <td>
                    <div style={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                      <button className="btn btn-sm btn-info" onClick={() => handleViewJobs(project)}>
                        🏗️ Jobs ({projectJobs[project.id]?.length || 0})
                      </button>
                      <select
                        value={project.status}
                        onChange={(e) => handleStatusUpdate(project.id, e.target.value)}
                        className="form-select"
                        style={{ minWidth: "120px" }}
                      >
                        <option value="planning">Planning</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                        <option value="on_hold">On Hold</option>
                      </select>
                      <button className="btn btn-sm btn-primary" onClick={() => handleEditProject(project)}>
                        ✏️ Edit
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Card Layout */}
        <div className="mobile-cards">
          {projects.map((project) => (
            <div key={project.id} className="mobile-card">
              <div className="mobile-card-header">{project.name}</div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Client:</span>
                <span className="mobile-card-value">{project.client_name}</span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Status:</span>
                <span className="mobile-card-value">
                  <span
                    className={`status-badge ${
                      project.status === "completed"
                        ? "status-completed"
                        : project.status === "in_progress"
                        ? "status-pending"
                        : project.status === "planning"
                        ? "status-warning"
                        : "status-inactive"
                    }`}
                  >
                    {project.status}
                  </span>
                </span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Budget:</span>
                <span className="mobile-card-value">${project.budget || "N/A"}</span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Materials:</span>
                <span className="mobile-card-value">
                  <button
                    className="btn btn-sm btn-secondary"
                    onClick={() => handleViewMaterials(project)}
                    disabled={!project.materials || project.materials.length === 0}
                  >
                    📦 {getMaterialsCount(project.materials)} items
                  </button>
                </span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Actions:</span>
                <span className="mobile-card-value">
                  <div style={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                    <button className="btn btn-sm btn-info" onClick={() => handleViewJobs(project)}>
                      🏗️ Jobs ({projectJobs[project.id]?.length || 0})
                    </button>
                    <select
                      value={project.status}
                      onChange={(e) => handleStatusUpdate(project.id, e.target.value)}
                      className="form-select"
                    >
                      <option value="planning">Planning</option>
                      <option value="in_progress">In Progress</option>
                      <option value="completed">Completed</option>
                      <option value="on_hold">On Hold</option>
                    </select>
                    <button className="btn btn-sm btn-primary" onClick={() => handleEditProject(project)}>
                      ✏️ Edit
                    </button>
                  </div>
                </span>
              </div>
            </div>
          ))}
        </div>

        {projects.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem", color: "#6b7280" }}>No projects found.</div>
        )}
      </div>

      {/* Materials Modal */}
      {showMaterialsModal && selectedProject && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "2rem",
              borderRadius: "8px",
              maxWidth: "600px",
              width: "90%",
              maxHeight: "80vh",
              overflow: "auto",
            }}
          >
            <h3 style={{ margin: "0 0 1rem 0" }}>📦 Materials for {selectedProject.name}</h3>

            {selectedProject.materials && selectedProject.materials.length > 0 ? (
              <div>
                <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem" }}>
                  <button
                    className="btn btn-sm btn-primary"
                    onClick={() => handleAddMaterialToProject(selectedProject.id)}
                  >
                    ➕ Add Material
                  </button>
                </div>

                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Material</th>
                        <th>Quantity</th>
                        <th>Unit</th>
                        <th>Cost/Unit</th>
                        <th>Total Cost</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedProject.materials.map((material, index) => (
                        <tr key={index}>
                          <td>{material.name}</td>
                          <td>{material.quantity}</td>
                          <td>{material.unit}</td>
                          <td>${material.cost_per_unit?.toFixed(2) || "N/A"}</td>
                          <td>${material.total_cost?.toFixed(2) || "N/A"}</td>
                          <td>
                            <button
                              className="btn btn-sm btn-danger"
                              onClick={() => handleRemoveMaterial(selectedProject.id, index)}
                            >
                              🗑️ Remove
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "#f0fdf4", borderRadius: "8px" }}>
                  <strong>Total Materials Cost: ${getTotalMaterialsCost(selectedProject.materials).toFixed(2)}</strong>
                </div>
              </div>
            ) : (
              <div>
                <p style={{ color: "#6b7280", marginBottom: "1rem" }}>
                  No materials have been added to this project yet.
                </p>
                <button className="btn btn-primary" onClick={() => handleAddMaterialToProject(selectedProject.id)}>
                  ➕ Add First Material
                </button>
              </div>
            )}

            <div style={{ marginTop: "1.5rem", textAlign: "center" }}>
              <button className="btn btn-secondary" onClick={() => setShowMaterialsModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Project Modal */}
      {showEditModal && editingProject && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "2rem",
              borderRadius: "8px",
              maxWidth: "500px",
              width: "90%",
              maxHeight: "80vh",
              overflow: "auto",
            }}
          >
            <h3 style={{ margin: "0 0 1rem 0" }}>✏️ Edit Project: {editingProject.name}</h3>

            <div style={{ display: "grid", gap: "1rem" }}>
              <div className="form-group">
                <label className="form-label">Project Name</label>
                <input
                  type="text"
                  name="name"
                  value={editFormData.name}
                  onChange={handleEditFormChange}
                  className="form-input"
                  placeholder="Enter project name"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  value={editFormData.status}
                  onChange={handleEditFormChange}
                  className="form-select"
                >
                  <option value="planning">Planning</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="on_hold">On Hold</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Budget</label>
                <input
                  type="number"
                  name="budget"
                  value={editFormData.budget}
                  onChange={handleEditFormChange}
                  className="form-input"
                  placeholder="Enter budget"
                  min="0"
                  step="0.01"
                />
              </div>

              <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "#f0f9ff", borderRadius: "8px" }}>
                <strong>Current Materials Cost: ${getTotalMaterialsCost(editingProject.materials).toFixed(2)}</strong>
                <br />
                <small style={{ color: "#6b7280" }}>
                  Total project cost will be: $
                  {(editFormData.budget + getTotalMaterialsCost(editingProject.materials)).toFixed(2)}
                </small>
              </div>
            </div>

            <div style={{ marginTop: "1.5rem", display: "flex", gap: "0.5rem" }}>
              <button className="btn btn-primary" onClick={handleSaveProject}>
                💾 Save Changes
              </button>
              <button className="btn btn-secondary" onClick={() => setShowEditModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Jobs Modal */}
      {showJobsModal && selectedProject && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "2rem",
              borderRadius: "8px",
              maxWidth: "800px",
              width: "90%",
              maxHeight: "80vh",
              overflow: "auto",
            }}
          >
            <h3 style={{ margin: "0 0 1rem 0" }}>🏗️ Jobs for {selectedProject.name}</h3>

            {selectedProjectJobs.length > 0 ? (
              <div>
                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Job Name</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Area</th>
                        <th>Materials</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedProjectJobs.map((job) => (
                        <tr key={job.id}>
                          <td>{job.name}</td>
                          <td>{job.job_type}</td>
                          <td>
                            <span className="status-badge" style={{ backgroundColor: getJobStatusColor(job.status) }}>
                              {job.status}
                            </span>
                          </td>
                          <td>
                            {job.calculation_result?.area_sqft ? `${job.calculation_result.area_sqft} sq ft` : "N/A"}
                          </td>
                          <td>
                            {job.calculation_result?.materials
                              ? Object.keys(job.calculation_result.materials).length + " types"
                              : "N/A"}
                          </td>
                          <td>
                            <div style={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                              <button
                                className="btn btn-sm btn-warning"
                                onClick={() => handleRecalculateJob(job)}
                                title="Recalculate job with current measurements"
                              >
                                🔄 Recalc
                              </button>
                              <button className="btn btn-sm btn-primary" onClick={() => handleEditJob(job)}>
                                ✏️ Edit
                              </button>
                              <button className="btn btn-sm btn-danger" onClick={() => handleDeleteJob(job)}>
                                🗑️ Delete
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Mobile Jobs Cards */}
                <div className="mobile-cards">
                  {selectedProjectJobs.map((job) => (
                    <div key={job.id} className="mobile-card">
                      <div className="mobile-card-header">{job.name}</div>
                      <div className="mobile-card-row">
                        <span className="mobile-card-label">Type:</span>
                        <span className="mobile-card-value">{job.job_type}</span>
                      </div>
                      <div className="mobile-card-row">
                        <span className="mobile-card-label">Status:</span>
                        <span className="mobile-card-value">
                          <span className="status-badge" style={{ backgroundColor: getJobStatusColor(job.status) }}>
                            {job.status}
                          </span>
                        </span>
                      </div>
                      <div className="mobile-card-row">
                        <span className="mobile-card-label">Area:</span>
                        <span className="mobile-card-value">
                          {job.calculation_result?.area_sqft ? `${job.calculation_result.area_sqft} sq ft` : "N/A"}
                        </span>
                      </div>
                      <div className="mobile-card-row">
                        <span className="mobile-card-label">Materials:</span>
                        <span className="mobile-card-value">
                          {job.calculation_result?.materials
                            ? Object.keys(job.calculation_result.materials).length + " types"
                            : "N/A"}
                        </span>
                      </div>
                      <div className="mobile-card-row">
                        <span className="mobile-card-label">Actions:</span>
                        <span className="mobile-card-value">
                          <div style={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                            <button className="btn btn-sm btn-warning" onClick={() => handleRecalculateJob(job)}>
                              🔄 Recalc
                            </button>
                            <button className="btn btn-sm btn-primary" onClick={() => handleEditJob(job)}>
                              ✏️ Edit
                            </button>
                            <button className="btn btn-sm btn-danger" onClick={() => handleDeleteJob(job)}>
                              🗑️ Delete
                            </button>
                          </div>
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div style={{ textAlign: "center", padding: "2rem", color: "#6b7280" }}>
                No jobs found for this project. Create jobs using the Job Calculator!
              </div>
            )}

            <div style={{ marginTop: "1.5rem", display: "flex", gap: "0.5rem" }}>
              <button className="btn btn-secondary" onClick={() => setShowJobsModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Job Modal */}
      {showEditJobModal && editingJob && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "2rem",
              borderRadius: "8px",
              maxWidth: "500px",
              width: "90%",
            }}
          >
            <h3 style={{ margin: "0 0 1rem 0" }}>✏️ Edit Job: {editingJob.name}</h3>

            <div>
              <div className="form-group">
                <label className="form-label">Job Name</label>
                <input
                  type="text"
                  name="name"
                  value={editJobFormData.name}
                  onChange={handleEditJobFormChange}
                  className="form-input"
                  placeholder="Enter job name"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  name="description"
                  value={editJobFormData.description}
                  onChange={handleEditJobFormChange}
                  className="form-input"
                  placeholder="Enter job description"
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  name="status"
                  value={editJobFormData.status}
                  onChange={handleEditJobFormChange}
                  className="form-select"
                >
                  <option value="planned">Planned</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="on_hold">On Hold</option>
                </select>
              </div>

              <div style={{ marginTop: "1rem", padding: "1rem", backgroundColor: "#f0f9ff", borderRadius: "8px" }}>
                <strong>Job Details:</strong>
                <br />
                <small style={{ color: "#6b7280" }}>
                  Type: {editingJob.job_type} | Area: {editingJob.calculation_result?.area_sqft || "N/A"} sq ft
                </small>
              </div>
            </div>

            <div style={{ marginTop: "1.5rem", display: "flex", gap: "0.5rem" }}>
              <button className="btn btn-primary" onClick={handleSaveJob}>
                💾 Save Changes
              </button>
              <button className="btn btn-secondary" onClick={() => setShowEditJobModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal */}
      {showConfirmModal && confirmAction && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "2rem",
              borderRadius: "8px",
              maxWidth: "400px",
              width: "90%",
              textAlign: "center",
            }}
          >
            <h3 style={{ margin: "0 0 1rem 0" }}>⚠️ Confirm Action</h3>
            <p style={{ margin: "0 0 1.5rem 0", color: "#6b7280" }}>{confirmAction.message}</p>
            <div style={{ display: "flex", gap: "0.5rem", justifyContent: "center" }}>
              <button className="btn btn-danger" onClick={handleConfirmAction}>
                ✅ Yes, Continue
              </button>
              <button className="btn btn-secondary" onClick={() => setShowConfirmModal(false)}>
                ❌ Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectsManagement;
