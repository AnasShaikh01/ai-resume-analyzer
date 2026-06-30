import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">

      <div className="footer-divider"></div>

      <div className="footer-content">

        <div className="footer-brand">
          <h3>AI Resume Analyzer</h3>
          <p>AI-powered resume optimization & ATS analysis.</p>
        </div>

        <div className="footer-bottom">
          <p>
            © 2025 AI Resume Analyzer. All rights reserved.
          </p>

          <span>
            Crafted by <strong>Anas Shaikh</strong>
          </span>
        </div>

      </div>

    </footer>
  );
};

export default Footer;