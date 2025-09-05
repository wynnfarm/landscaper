import React, { useState, useEffect } from "react";

const MaterialsManagement = () => {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingMaterial, setEditingMaterial] = useState(null);
  const [materialTypes, setMaterialTypes] = useState([]);
  const [loadingMaterialTypes, setLoadingMaterialTypes] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");

  const [formData, setFormData] = useState({
    name: "",
    material_type: "",
    description: "",
    unit_of_measure: "",
    price_per_unit: "",
    supplier: "",
    supplier_contact: "",
    notes: "",
  });

  // Fetch materials from API
  const fetchMaterials = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/materials");
      if (response.ok) {
        const data = await response.json();
        setMaterials(data);
      } else {
        console.error("Failed to fetch materials");
      }
    } catch (error) {
      console.error("Error fetching materials:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMaterialTypes = async () => {
    try {
      setLoadingMaterialTypes(true);
      const response = await fetch("/api/materials/types");
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setMaterialTypes(data.types);
        }
      }
    } catch (error) {
      console.error("Error fetching material types:", error);
    } finally {
      setLoadingMaterialTypes(false);
    }
  };

  useEffect(() => {
    fetchMaterials();
    fetchMaterialTypes();
  }, []);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const url = editingMaterial ? `/api/materials/edit/${editingMaterial.id}` : "/api/materials/add";

      const method = editingMaterial ? "POST" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await fetchMaterials(); // Refresh the list
        setShowModal(false);
        setEditingMaterial(null);
        setFormData({
          name: "",
          material_type: "",
          description: "",
          unit_of_measure: "",
          price_per_unit: "",
          supplier: "",
          supplier_contact: "",
          notes: "",
        });
      } else {
        console.error("Failed to save material");
      }
    } catch (error) {
      console.error("Error saving material:", error);
    }
  };

  // Handle edit
  const handleEdit = (material) => {
    setEditingMaterial(material);
    setFormData({
      name: material.name || "",
      material_type: material.material_type || "",
      description: material.description || "",
      unit_of_measure: material.unit_of_measure || "",
      price_per_unit: material.price_per_unit || "",
      supplier: material.supplier || "",
      supplier_contact: material.supplier_contact || "",
      notes: material.notes || "",
    });
    setShowModal(true);
  };

  // Handle delete
  const handleDelete = async (materialId) => {
    if (window.confirm("Are you sure you want to delete this material?")) {
      try {
        const response = await fetch(`/api/materials/delete/${materialId}`, {
          method: "POST",
        });

        if (response.ok) {
          await fetchMaterials(); // Refresh the list
        } else {
          console.error("Failed to delete material");
        }
      } catch (error) {
        console.error("Error deleting material:", error);
      }
    }
  };

  // Filter materials
  const filteredMaterials = materials.filter((material) => {
    const matchesSearch =
      material.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      material.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      material.supplier?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesFilter = filterType === "all" || material.material_type === filterType;

    return matchesSearch && matchesFilter;
  });

  // Get unique material types for filter
  const uniqueMaterialTypes = [...new Set(materials.map((m) => m.material_type).filter(Boolean))];

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="materials-management">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">📦 Materials Management</h2>
          <button
            className="btn btn-primary"
            onClick={() => {
              setEditingMaterial(null);
              setFormData({
                name: "",
                material_type: "",
                description: "",
                unit_of_measure: "",
                price_per_unit: "",
                supplier: "",
                supplier_contact: "",
                notes: "",
              });
              setShowModal(true);
            }}
          >
            ➕ Add Material
          </button>
        </div>

        {/* Search and Filter */}
        <div style={{ marginBottom: "1rem", display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            type="text"
            placeholder="Search materials..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-input"
            style={{ flex: "1", minWidth: "200px" }}
          />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="form-select"
            style={{ minWidth: "150px" }}
          >
            <option value="all">All Types</option>
            {uniqueMaterialTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Materials Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Description</th>
                <th>Unit</th>
                <th>Cost/Unit</th>
                <th>Supplier</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredMaterials.map((material) => (
                <tr key={material.id}>
                  <td>{material.name}</td>
                  <td>
                    <span className="status-badge status-active">{material.material_type}</span>
                  </td>
                  <td>{material.description}</td>
                  <td>{material.unit_of_measure}</td>
                  <td>${material.price_per_unit}</td>
                  <td>{material.supplier}</td>
                  <td>
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEdit(material)}>
                      ✏️ Edit
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(material.id)}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🗑️ Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Mobile Card Layout */}
          <div className="mobile-cards">
            {filteredMaterials.map((material) => (
              <div key={material.id} className="mobile-card">
                <div className="mobile-card-header">{material.name}</div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Type:</span>
                  <span className="mobile-card-value">
                    <span className="status-badge status-active">{material.material_type}</span>
                  </span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Description:</span>
                  <span className="mobile-card-value">{material.description}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Unit:</span>
                  <span className="mobile-card-value">{material.unit_of_measure}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Cost/Unit:</span>
                  <span className="mobile-card-value">${material.price_per_unit}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Supplier:</span>
                  <span className="mobile-card-value">{material.supplier}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Actions:</span>
                  <span className="mobile-card-value">
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEdit(material)}>
                      ✏️ Edit
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(material.id)}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🗑️ Delete
                    </button>
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {filteredMaterials.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem", color: "#6b7280" }}>
            No materials found.{" "}
            {materials.length === 0 ? "Add your first material!" : "Try adjusting your search or filter."}
          </div>
        )}
      </div>

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">{editingMaterial ? "Edit Material" : "Add New Material"}</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Material Type *</label>
                <select
                  name="material_type"
                  value={formData.material_type}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                  disabled={loadingMaterialTypes}
                >
                  <option value="">Select Type</option>
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

              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="form-input"
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Unit of Measure</label>
                <input
                  type="text"
                  name="unit_of_measure"
                  value={formData.unit_of_measure}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="e.g., cubic yard, ton, piece"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Price per Unit</label>
                <input
                  type="number"
                  name="price_per_unit"
                  value={formData.price_per_unit}
                  onChange={handleInputChange}
                  className="form-input"
                  step="0.01"
                  min="0"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Supplier</label>
                <input
                  type="text"
                  name="supplier"
                  value={formData.supplier}
                  onChange={handleInputChange}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Supplier Contact</label>
                <input
                  type="text"
                  name="supplier_contact"
                  value={formData.supplier_contact}
                  onChange={handleInputChange}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Notes</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  className="form-input"
                  rows="3"
                />
              </div>

              <div style={{ display: "flex", gap: "1rem", justifyContent: "flex-end" }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingMaterial ? "Update Material" : "Add Material"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MaterialsManagement;
