import React, { useState } from "react";
import "./App.css";
import MaterialsManagement from "./components/MaterialsManagement";
import EquipmentManagement from "./components/EquipmentManagement";
import ProjectsManagement from "./components/ProjectsManagement";
import CrewManagement from "./components/CrewManagement";
import Dashboard from "./components/Dashboard";
import TestAPI from "./components/TestAPI";
import MaterialsCalculator from "./components/MaterialsCalculator";
import ProjectDesigner from "./components/ProjectDesigner";

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");

  const renderActiveComponent = () => {
    switch (activeTab) {
      case "materials":
        return <MaterialsManagement />;
      case "equipment":
        return <EquipmentManagement />;
      case "projects":
        return <ProjectsManagement />;
      case "crew":
        return <CrewManagement />;
      case "calculator":
        return <MaterialsCalculator />;
      case "designer":
        return <ProjectDesigner />;
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
            className={activeTab === "equipment" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("equipment")}
          >
            🔧 Equipment
          </button>
          <button
            className={activeTab === "projects" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("projects")}
          >
            🏗️ Projects
          </button>
          <button className={activeTab === "crew" ? "nav-tab active" : "nav-tab"} onClick={() => setActiveTab("crew")}>
            👥 Crew
          </button>
          <button
            className={activeTab === "calculator" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("calculator")}
          >
            🧮 Calculator
          </button>
          <button
            className={activeTab === "designer" ? "nav-tab active" : "nav-tab"}
            onClick={() => setActiveTab("designer")}
          >
            🎨 Designer
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
