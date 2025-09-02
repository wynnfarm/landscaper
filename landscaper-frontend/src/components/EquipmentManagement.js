import React, { useState, useEffect } from "react";

const EquipmentManagement = () => {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch equipment from API
  const fetchEquipment = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/equipment/status");
      if (response.ok) {
        const data = await response.json();
        setEquipment(data);
      } else {
        console.error("Failed to fetch equipment");
      }
    } catch (error) {
      console.error("Error fetching equipment:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEquipment();
  }, []);

  // Handle equipment actions
  const handleEquipmentAction = async (equipmentId, action) => {
    try {
      const response = await fetch(`/api/equipment/${action}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ equipment_id: equipmentId }),
      });

      if (response.ok) {
        await fetchEquipment(); // Refresh the list
      } else {
        console.error(`Failed to ${action} equipment`);
      }
    } catch (error) {
      console.error(`Error ${action} equipment:`, error);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="equipment-management">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">🔧 Equipment Management</h2>
          <button className="btn btn-primary" onClick={fetchEquipment}>
            🔄 Refresh
          </button>
        </div>

        {/* Equipment Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Status</th>
                <th>Location</th>
                <th>Last Maintenance</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {equipment.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{item.equipment_type}</td>
                  <td>
                    <span
                      className={`status-badge ${
                        item.status === "available"
                          ? "status-active"
                          : item.status === "in_use"
                          ? "status-pending"
                          : item.status === "maintenance"
                          ? "status-warning"
                          : "status-inactive"
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>
                  <td>{item.current_location}</td>
                  <td>
                    {item.last_maintenance_date ? new Date(item.last_maintenance_date).toLocaleDateString() : "N/A"}
                  </td>
                  <td>
                    {item.status === "available" && (
                      <button
                        className="btn btn-sm btn-success"
                        onClick={() => handleEquipmentAction(item.id, "checkout")}
                      >
                        ✅ Checkout
                      </button>
                    )}
                    {item.status === "in_use" && (
                      <button
                        className="btn btn-sm btn-warning"
                        onClick={() => handleEquipmentAction(item.id, "checkin")}
                      >
                        🔄 Checkin
                      </button>
                    )}
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleEquipmentAction(item.id, "repair")}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🔧 Repair
                    </button>
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEquipmentAction(item.id, "maintenance")}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🛠️ Maintenance
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Mobile Card Layout */}
          <div className="mobile-cards">
            {equipment.map((item) => (
              <div key={item.id} className="mobile-card">
                <div className="mobile-card-header">{item.name}</div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Type:</span>
                  <span className="mobile-card-value">{item.equipment_type}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Status:</span>
                  <span className="mobile-card-value">
                    <span
                      className={`status-badge ${
                        item.status === "available"
                          ? "status-active"
                          : item.status === "in_use"
                          ? "status-pending"
                          : item.status === "maintenance"
                          ? "status-warning"
                          : "status-inactive"
                      }`}
                    >
                      {item.status}
                    </span>
                  </span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Location:</span>
                  <span className="mobile-card-value">{item.current_location}</span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Last Maintenance:</span>
                  <span className="mobile-card-value">
                    {item.last_maintenance_date ? new Date(item.last_maintenance_date).toLocaleDateString() : "N/A"}
                  </span>
                </div>
                <div className="mobile-card-row">
                  <span className="mobile-card-label">Actions:</span>
                  <span className="mobile-card-value">
                    {item.status === "available" && (
                      <button
                        className="btn btn-sm btn-success"
                        onClick={() => handleEquipmentAction(item.id, "checkout")}
                      >
                        ✅ Checkout
                      </button>
                    )}
                    {item.status === "in_use" && (
                      <button
                        className="btn btn-sm btn-warning"
                        onClick={() => handleEquipmentAction(item.id, "checkin")}
                      >
                        🔄 Checkin
                      </button>
                    )}
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleEquipmentAction(item.id, "repair")}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🔧 Repair
                    </button>
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEquipmentAction(item.id, "maintenance")}
                      style={{ marginLeft: "0.5rem" }}
                    >
                      🛠️ Maintenance
                    </button>
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {equipment.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem", color: "#6b7280" }}>No equipment found.</div>
        )}
      </div>
    </div>
  );
};

export default EquipmentManagement;
