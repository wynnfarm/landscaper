import React, { useState, useEffect } from "react";
import "./JobCalculator.css";

const JobCalculator = () => {
  const [jobTypes, setJobTypes] = useState([]);
  const [templates, setTemplates] = useState({});
  const [selectedJobType, setSelectedJobType] = useState("");
  const [measurements, setMeasurements] = useState({});
  const [calculationResult, setCalculationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState("");
  const [jobName, setJobName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [savingJob, setSavingJob] = useState(false);

  useEffect(() => {
    fetchJobTypes();
    fetchTemplates();
    fetchProjects();
  }, []);

  const fetchJobTypes = async () => {
    try {
      const response = await fetch("/api/job-calculator/types");
      const data = await response.json();
      if (data.success) {
        setJobTypes(data.job_types);
      }
    } catch (err) {
      setError("Failed to load job types");
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await fetch("/api/job-calculator/templates");
      const data = await response.json();
      if (data.success) {
        setTemplates(data.templates);
      }
    } catch (err) {
      setError("Failed to load templates");
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await fetch("/api/projects");
      const data = await response.json();
      setProjects(data);
    } catch (err) {
      setError("Failed to load projects");
    }
  };

  const handleJobTypeChange = (jobType) => {
    setSelectedJobType(jobType);
    setCalculationResult(null);

    // Initialize measurements with defaults
    if (templates[jobType]) {
      const defaultMeasurements = {};
      Object.keys(templates[jobType].measurements).forEach((key) => {
        const field = templates[jobType].measurements[key];
        if (field.default !== undefined) {
          defaultMeasurements[key] = field.default;
        } else {
          defaultMeasurements[key] = "";
        }
      });
      setMeasurements(defaultMeasurements);
    }
  };

  const handleMeasurementChange = (field, value) => {
    setMeasurements((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const calculateJob = async () => {
    if (!selectedJobType) {
      setError("Please select a job type");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/job-calculator/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_type: selectedJobType,
          measurements: measurements,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setCalculationResult(data.result);
      } else {
        setError(data.error || "Calculation failed");
      }
    } catch (err) {
      setError("Failed to calculate job");
    } finally {
      setLoading(false);
    }
  };

  const saveJobToProject = async () => {
    if (!selectedProject || !jobName || !calculationResult) {
      setError("Please select a project, enter a job name, and calculate the job first");
      return;
    }

    setSavingJob(true);
    setError("");

    try {
      const response = await fetch("/api/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          project_id: selectedProject,
          name: jobName,
          job_type: selectedJobType,
          description: jobDescription,
          measurements: measurements,
          calculation_result: calculationResult,
          status: "planned",
        }),
      });

      const data = await response.json();

      if (data.success) {
        setError("");
        setJobName("");
        setJobDescription("");
        setSelectedProject("");
        setCalculationResult(null);
        setSelectedJobType("");
        setMeasurements({});
        alert("✅ Job saved to project successfully!");
      } else {
        setError(data.error || "Failed to save job");
      }
    } catch (err) {
      setError("Failed to save job to project");
    } finally {
      setSavingJob(false);
    }
  };

  const renderMeasurementField = (fieldName, fieldConfig) => {
    const { type, label, required, options, default: defaultValue } = fieldConfig;

    if (type === "select") {
      return (
        <div key={fieldName} className="measurement-field">
          <label>
            {label}
            {required && "*"}
          </label>
          <select
            value={measurements[fieldName] || ""}
            onChange={(e) => handleMeasurementChange(fieldName, e.target.value)}
            required={required}
          >
            <option value="">Select {label}</option>
            {options.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
      );
    }

    return (
      <div key={fieldName} className="measurement-field">
        <label>
          {label}
          {required && "*"}
        </label>
        <input
          type="number"
          step="0.01"
          value={measurements[fieldName] || ""}
          onChange={(e) => handleMeasurementChange(fieldName, parseFloat(e.target.value) || "")}
          placeholder={defaultValue ? defaultValue.toString() : ""}
          required={required}
        />
      </div>
    );
  };

  const renderCalculationResult = () => {
    if (!calculationResult) return null;

    const { area_sqft, total_depth_inches, materials, layers, calculations, dimensions } = calculationResult;

    return (
      <div className="calculation-result">
        <h3>📊 Calculation Results</h3>

        <div className="result-summary">
          <h4>Summary</h4>
          <div className="summary-grid">
            {area_sqft && (
              <div>
                <strong>Area:</strong> {area_sqft} sq ft
              </div>
            )}
            {total_depth_inches && (
              <div>
                <strong>Total Depth:</strong> {total_depth_inches} inches
              </div>
            )}
            {dimensions && (
              <>
                <div>
                  <strong>Length:</strong> {dimensions.length_feet} ft
                </div>
                <div>
                  <strong>Height:</strong> {dimensions.height_feet} ft
                </div>
                {dimensions.width_feet && (
                  <div>
                    <strong>Width:</strong> {dimensions.width_feet} ft
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {materials && (
          <div className="materials-section">
            <h4>Materials Required</h4>
            <div className="materials-grid">
              {Object.entries(materials).map(([material, details]) => (
                <div key={material} className="material-item">
                  <h5>{material.charAt(0).toUpperCase() + material.slice(1)}</h5>
                  {Object.entries(details).map(([key, value]) => (
                    <div key={key}>
                      <strong>{key}:</strong> {value}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )}

        {layers && (
          <div className="layers-section">
            <h4>Layer Structure</h4>
            <div className="layers-list">
              {layers.map((layer, index) => (
                <div key={index} className="layer-item">
                  <strong>{layer.name}</strong> - {layer.depth} inches ({layer.material})
                </div>
              ))}
            </div>
          </div>
        )}

        {calculations && (
          <div className="calculations-section">
            <h4>Additional Calculations</h4>
            <div className="calculations-grid">
              {Object.entries(calculations).map(([key, value]) => (
                <div key={key}>
                  <strong>{key}:</strong> {value}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="job-calculator">
      <div className="calculator-header">
        <h2>🏗️ Job Calculator</h2>
        <p>Calculate materials and requirements for landscaping jobs</p>
      </div>

      <div className="calculator-content">
        <div className="job-type-selection">
          <h3>1. Select Job Type</h3>
          <div className="job-types-grid">
            {jobTypes.map((jobType) => (
              <button
                key={jobType}
                className={`job-type-btn ${selectedJobType === jobType ? "selected" : ""}`}
                onClick={() => handleJobTypeChange(jobType)}
              >
                {templates[jobType]?.name || jobType}
              </button>
            ))}
          </div>
        </div>

        {selectedJobType && templates[selectedJobType] && (
          <div className="measurements-section">
            <h3>2. Enter Measurements</h3>
            <p>{templates[selectedJobType].description}</p>

            <div className="measurements-form">
              {Object.entries(templates[selectedJobType].measurements).map(([fieldName, fieldConfig]) =>
                renderMeasurementField(fieldName, fieldConfig),
              )}
            </div>

            <button className="calculate-btn" onClick={calculateJob} disabled={loading}>
              {loading ? "Calculating..." : "Calculate Job"}
            </button>
          </div>
        )}

        {error && <div className="error-message">❌ {error}</div>}

        {renderCalculationResult()}

        {calculationResult && (
          <div className="project-assignment-section">
            <h3>3. Save to Project (Optional)</h3>
            <p>Save this calculated job to an existing project</p>

            <div className="project-assignment-form">
              <div className="form-group">
                <label>Job Name *</label>
                <input
                  type="text"
                  value={jobName}
                  onChange={(e) => setJobName(e.target.value)}
                  placeholder="Enter job name"
                  required
                />
              </div>

              <div className="form-group">
                <label>Job Description</label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Enter job description"
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label>Select Project *</label>
                <select value={selectedProject} onChange={(e) => setSelectedProject(e.target.value)} required>
                  <option value="">Choose a project...</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name} - {project.status}
                    </option>
                  ))}
                </select>
              </div>

              <button
                className="save-job-btn"
                onClick={saveJobToProject}
                disabled={savingJob || !selectedProject || !jobName}
              >
                {savingJob ? "Saving..." : "💾 Save Job to Project"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobCalculator;
