import React, { useState, useEffect } from "react";

const CrewManagement = () => {
  const [crew, setCrew] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch crew from API
  const fetchCrew = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/crew");
      if (response.ok) {
        const data = await response.json();
        setCrew(data);
      } else {
        console.error("Failed to fetch crew");
      }
    } catch (error) {
      console.error("Error fetching crew:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCrew();
  }, []);

  // Handle crew member status update
  const handleStatusUpdate = async (crewId, newStatus) => {
    try {
      const response = await fetch("/api/crew/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          crew_id: crewId,
          status: newStatus,
        }),
      });

      if (response.ok) {
        await fetchCrew(); // Refresh the list
      } else {
        console.error("Failed to update crew member status");
      }
    } catch (error) {
      console.error("Error updating crew member status:", error);
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
    <div className="crew-management">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">👥 Crew Management</h2>
          <button className="btn btn-primary" onClick={fetchCrew}>
            🔄 Refresh
          </button>
        </div>

        {/* Crew Table */}
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Status</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Hire Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {crew.map((member) => (
                <tr key={member.id}>
                  <td>
                    {member.first_name} {member.last_name}
                  </td>
                  <td>{member.position}</td>
                  <td>
                    <span
                      className={`status-badge ${
                        member.status === "active"
                          ? "status-active"
                          : member.status === "on_leave"
                          ? "status-warning"
                          : "status-inactive"
                      }`}
                    >
                      {member.status}
                    </span>
                  </td>
                  <td>{member.phone}</td>
                  <td>{member.email}</td>
                  <td>{member.hire_date ? new Date(member.hire_date).toLocaleDateString() : "N/A"}</td>
                  <td>
                    <select
                      value={member.status}
                      onChange={(e) => handleStatusUpdate(member.id, e.target.value)}
                      className="form-select"
                      style={{ minWidth: "120px" }}
                    >
                      <option value="active">Active</option>
                      <option value="on_leave">On Leave</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {crew.length === 0 && (
          <div style={{ textAlign: "center", padding: "2rem", color: "#6b7280" }}>No crew members found.</div>
        )}
      </div>
    </div>
  );
};

export default CrewManagement;
