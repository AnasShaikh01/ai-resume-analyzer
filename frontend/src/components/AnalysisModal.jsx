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

        <h2>Scanning Resume...</h2>
        <p>Your resume is being analyzed for ATS compatibility.</p>

        <button className="cancel-btn" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export default AnalysisModal;
