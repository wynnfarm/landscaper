import React, { useState, useEffect, useCallback } from "react";

const MaterialsCalculator = () => {
  const [formData, setFormData] = useState({
    project_type: "retaining_wall",
    material_type: "concrete",
    length_feet: "",
    length_inches: "",
    width_feet: "",
    width_inches: "",
    height_feet: "",
    height_inches: "",
    depth_feet: "",
    depth_inches: "",
  });

  const [calculation, setCalculation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedMaterials, setSelectedMaterials] = useState([]);
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [projectAction, setProjectAction] = useState(""); // "existing" or "new"
  const [existingProjects, setExistingProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [newProjectName, setNewProjectName] = useState("");
  const [materialTypes, setMaterialTypes] = useState([]);
  const [loadingMaterialTypes, setLoadingMaterialTypes] = useState(false);

  const fetchExistingProjects = async () => {
    try {
      const response = await fetch("/api/projects");
      if (response.ok) {
        const projects = await response.json();
        setExistingProjects(projects);
      }
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  };

  const fetchMaterialTypes = useCallback(async () => {
    try {
      setLoadingMaterialTypes(true);
      const response = await fetch("/api/materials/types");
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setMaterialTypes(data.types);
          // Set the first material type as default if none is selected
          if (data.types.length > 0 && !formData.material_type) {
            setFormData((prev) => ({
              ...prev,
              material_type: data.types[0],
            }));
          }
        }
      }
    } catch (error) {
      console.error("Error fetching material types:", error);
    } finally {
      setLoadingMaterialTypes(false);
    }
  }, [formData.material_type]);

  useEffect(() => {
    // Fetch existing projects and material types when component mounts
    fetchExistingProjects();
    fetchMaterialTypes();
  }, [fetchMaterialTypes]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Convert feet and inches to decimal feet
    const convertToDecimal = (feet, inches) => {
      const feetNum = parseFloat(feet) || 0;
      const inchesNum = parseFloat(inches) || 0;
      return feetNum + inchesNum / 12;
    };

    const dimensions = {
      project_type: formData.project_type,
      material_type: formData.material_type,
    };

    // Add dimensions based on project type
    if (formData.project_type === "retaining_wall") {
      dimensions.length = convertToDecimal(formData.length_feet, formData.length_inches);
      dimensions.height = convertToDecimal(formData.height_feet, formData.height_inches);
      dimensions.depth = convertToDecimal(formData.depth_feet, formData.depth_inches);
    } else if (formData.project_type === "patio") {
      dimensions.length = convertToDecimal(formData.length_feet, formData.length_inches);
      dimensions.width = convertToDecimal(formData.width_feet, formData.width_inches);
    } else if (formData.project_type === "garden_wall") {
      dimensions.length = convertToDecimal(formData.length_feet, formData.length_inches);
      dimensions.height = convertToDecimal(formData.height_feet, formData.height_inches);
    }

    try {
      const response = await fetch("/api/materials/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dimensions),
      });

      const data = await response.json();

      if (data.success) {
        setCalculation(data);
        // Initialize selected materials with all materials selected
        const materials = Object.entries(data.materials).map(([key, material]) => ({
          key,
          ...material,
          selected: true,
        }));
        setSelectedMaterials(materials);
      } else {
        setError(data.error || "Failed to calculate materials");
      }
    } catch (error) {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };

  const handleMaterialSelection = (materialKey, selected) => {
    setSelectedMaterials((prev) =>
      prev.map((material) => (material.key === materialKey ? { ...material, selected } : material)),
    );
  };

  const handleAddToProject = (action) => {
    setProjectAction(action);
    setShowProjectModal(true);
  };

  const handleProjectSubmit = async () => {
    if (projectAction === "existing" && !selectedProjectId) {
      setError("Please select a project");
      return;
    }
    if (projectAction === "new" && !newProjectName.trim()) {
      setError("Please enter a project name");
      return;
    }

    const selectedMaterialsData = selectedMaterials
      .filter((material) => material.selected)
      .map((material) => ({
        name: material.key.replace("_", " ").toUpperCase(),
        quantity: material.quantity,
        unit: material.unit,
        cost_per_unit: material.cost_per_unit,
        total_cost: material.total_cost,
      }));

    try {
      if (projectAction === "existing") {
        // Add materials to existing project
        const response = await fetch(`/api/projects/${selectedProjectId}/materials`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            materials: selectedMaterialsData,
            calculation_data: calculation,
          }),
        });

        if (response.ok) {
          alert("Materials added to project successfully!");
          setShowProjectModal(false);
          setSelectedMaterials([]);
          setCalculation(null);
        } else {
          setError("Failed to add materials to project");
        }
      } else {
        // Create new project with materials
        const response = await fetch("/api/projects", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: newProjectName,
            job_type: "garden_design",
            status: "planning",
            materials: selectedMaterialsData,
            calculation_data: calculation,
            estimated_cost: selectedMaterialsData.reduce((sum, mat) => sum + mat.total_cost, 0),
          }),
        });

        if (response.ok) {
          alert("New project created successfully!");
          setShowProjectModal(false);
          setSelectedMaterials([]);
          setCalculation(null);
          setNewProjectName("");
          fetchExistingProjects(); // Refresh project list
        } else {
          setError("Failed to create new project");
        }
      }
    } catch (error) {
      setError("Failed to save project");
    }
  };

  const renderProjectTypeFields = () => {
    switch (formData.project_type) {
      case "retaining_wall":
        return (
          <>
            <div className="dimension-group">
              <div className="form-group">
                <label className="form-label">Length</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="length_feet"
                    value={formData.length_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="length_inches"
                    value={formData.length_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Height</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="height_feet"
                    value={formData.height_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="height_inches"
                    value={formData.height_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Depth</label>
              <div className="dimension-inputs">
                <input
                  type="number"
                  name="depth_feet"
                  value={formData.depth_feet}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Feet"
                  required
                  min="0"
                  step="1"
                />
                <input
                  type="number"
                  name="depth_inches"
                  value={formData.depth_inches}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Inches"
                  min="0"
                  max="11"
                  step="1"
                />
              </div>
            </div>
          </>
        );
      case "patio":
        return (
          <>
            <div className="dimension-group">
              <div className="form-group">
                <label className="form-label">Length</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="length_feet"
                    value={formData.length_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="length_inches"
                    value={formData.length_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Width</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="width_feet"
                    value={formData.width_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="width_inches"
                    value={formData.width_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
            </div>
          </>
        );
      case "garden_wall":
        return (
          <>
            <div className="dimension-group">
              <div className="form-group">
                <label className="form-label">Length</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="length_feet"
                    value={formData.length_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="length_inches"
                    value={formData.length_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Height</label>
                <div className="dimension-inputs">
                  <input
                    type="number"
                    name="height_feet"
                    value={formData.height_feet}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Feet"
                    required
                    min="0"
                    step="1"
                  />
                  <input
                    type="number"
                    name="height_inches"
                    value={formData.height_inches}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Inches"
                    min="0"
                    max="11"
                    step="1"
                  />
                </div>
              </div>
            </div>
          </>
        );
      default:
        return null;
    }
  };

  const renderCalculationResults = () => {
    if (!calculation) return null;

    const projectArea = calculation.wall_area || calculation.patio_area || 0;

    return (
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">📊 Calculation Results</h3>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <strong>Project Type:</strong> {calculation.project_type.replace("_", " ").toUpperCase()}
          <br />
          <strong>Area:</strong> {projectArea.toFixed(1)} sq ft
          <br />
          <strong>Labor Hours:</strong> {calculation.labor_hours} hours
        </div>

        {/* Desktop Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Material</th>
                <th>Quantity</th>
                <th>Unit</th>
                <th>Cost/Unit</th>
                <th>Total Cost</th>
                <th>Select</th>
              </tr>
            </thead>
            <tbody>
              {selectedMaterials.map((material) => (
                <tr key={material.key}>
                  <td>{material.key.replace("_", " ").toUpperCase()}</td>
                  <td>{material.quantity}</td>
                  <td>{material.unit}</td>
                  <td>${material.cost_per_unit.toFixed(2)}</td>
                  <td>${material.total_cost.toFixed(2)}</td>
                  <td>
                    <input
                      type="checkbox"
                      checked={material.selected}
                      onChange={(e) => handleMaterialSelection(material.key, e.target.checked)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Card Layout */}
        <div className="mobile-cards">
          {selectedMaterials.map((material) => (
            <div key={material.key} className="mobile-card">
              <div className="mobile-card-header">{material.key.replace("_", " ").toUpperCase()}</div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Quantity:</span>
                <span className="mobile-card-value">
                  {material.quantity} {material.unit}
                </span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Cost/Unit:</span>
                <span className="mobile-card-value">${material.cost_per_unit.toFixed(2)}</span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Total Cost:</span>
                <span className="mobile-card-value">${material.total_cost.toFixed(2)}</span>
              </div>
              <div className="mobile-card-row">
                <span className="mobile-card-label">Select:</span>
                <span className="mobile-card-value">
                  <input
                    type="checkbox"
                    checked={material.selected}
                    onChange={(e) => handleMaterialSelection(material.key, e.target.checked)}
                  />
                </span>
              </div>
            </div>
          ))}
        </div>

        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            backgroundColor: "#f0f9ff",
            borderRadius: "8px",
            border: "1px solid #0ea5e9",
          }}
        >
          <h4 style={{ margin: "0 0 0.5rem 0", color: "#0c4a6e" }}>
            💰 Total Project Cost: ${calculation.total_cost.toFixed(2)}
          </h4>
          <p style={{ margin: "0", color: "#0c4a6e" }}>
            Selected Materials Cost: $
            {selectedMaterials
              .filter((m) => m.selected)
              .reduce((sum, m) => sum + m.total_cost, 0)
              .toFixed(2)}
          </p>
        </div>

        {/* Project Integration Buttons */}
        <div style={{ marginTop: "1rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <button
            className="btn btn-primary"
            onClick={() => handleAddToProject("existing")}
            disabled={selectedMaterials.filter((m) => m.selected).length === 0}
          >
            📋 Add to Existing Project
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => handleAddToProject("new")}
            disabled={selectedMaterials.filter((m) => m.selected).length === 0}
          >
            🆕 Create New Project
          </button>
        </div>
      </div>
    );
  };

  const renderProjectModal = () => {
    if (!showProjectModal) return null;

    return (
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
          <h3 style={{ margin: "0 0 1rem 0" }}>
            {projectAction === "existing" ? "Add to Existing Project" : "Create New Project"}
          </h3>

          {projectAction === "existing" ? (
            <div className="form-group">
              <label className="form-label">Select Project</label>
              <select
                value={selectedProjectId}
                onChange={(e) => setSelectedProjectId(e.target.value)}
                className="form-select"
              >
                <option value="">Choose a project...</option>
                {existingProjects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name} - {project.status}
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">Project Name</label>
              <input
                type="text"
                value={newProjectName}
                onChange={(e) => setNewProjectName(e.target.value)}
                className="form-input"
                placeholder="Enter project name"
              />
            </div>
          )}

          <div style={{ marginTop: "1rem" }}>
            <strong>Selected Materials:</strong>
            <ul style={{ margin: "0.5rem 0", paddingLeft: "1.5rem" }}>
              {selectedMaterials
                .filter((m) => m.selected)
                .map((material) => (
                  <li key={material.key}>
                    {material.key.replace("_", " ").toUpperCase()} - {material.quantity} {material.unit} ($
                    {material.total_cost.toFixed(2)})
                  </li>
                ))}
            </ul>
          </div>

          <div style={{ marginTop: "1.5rem", display: "flex", gap: "0.5rem" }}>
            <button className="btn btn-primary" onClick={handleProjectSubmit}>
              {projectAction === "existing" ? "Add to Project" : "Create Project"}
            </button>
            <button className="btn btn-secondary" onClick={() => setShowProjectModal(false)}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🧮 Materials Calculator</h2>
        </div>

        <form onSubmit={handleSubmit} className="calculator-form">
          <div className="form-group">
            <label className="form-label">Project Type</label>
            <select
              name="project_type"
              value={formData.project_type}
              onChange={handleInputChange}
              className="form-select"
            >
              <option value="retaining_wall">Retaining Wall</option>
              <option value="patio">Patio</option>
              <option value="garden_wall">Garden Wall</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Material Type</label>
            <select
              name="material_type"
              value={formData.material_type}
              onChange={handleInputChange}
              className="form-select"
              disabled={loadingMaterialTypes}
            >
              {loadingMaterialTypes ? (
                <option value="">Loading material types...</option>
              ) : materialTypes.length > 0 ? (
                materialTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))
              ) : (
                <option value="">No material types available</option>
              )}
            </select>
          </div>

          {renderProjectTypeFields()}

          {error && (
            <div
              style={{
                padding: "0.75rem",
                backgroundColor: "#fef2f2",
                border: "1px solid #fecaca",
                borderRadius: "8px",
                color: "#991b1b",
                marginBottom: "1rem",
              }}
            >
              ❌ {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: "100%" }}>
            {loading ? "🔄 Calculating..." : "🧮 Calculate Materials"}
          </button>
        </form>
      </div>

      {renderCalculationResults()}
      {renderProjectModal()}
    </div>
  );
};

export default MaterialsCalculator;
