import React, { useState } from "react";
import "./App.css";
import MaterialsManagement from "./components/MaterialsManagement";
import ProjectsManagement from "./components/ProjectsManagement";
import Dashboard from "./components/Dashboard";
import TestAPI from "./components/TestAPI";
import MaterialsCalculator from "./components/MaterialsCalculator";
import JobCalculator from "./components/JobCalculator";

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [editJobData, setEditJobData] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const navigateToJobCalculator = (jobData) => {
    setEditJobData(jobData);
    setActiveTab("job-calculator");
  };

  const clearEditJobData = () => {
    setEditJobData(null);
  };

  const refreshProjectJobs = () => {
    // This will trigger a refresh of project jobs in ProjectsManagement
    setRefreshTrigger((prev) => prev + 1);
  };

  const renderActiveComponent = () => {
    switch (activeTab) {
      case "materials":
        return <MaterialsManagement />;
      case "projects":
        return <ProjectsManagement navigateToJobCalculator={navigateToJobCalculator} refreshTrigger={refreshTrigger} />;
      case "calculator":
        return <MaterialsCalculator />;
      case "job-calculator":
        return (
          <JobCalculator
            editJobData={editJobData}
            clearEditJobData={clearEditJobData}
            refreshProjectJobs={refreshProjectJobs}
          />
        );
      case "test":
        return <TestAPI />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏡 Landscaper Management System</h1>
        <nav className="nav-tabs">
          <button
            className={activeTab === "dashboard" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("dashboard")}
          >
            📊 Dashboard
          </button>
          <button
            className={activeTab === "materials" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("materials")}
          >
            📦 Materials
          </button>
          <button
            className={activeTab === "projects" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("projects")}
          >
            🏗️ Projects
          </button>
          <button
            className={activeTab === "calculator" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("calculator")}
          >
            🧮 Calculator
          </button>
          <button
            className={activeTab === "job-calculator" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("job-calculator")}
          >
            🏗️ Job Calculator
          </button>
          <button className={activeTab === "test" ? "nav-tab active" : "nav-tab"} onClick={() => setActiveTab("test")}>
            🔧 Test API
          </button>
        </nav>
      </header>

      <main className="app-main">{renderActiveComponent()}</main>
    </div>
  );
}

export default App;
