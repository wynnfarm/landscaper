import React, { useState, useEffect } from "react";

const Dashboard = () => {
  const [stats, setStats] = useState({
    materials: 0,
    projects: 0,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Fetch materials count
        const materialsResponse = await fetch("/api/materials");
        const materialsData = (await materialsResponse.ok) ? await materialsResponse.json() : [];

        // Fetch projects count
        const projectsResponse = await fetch("/api/projects");
        const projectsData = (await projectsResponse.ok) ? await projectsResponse.json() : [];

        setStats({
          materials: materialsData.length,
          projects: projectsData.length,
        });
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="card">
        <h2 className="card-title">📊 Dashboard Overview</h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "1.5rem",
            marginBottom: "2rem",
          }}
        >
          <div
            className="stat-card"
            style={{
              background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
              color: "white",
              padding: "1.5rem",
              borderRadius: "12px",
              textAlign: "center",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>📦</div>
            <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{stats.materials}</div>
            <div>Materials</div>
          </div>

          <div
            className="stat-card"
            style={{
              background: "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
              color: "white",
              padding: "1.5rem",
              borderRadius: "12px",
              textAlign: "center",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🔧</div>
            <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{stats.equipment}</div>
            <div>Equipment</div>
          </div>

          <div
            className="stat-card"
            style={{
              background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
              color: "white",
              padding: "1.5rem",
              borderRadius: "12px",
              textAlign: "center",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🏗️</div>
            <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{stats.projects}</div>
            <div>Projects</div>
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "1.5rem",
          }}
        >
          <div className="card">
            <h3 style={{ marginBottom: "1rem", color: "#1f2937" }}>🚀 Quick Actions</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              <button className="btn btn-primary">📦 Add New Material</button>
              <button className="btn btn-success">🏗️ Create New Project</button>
            </div>
          </div>

          <div className="card">
            <h3 style={{ marginBottom: "1rem", color: "#1f2937" }}>📈 Recent Activity</h3>
            <div style={{ color: "#6b7280", fontStyle: "italic" }}>Activity tracking coming soon...</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
