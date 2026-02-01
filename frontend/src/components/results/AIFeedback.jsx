import React from "react";

const AIFeedback = ({ ai_raw }) => {
  if (!ai_raw) return null;

  const lines = ai_raw
    .split("\n")
    .map(line => line.trim())
    .filter(Boolean);

  return (
    <div className="ai-feedback">
      {lines.map((line, idx) => {
        // Heuristic: treat short, capitalized lines as headings
        const isHeading =
          line.length < 60 &&
          line === line.toUpperCase() ||
          /^[A-Z][A-Za-z\s]+:$/.test(line);

        // Heuristic: bullet points
        const isBullet =
          line.startsWith("-") ||
          line.startsWith("•") ||
          line.startsWith("*");

        if (isHeading) {
          return (
            <h4 key={idx} className="ai-heading">
              {line.replace(":", "")}
            </h4>
          );
        }

        if (isBullet) {
          return (
            <li key={idx} className="ai-bullet">
              {line.replace(/^[-•*]\s*/, "")}
            </li>
          );
        }

        return (
          <p key={idx} className="ai-paragraph">
            {line}
          </p>
        );
      })}
    </div>
  );
};

export default AIFeedback;
