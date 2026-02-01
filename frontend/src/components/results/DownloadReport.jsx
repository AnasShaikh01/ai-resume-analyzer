import React, { useState } from "react";
import { FiDownload } from "react-icons/fi";

const DownloadReport = ({ analysisData }) => {
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    try {
      setLoading(true);

      const response = await fetch("http://localhost:8000/download-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          result: analysisData,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to download report");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "AI_Resume_Analysis_Report.pdf";
      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Unable to download report. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      className="download-btn"
      onClick={handleDownload}
      disabled={loading}
    >
      <FiDownload size={18} />
      {loading ? "Preparing PDF..." : "Download PDF"}
    </button>
  );
};

export default DownloadReport;
