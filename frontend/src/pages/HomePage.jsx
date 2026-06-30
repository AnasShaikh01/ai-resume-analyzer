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

      {/* ================= HERO ================= */}
      <section className="hero-section">

        <div className="hero-pattern"></div>
        <div className="hero-glow hero-glow-left"></div>
        <div className="hero-glow hero-glow-right"></div>

        <div className="hero-container">

          <div className="hero-header">

            <div className="hero-badge">
              AI Resume Analyzer
            </div>

            <h1 className="hero-title">
              Build a Resume That Gets
              <span> More Interviews</span>
            </h1>

            <p className="hero-subtitle">
              Instantly analyze your resume using AI, compare it against
              multiple job descriptions, improve ATS compatibility,
              identify missing skills, and receive actionable recommendations
              to maximize your chances of getting shortlisted.
            </p>

          </div>

          <div className="form-info-row">

            {/* LEFT */}

            <div className="upload-card">

              <div className="panel-header">

                <div>
                  <h2>Resume Analysis</h2>
                  <p>
                    Upload your resume and start your AI-powered analysis.
                  </p>
                </div>

                <div className="panel-status">
                  Ready
                </div>

              </div>

              <AnalysisForm />

            </div>

            {/* RIGHT */}

            <div className="info-card">

              <div className="steps-header">

                <h2>How It Works</h2>

                <p>
                  Three simple steps to optimize your resume.
                </p>

              </div>

              <div className="steps">

                <div className="step">

                  <div className="step-number">
                    01
                  </div>

                  <div className="step-content">

                    <h3>Upload Resume</h3>

                    <p>
                      Upload your resume in PDF or DOCX format.
                      Our parser extracts every important detail.
                    </p>

                  </div>

                </div>

                <div className="step">

                  <div className="step-number">
                    02
                  </div>

                  <div className="step-content">

                    <h3>Add Job Description</h3>

                    <p>
                      Compare against one or multiple job descriptions
                      for targeted ATS optimization.
                    </p>

                  </div>

                </div>

                <div className="step">

                  <div className="step-number">
                    03
                  </div>

                  <div className="step-content">

                    <h3>Get AI Insights</h3>

                    <p>
                      Receive ATS score, missing skills,
                      keyword analysis and improvement suggestions.
                    </p>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </section>

      {/* ================= FEATURES ================= */}

      <section className="section">

        <div className="container">

          <Features />

        </div>

      </section>

      {/* ================= ANALYSIS OUTCOME ================= */}

      <section className="section outcome-section">

        <div className="container">

          <AnalysisOutcome />

        </div>

      </section>

      <Footer />

    </div>
  );
};

export default HomePage;