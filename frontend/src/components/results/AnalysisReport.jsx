import React from "react";
import Expander from "./Expander";
import ScoreSection from "./ScoreSection";
import ATSCompliance from "./ATSCompliance";
import KeywordGapAnalysis from "./KeywordGapAnalysis";
import AIFeedback from "./AIFeedback";
import DownloadReport from "./DownloadReport";

const AnalysisReport = ({ result }) => {
  if (!result) return null;

  const {
  overall_score,
  requirements_score,
  keywords_score,
  ats_compliance,
  ai_raw,
} = result;

  return (
    <>
      <Expander title="📊 Resume Score" defaultOpen>
        <ScoreSection
          overall={overall_score}
          requirements={requirements_score}
          keywords={keywords_score}
        />
      </Expander>

      <Expander title="🛡 ATS Compliance">
        <ATSCompliance ats_compliance={ats_compliance} />
      </Expander>

      <Expander title="📌 Keyword Gap Analysis">
        <KeywordGapAnalysis
          matched_skills={result.matched_skills}
          missing_skills={result.missing_skills}
          additional_skills={result.additional_skills}
          learning_suggestions={result.learning_suggestions}
        />
      </Expander>

      <Expander title="🤖 AI Feedback Report">
        <AIFeedback ai_raw={ai_raw} />
      </Expander>

      {/* ⬇️ Download button directly after AI feedback */}
      <div className="download-inline">
        <DownloadReport analysisData={result} />
      </div>
    </>
  );
};

export default AnalysisReport;
