import React from "react";

const atsRules = {
  multi_column: {
    issue: {
      title: "Multiple columns detected",
      description: "ATS may skip content placed in columns."
    },
    ok: {
      title: "Single-column layout used",
      description: "Your resume structure is ATS-friendly."
    }
  },
  tables: {
    issue: {
      title: "Tables detected",
      description: "Tables can confuse ATS while reading content."
    },
    ok: {
      title: "No tables found",
      description: "Simple text layout improves ATS readability."
    }
  },
  images: {
    issue: {
      title: "Images or graphics detected",
      description: "ATS systems cannot read images."
    },
    ok: {
      title: "No images used",
      description: "Text-only content is easy for ATS to read."
    }
  },
  non_standard_fonts: {
    issue: {
      title: "Non-standard fonts detected",
      description: "Unusual fonts may reduce readability."
    },
    ok: {
      title: "Standard fonts used",
      description: "Your font choice is ATS-compatible."
    }
  }
};

const ATSCompliance = ({ ats_compliance }) => {
  return (
    <div className="ats-grid">
      {Object.entries(atsRules).map(([key, rule]) => {
        const hasIssue = ats_compliance?.[key];
        const content = hasIssue ? rule.issue : rule.ok;

        return (
          <div
            key={key}
            className={`ats-card ${hasIssue ? "ats-issue" : "ats-ok"}`}
          >
            <div className="ats-icon">
              {hasIssue ? "⚠️" : "✅"}
            </div>

            <div className="ats-text">
              <h4>{content.title}</h4>
              <p>{content.description}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ATSCompliance;
