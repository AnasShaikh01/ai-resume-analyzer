import React from "react";
import "./AnalysisModal.css";
import { FiSettings } from "react-icons/fi";

const AnalysisModal = ({ onCancel }) => {
  return (
    <div className="analysis-modal-backdrop">
      <div className="analysis-modal">
        <div className="analysis-icon">
          <FiSettings />
        </div>

        <h2>Analyzing Your Resume</h2>
        <p>
        Our AI is extracting content, matching skills against the job description,
        calculating ATS compatibility, and generating personalized recommendations.
        </p>
        <div className="analysis-progress">
          <div className="analysis-progress-bar"></div>
        </div>

        <div className="analysis-status">
          <span>Extracting Resume</span>
          <span>Matching Skills</span>
          <span>Calculating ATS</span>
        </div>

        <button className="cancel-btn" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export default AnalysisModal;
