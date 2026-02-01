// src/components/Features.jsx
import React from "react";
import "./Features.css";
import { FiLayers, FiTarget, FiSearch, FiTrendingUp } from "react-icons/fi";

const Features = () => {
  return (
    <div className="features-container">

      <h2 className="features-heading">Powerful Features to Improve Your Resume</h2>
      <p className="features-subtitle">
        Get detailed, AI-driven insights to increase your chances of getting shortlisted.
      </p>

      <div className="features-grid">

        {/* CARD 1 - Multiple JD Comparison */}
        <div className="feature-card">
          <div className="feature-icon">
            <FiLayers />
          </div>
          <h3>Compare Across Multiple JDs</h3>
          <p>
            Analyze your resume against several job descriptions to find your best-fit roles
            and see which JD matches highest.
          </p>
        </div>

        {/* CARD 2 - ATS Score */}
        <div className="feature-card">
          <div className="feature-icon">
            <FiTarget />
          </div>
          <h3>ATS Match Score</h3>
          <p>
            Receive a detailed ATS score breakdown for each JD showing how well your resume meets recruiters' criteria.
          </p>
        </div>

        {/* CARD 3 - Keyword Insights */}
        <div className="feature-card">
          <div className="feature-icon">
            <FiSearch />
          </div>
          <h3>Keyword & Skills Insights</h3>
          <p>
            Identify missing skills, important keywords, and strengths extracted from both your resume and job role.
          </p>
        </div>

      </div>
    </div>
  );
};

export default Features;
