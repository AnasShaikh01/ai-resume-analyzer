import React from "react";
import {
  FiTarget,
  FiFileText,
  FiLayers,
  FiShuffle
} from "react-icons/fi";
import "./AnalysisOutcome.css";

const outcomes = [
  {
    icon: <FiTarget />,
    title: "Tailored Scoring for Job Descriptions",
    desc: "Your resume is evaluated against specific job descriptions, ensuring relevance to the role you are targeting."
  },
  {
    icon: <FiFileText />,
    title: "AI-Generated Feedback Report",
    desc: "Get a clear AI-generated report highlighting strengths, gaps, and actionable improvements."
  },
  {
    icon: <FiLayers />,
    title: "Role-Specific Resume Insights",
    desc: "Understand how your experience and skills align with the specific job role requirements."
  },
  {
    icon: <FiShuffle />,
    title: "Multiple Job Description Comparison",
    desc: "Compare your resume against multiple job descriptions to identify the best-fit role."
  }
];

const AnalysisOutcome = () => {
  return (
    <section className="analysis-outcome">
      <div className="outcome-container">
        <h2 className="outcome-title">
          Why Choose Our AI Resume Analyzer?
        </h2>

        <p className="outcome-subtitle">
          Built to provide accurate, role-focused resume analysis with clear
          and actionable insights.
        </p>

        <div className="outcome-grid">
          {outcomes.map((item, index) => (
            <div className="outcome-card" key={index}>
              <div className="outcome-icon">{item.icon}</div>
              <h3 className="outcome-card-title">{item.title}</h3>
              <p className="outcome-card-desc">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AnalysisOutcome;
