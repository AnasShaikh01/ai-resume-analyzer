import React from "react";

const AIFeedback = ({ ai_raw }) => {
  if (!ai_raw) return null;

  const lines = ai_raw
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  return (
    <div className="ai-feedback">

      <div className="ai-report-header">
        <div className="ai-badge">AI Report</div>

        <h3 className="ai-report-title">
          Resume Analysis & Recommendations
        </h3>

        <p className="ai-report-subtitle">
          AI-generated insights based on your resume and the selected job description.
        </p>
      </div>

      <div className="ai-report-content">

        {lines.map((line, idx) => {

          const isHeading =
            (line.length < 60 && line === line.toUpperCase()) ||
            /^[A-Z][A-Za-z\s]+:$/.test(line);

          const isBullet =
            line.startsWith("-") ||
            line.startsWith("•") ||
            line.startsWith("*");

          if (isHeading) {
            return (
              <div className="ai-section" key={idx}>
                <h4 className="ai-heading">
                  {line.replace(":", "")}
                </h4>
              </div>
            );
          }

          if (isBullet) {
            return (
              <div className="ai-bullet" key={idx}>
                <span className="bullet-dot"></span>

                <span className="bullet-text">
                  {line.replace(/^[-•*]\s*/, "")}
                </span>
              </div>
            );
          }

          return (
            <p
              key={idx}
              className="ai-paragraph"
            >
              {line}
            </p>
          );

        })}

      </div>

    </div>
  );
};

export default AIFeedback;