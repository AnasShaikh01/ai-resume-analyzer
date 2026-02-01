import React from "react";

const ScoreItem = ({ label, value, color }) => {
  return (
    <div className="score-item">
      <div className="score-ring" style={{ borderColor: color }}>
        <span>{value}%</span>
      </div>

      <div className="score-info">
        <p className="score-label">{label}</p>
        <p className="score-value" style={{ color }}>
          {value}%
        </p>
      </div>
    </div>
  );
};

const ScoreSection = ({ overall, requirements, keywords }) => {
  return (
    <div className="score-row">
      <ScoreItem
        label="Overall Score"
        value={overall}
        color="var(--primary-color)"
      />
      <ScoreItem
        label="Requirements Score"
        value={requirements}
        color="var(--success-color)"
      />
      <ScoreItem
        label="Keywords Score"
        value={keywords}
        color="var(--accent-color)"
      />
    </div>
  );
};

export default ScoreSection;
