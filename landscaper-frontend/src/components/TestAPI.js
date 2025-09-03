import React, { useState, useEffect } from "react";

const TestAPI = () => {
  const [results, setResults] = useState({});

  useEffect(() => {
    const testEndpoints = async () => {
      const endpoints = [
        "/api/materials",
        "/api/projects",
        "/api/crew",
        "/api/equipment",
        "/api/jobs",
        "/api/job-calculator/types",
      ];

      const testResults = {};

      for (const endpoint of endpoints) {
        try {
          console.log(`Testing ${endpoint}...`);
          const response = await fetch(endpoint);
          const data = await response.json();
          testResults[endpoint] = {
            status: response.status,
            ok: response.ok,
            data: data,
            error: null,
          };
        } catch (error) {
          testResults[endpoint] = {
            status: "error",
            ok: false,
            data: null,
            error: error.message,
          };
        }
      }

      setResults(testResults);
    };

    testEndpoints();
  }, []);

  return (
    <div className="card">
      <h2>API Test Results</h2>
      {Object.entries(results).map(([endpoint, result]) => (
        <div key={endpoint} style={{ marginBottom: "1rem", padding: "1rem", border: "1px solid #ccc" }}>
          <h3>{endpoint}</h3>
          <p>
            <strong>Status:</strong> {result.status}
          </p>
          <p>
            <strong>OK:</strong> {result.ok ? "Yes" : "No"}
          </p>
          {result.error && (
            <p>
              <strong>Error:</strong> {result.error}
            </p>
          )}
          <p>
            <strong>Data:</strong> {JSON.stringify(result.data, null, 2)}
          </p>
        </div>
      ))}
    </div>
  );
};

export default TestAPI;
