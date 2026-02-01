import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import AnalysisReport from "../components/results/AnalysisReport";
import "../components/results/results.css";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const analysisData = location.state?.analysisData;

  // ✅ Hook MUST be before any return
  const [activeJD, setActiveJD] = useState(0);

  if (!analysisData || analysisData.length === 0) {
    return (
      <div style={{ padding: 60, textAlign: "center" }}>
        <h2>No result found</h2>
        <button onClick={() => navigate("/")}>Go Back</button>
      </div>
    );
  }

  return (
    <div className="results-page">
      <header className="results-header">
        <h1>Resume Analysis Results</h1>
        <p>AI-powered evaluation of your resume</p>
      </header>

      {/* JD Tabs */}
      {analysisData.length > 1 && (
        <div className="jd-tabs">
          {analysisData.map((_, index) => (
            <button
              key={index}
              className={`jd-tab ${activeJD === index ? "active" : ""}`}
              onClick={() => setActiveJD(index)}
            >
              Job Description {index + 1}
            </button>
          ))}
        </div>
      )}

      {/* Selected JD Report */}
      <AnalysisReport result={analysisData[activeJD]} />
    </div>
  );
};

export default ResultsPage;
