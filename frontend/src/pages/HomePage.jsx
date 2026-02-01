// src/pages/HomePage.jsx
import React from "react";
import AnalysisForm from "../components/AnalysisForm";
import Features from "../components/Features";
import AnalysisOutcome from "../components/AnalysisOutcome";
import Footer from "../components/Footer";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="homepage">

      {/* HERO SECTION */}
      <section className="hero-section">

        {/* Eyebrow / Context (Reference style) */}
        <p className="hero-eyebrow">
          AI Resume Analyzer
        </p>

        {/* Main Headline */}
        <h1 className="hero-title">
          Optimize Your Resume with <span>AI-Powered Insights</span>
        </h1>

        {/* Supporting Subheadline */}
        <p className="hero-subtitle">
          Upload your resume and compare it against multiple job descriptions
          to receive ATS scores, keyword insights, and improvement suggestions.
        </p>

        {/* FORM + HOW IT WORKS */}
        <div className="form-info-row">

          {/* LEFT → FORM */}
          <div className="upload-card">
            <AnalysisForm />
          </div>

          {/* RIGHT → HOW IT WORKS */}
          <div className="info-card">
            <h2 className="info-title">How It Works</h2>

            <div className="info-step">
              <h3 className="step-title">1. Upload Your Resume</h3>
              <p className="step-text">
                Upload your resume in PDF or DOCX format. Maximum file size is 10MB.
              </p>
            </div>

            <div className="info-step">
              <h3 className="step-title">2. Add Job Descriptions (Optional)</h3>
              <p className="step-text">
                Paste one or multiple job descriptions to get role-specific insights.
              </p>
            </div>

            <div className="info-step">
              <h3 className="step-title">3. Get Instant Analysis</h3>
              <p className="step-text">
                Our AI analyzes your resume and provides:
              </p>

              <ul className="bullet-list">
                <li>Content and formatting improvements</li>
                <li>Key skills extracted from resume & JD</li>
                <li>ATS optimization suggestions</li>
                <li>Job description alignment score</li>
                <li>Missing keywords & improvement areas</li>
              </ul>
            </div>
          </div>

        </div>
      </section>

      {/* FEATURES */}
      <section className="hero-to-features-spacing">
        <Features />
      </section>

      {/* ANALYSIS OUTCOME (NEW SPACING WRAPPER) */}
      <section className="features-to-outcome-spacing">
        <AnalysisOutcome />
      </section>
      <Footer />
    </div>
  );
};

export default HomePage;
