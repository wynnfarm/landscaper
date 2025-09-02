import React, { useState, useRef, useEffect } from "react";

const ProjectDesigner = () => {
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [projectName, setProjectName] = useState("");
  const [projectElements, setProjectElements] = useState([]);
  const [selectedElement, setSelectedElement] = useState(null);
  const [showElementPanel, setShowElementPanel] = useState(false);
  const [designMode, setDesignMode] = useState("view"); // view, edit, measure
  const canvasRef = useRef(null);

  // Project templates
  const projectTemplates = [
    {
      id: "residential_backyard",
      name: "Residential Backyard",
      description: "Complete backyard transformation with patio, retaining wall, and garden beds",
      thumbnail: "🏡",
      elements: [
        { type: "patio", x: 20, y: 30, width: 15, height: 12, material: "concrete_pavers" },
        { type: "retaining_wall", x: 10, y: 50, width: 25, height: 4, material: "versa_lok_standard" },
        { type: "garden_bed", x: 5, y: 10, width: 8, height: 6, plants: ["roses", "lavender"] },
        { type: "pathway", x: 35, y: 20, width: 3, height: 15, material: "stone_pavers" },
      ],
    },
    {
      id: "commercial_entrance",
      name: "Commercial Entrance",
      description: "Professional entrance design with hardscaping and seasonal plants",
      thumbnail: "🏢",
      elements: [
        { type: "entrance_patio", x: 15, y: 25, width: 20, height: 10, material: "concrete" },
        { type: "retaining_wall", x: 5, y: 40, width: 30, height: 3, material: "natural_stone" },
        { type: "planting_area", x: 40, y: 15, width: 12, height: 8, plants: ["boxwood", "annuals"] },
        { type: "lighting", x: 18, y: 28, type: "path_lights", quantity: 6 },
      ],
    },
    {
      id: "garden_retreat",
      name: "Garden Retreat",
      description: "Peaceful garden space with water features and native plants",
      thumbnail: "🌿",
      elements: [
        { type: "water_feature", x: 25, y: 25, width: 8, height: 6, style: "pond" },
        { type: "garden_path", x: 20, y: 35, width: 2, height: 10, material: "gravel" },
        { type: "seating_area", x: 15, y: 15, width: 6, height: 4, material: "stone" },
        { type: "planting_beds", x: 35, y: 20, width: 10, height: 15, plants: ["native_grasses", "wildflowers"] },
      ],
    },
  ];

  // Design elements library
  const designElements = [
    {
      category: "Hardscaping",
      elements: [
        { type: "patio", name: "Patio", icon: "🏠", materials: ["concrete", "pavers", "stone"] },
        {
          type: "retaining_wall",
          name: "Retaining Wall",
          icon: "🧱",
          materials: ["concrete_blocks", "natural_stone", "timber"],
        },
        { type: "pathway", name: "Pathway", icon: "🛤️", materials: ["pavers", "gravel", "stone"] },
        { type: "steps", name: "Steps", icon: "📶", materials: ["stone", "concrete", "wood"] },
      ],
    },
    {
      category: "Landscaping",
      elements: [
        { type: "garden_bed", name: "Garden Bed", icon: "🌱", plants: ["annuals", "perennials", "shrubs"] },
        { type: "tree", name: "Tree", icon: "🌳", varieties: ["oak", "maple", "cherry", "pine"] },
        { type: "hedge", name: "Hedge", icon: "🌿", plants: ["boxwood", "privet", "holly"] },
        { type: "lawn", name: "Lawn", icon: "🌾", grass_types: ["fescue", "bermuda", "zoysia"] },
      ],
    },
    {
      category: "Features",
      elements: [
        { type: "water_feature", name: "Water Feature", icon: "💧", styles: ["fountain", "pond", "stream"] },
        { type: "fire_pit", name: "Fire Pit", icon: "🔥", materials: ["stone", "metal", "concrete"] },
        { type: "lighting", name: "Lighting", icon: "💡", types: ["path_lights", "spotlights", "string_lights"] },
        { type: "seating", name: "Seating", icon: "🪑", materials: ["wood", "stone", "metal"] },
      ],
    },
  ];

  // Material options
  const materialOptions = {
    concrete: { name: "Concrete", cost: 8.5, unit: "sq ft" },
    pavers: { name: "Concrete Pavers", cost: 12.0, unit: "sq ft" },
    stone: { name: "Natural Stone", cost: 25.0, unit: "sq ft" },
    concrete_blocks: { name: "Concrete Blocks", cost: 4.5, unit: "block" },
    natural_stone: { name: "Natural Stone", cost: 150.0, unit: "ton" },
    timber: { name: "Landscape Timber", cost: 15.0, unit: "piece" },
    gravel: { name: "Gravel", cost: 35.0, unit: "cubic yard" },
  };

  useEffect(() => {
    if (selectedTemplate) {
      setProjectElements([...selectedTemplate.elements]);
      setProjectName(`${selectedTemplate.name} Project`);
    }
  }, [selectedTemplate]);

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setShowElementPanel(false);
  };

  const handleElementSelect = (element) => {
    setSelectedElement(element);
    setShowElementPanel(true);
  };

  const addElementToProject = (elementType, elementData) => {
    const newElement = {
      id: Date.now(),
      type: elementType,
      x: 50,
      y: 50,
      width: 10,
      height: 8,
      ...elementData,
    };
    setProjectElements([...projectElements, newElement]);
  };

  const updateElement = (elementId, updates) => {
    setProjectElements(projectElements.map((el) => (el.id === elementId ? { ...el, ...updates } : el)));
  };

  const deleteElement = (elementId) => {
    setProjectElements(projectElements.filter((el) => el.id !== elementId));
    setSelectedElement(null);
    setShowElementPanel(false);
  };

  const calculateProjectCost = () => {
    return projectElements.reduce((total, element) => {
      if (element.material && materialOptions[element.material]) {
        const area = element.width * element.height;
        return total + area * materialOptions[element.material].cost;
      }
      return total;
    }, 0);
  };

  const exportProject = () => {
    const projectData = {
      name: projectName,
      elements: projectElements,
      totalCost: calculateProjectCost(),
      created: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(projectData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${projectName.replace(/\s+/g, "_")}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const renderTemplateGallery = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">📋 Project Templates</h3>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))", gap: "1rem" }}>
        {projectTemplates.map((template) => (
          <div
            key={template.id}
            className="template-card"
            onClick={() => handleTemplateSelect(template)}
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              padding: "1rem",
              cursor: "pointer",
              transition: "all 0.3s ease",
              backgroundColor: selectedTemplate?.id === template.id ? "#f0f9ff" : "white",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>{template.thumbnail}</div>
            <h4 style={{ margin: "0 0 0.5rem 0" }}>{template.name}</h4>
            <p style={{ margin: 0, fontSize: "0.875rem", color: "#6b7280" }}>{template.description}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderDesignCanvas = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">🎨 Design Canvas</h3>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            className={`btn btn-sm ${designMode === "view" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setDesignMode("view")}
          >
            👁️ View
          </button>
          <button
            className={`btn btn-sm ${designMode === "edit" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setDesignMode("edit")}
          >
            ✏️ Edit
          </button>
          <button
            className={`btn btn-sm ${designMode === "measure" ? "btn-primary" : "btn-secondary"}`}
            onClick={() => setDesignMode("measure")}
          >
            📏 Measure
          </button>
        </div>
      </div>

      <div
        ref={canvasRef}
        style={{
          width: "100%",
          height: "400px",
          border: "2px solid #e5e7eb",
          borderRadius: "8px",
          position: "relative",
          backgroundColor: "#f9fafb",
          overflow: "hidden",
        }}
      >
        {projectElements.map((element) => (
          <div
            key={element.id}
            onClick={() => handleElementSelect(element)}
            style={{
              position: "absolute",
              left: `${element.x}%`,
              top: `${element.y}%`,
              width: `${element.width}%`,
              height: `${element.height}%`,
              border: selectedElement?.id === element.id ? "3px solid #3b82f6" : "2px solid #d1d5db",
              borderRadius: "4px",
              backgroundColor: getElementColor(element.type),
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.5rem",
              transition: "all 0.3s ease",
            }}
          >
            {getElementIcon(element.type)}
          </div>
        ))}
      </div>
    </div>
  );

  const renderElementPanel = () => {
    if (!selectedElement || !showElementPanel) return null;

    return (
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">⚙️ Element Properties</h3>
          <button className="btn btn-sm btn-danger" onClick={() => deleteElement(selectedElement.id)}>
            🗑️ Delete
          </button>
        </div>

        <div style={{ display: "grid", gap: "1rem" }}>
          <div className="form-group">
            <label className="form-label">Position X (%)</label>
            <input
              type="number"
              value={selectedElement.x}
              onChange={(e) => updateElement(selectedElement.id, { x: parseFloat(e.target.value) })}
              className="form-input"
              min="0"
              max="100"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Position Y (%)</label>
            <input
              type="number"
              value={selectedElement.y}
              onChange={(e) => updateElement(selectedElement.id, { y: parseFloat(e.target.value) })}
              className="form-input"
              min="0"
              max="100"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Width (%)</label>
            <input
              type="number"
              value={selectedElement.width}
              onChange={(e) => updateElement(selectedElement.id, { width: parseFloat(e.target.value) })}
              className="form-input"
              min="1"
              max="100"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Height (%)</label>
            <input
              type="number"
              value={selectedElement.height}
              onChange={(e) => updateElement(selectedElement.id, { height: parseFloat(e.target.value) })}
              className="form-input"
              min="1"
              max="100"
            />
          </div>

          {selectedElement.material && (
            <div className="form-group">
              <label className="form-label">Material</label>
              <select
                value={selectedElement.material}
                onChange={(e) => updateElement(selectedElement.id, { material: e.target.value })}
                className="form-select"
              >
                {Object.entries(materialOptions).map(([key, material]) => (
                  <option key={key} value={key}>
                    {material.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderElementLibrary = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">📚 Element Library</h3>
      </div>

      {designElements.map((category) => (
        <div key={category.category} style={{ marginBottom: "1.5rem" }}>
          <h4 style={{ margin: "0 0 0.5rem 0", color: "#374151" }}>{category.category}</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: "0.5rem" }}>
            {category.elements.map((element) => (
              <button
                key={element.type}
                className="btn btn-secondary"
                onClick={() => addElementToProject(element.type, { material: element.materials?.[0] })}
                style={{ fontSize: "0.875rem", padding: "0.5rem" }}
              >
                <div style={{ fontSize: "1.25rem", marginBottom: "0.25rem" }}>{element.icon}</div>
                {element.name}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  const renderProjectSummary = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">📊 Project Summary</h3>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <div className="form-group">
          <label className="form-label">Project Name</label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            className="form-input"
            placeholder="Enter project name"
          />
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
          gap: "1rem",
          marginBottom: "1rem",
        }}
      >
        <div style={{ textAlign: "center", padding: "1rem", backgroundColor: "#f0f9ff", borderRadius: "8px" }}>
          <div style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>🏗️</div>
          <div style={{ fontWeight: "600" }}>{projectElements.length}</div>
          <div style={{ fontSize: "0.875rem", color: "#6b7280" }}>Elements</div>
        </div>

        <div style={{ textAlign: "center", padding: "1rem", backgroundColor: "#f0fdf4", borderRadius: "8px" }}>
          <div style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>💰</div>
          <div style={{ fontWeight: "600" }}>${calculateProjectCost().toFixed(2)}</div>
          <div style={{ fontSize: "0.875rem", color: "#6b7280" }}>Estimated Cost</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button className="btn btn-primary" onClick={exportProject}>
          📤 Export Project
        </button>
        <button className="btn btn-secondary" onClick={() => window.print()}>
          🖨️ Print Design
        </button>
      </div>
    </div>
  );

  const getElementColor = (type) => {
    const colors = {
      patio: "#e5e7eb",
      retaining_wall: "#d1d5db",
      pathway: "#f3f4f6",
      garden_bed: "#dcfce7",
      tree: "#bbf7d0",
      water_feature: "#dbeafe",
      fire_pit: "#fed7aa",
      lighting: "#fef3c7",
    };
    return colors[type] || "#f9fafb";
  };

  const getElementIcon = (type) => {
    const icons = {
      patio: "🏠",
      retaining_wall: "🧱",
      pathway: "🛤️",
      garden_bed: "🌱",
      tree: "🌳",
      water_feature: "💧",
      fire_pit: "🔥",
      lighting: "💡",
    };
    return icons[type] || "📦";
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🎨 Project Designer</h2>
        </div>
        <p style={{ margin: "0", color: "#6b7280" }}>
          Create and visualize landscaping projects with our interactive design tool.
        </p>
      </div>

      {!selectedTemplate ? (
        renderTemplateGallery()
      ) : (
        <div style={{ display: "grid", gap: "1.5rem" }}>
          {renderDesignCanvas()}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
            {renderElementLibrary()}
            {renderElementPanel()}
          </div>

          {renderProjectSummary()}

          <div style={{ textAlign: "center" }}>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setSelectedTemplate(null);
                setProjectElements([]);
                setProjectName("");
                setSelectedElement(null);
                setShowElementPanel(false);
              }}
            >
              🔄 Start New Project
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectDesigner;
