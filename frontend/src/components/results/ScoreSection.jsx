import React from "react";

const ScoreItem = ({ label, value, color }) => {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="score-item">

      <div className="score-ring">

        <svg className="progress-ring" width="100" height="100">

          <circle
            className="progress-bg"
            stroke="#E5E7EB"
            strokeWidth="8"
            fill="transparent"
            r={radius}
            cx="50"
            cy="50"
          />

          <circle
            className="progress-value"
            stroke={color}
            strokeWidth="8"
            fill="transparent"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            r={radius}
            cx="50"
            cy="50"
          />

        </svg>

        <div className="score-percent">
          {value}%
        </div>

      </div>

      <div className="score-info">
        <p className="score-label">{label}</p>

        <p
          className="score-value"
          style={{ color }}
        >
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
