import React, { useState } from "react";
import { analyzeResume } from "../services/api";
import { useNavigate } from "react-router-dom";
import { FiUpload } from "react-icons/fi";
import AnalysisModal from "./AnalysisModal";
import "./AnalysisForm.css";

const AnalysisForm = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescriptions, setJobDescriptions] = useState([
    { id: 1, text: "" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const addJD = () => {
    setJobDescriptions([...jobDescriptions, { id: Date.now(), text: "" }]);
  };

  const removeJD = (id) => {
    if (jobDescriptions.length === 1) return;
    setJobDescriptions(jobDescriptions.filter(jd => jd.id !== id));
  };

  const handleCancelAnalysis = () => {
    setIsLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!resumeFile) {
      setError("Please upload your resume.");
      return;
    }

    const validJDs = jobDescriptions
      .map(jd => jd.text.trim())
      .filter(Boolean);

    if (validJDs.length === 0) {
      setError("Please add at least one job description.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await analyzeResume(resumeFile, validJDs);
      navigate("/results", {
      state: {
        analysisData: response.results   // ARRAY of JD results
      }
    });
    } catch (err) {
      console.error(err);
      setError("Backend error — please try again later.");
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* 🔄 Analysis Modal */}
      {isLoading && <AnalysisModal onCancel={handleCancelAnalysis} />}

      <form className="analysis-form" onSubmit={handleSubmit}>
        <h2 className="form-heading">Upload Your Resume</h2>

        {/* UPLOAD BOX */}
        <div className="file-upload-box">
          {!resumeFile ? (
            <>
              <FiUpload className="upload-icon" />
              <p className="upload-label">Click to upload or drag & drop</p>
              <span className="upload-hint">PDF / DOCX / TXT</span>
            </>
          ) : (
            <div className="uploaded-file">
              <span className="file-icon">📄</span>
              <span className="file-name">{resumeFile.name}</span>

              <button
                type="button"
                className="remove-file-btn"
                onClick={() => setResumeFile(null)}
                title="Remove file"
              >
                ×
              </button>
            </div>
          )}

          <input
            type="file"
            className="file-input"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setResumeFile(e.target.files[0])}
          />
        </div>

        {/* Job Descriptions */}
        <div className="jd-section">
          {jobDescriptions.map((jd, idx) => (
            <div className="jd-card" key={jd.id}>
              <div className="jd-header">
                <span className="jd-title">
                  {idx === 0
                    ? "Job Description (Required)"
                    : `Job Description ${idx + 1} (Optional)`}
                </span>

                {idx !== 0 && (
                  <button
                    type="button"
                    className="remove-jd-text"
                    onClick={() => removeJD(jd.id)}
                  >
                    Remove
                  </button>
                )}
              </div>

              <textarea
                className="jd-textarea"
                placeholder="Paste the job description here..."
                value={jd.text}
                onChange={(e) =>
                  setJobDescriptions(
                    jobDescriptions.map(x =>
                      x.id === jd.id ? { ...x, text: e.target.value } : x
                    )
                  )
                }
              />
            </div>
          ))}

          <button
            type="button"
            className="add-jd-btn"
            onClick={addJD}
          >
            + Add another job description
          </button>
        </div>

        {/* Submit */}
        <button
          type="submit"
          className="analyze-btn"
          disabled={isLoading}
        >
          Analyze Resume
        </button>

        {error && <p className="error">{error}</p>}
      </form>
    </>
  );
};

export default AnalysisForm;
