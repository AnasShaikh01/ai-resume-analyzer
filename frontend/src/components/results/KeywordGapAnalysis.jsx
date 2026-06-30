import React, { useState } from "react";

/* Skill chip */
const SkillChip = ({ skill, type }) => (
  <span className={`skill-chip ${type}`}>{skill}</span>
);

/* Missing skill card */
const MissingSkillCard = ({ skill, learningSuggestions }) => {
  const [open, setOpen] = useState(false);

  // 🔐 SAFE lookup (handles case mismatch + undefined)
  const resources =
    learningSuggestions?.[skill] ||
    learningSuggestions?.[skill.toLowerCase()] ||
    [];

  return (
    <div className="missing-skill-card">
      <div className="missing-skill-header">
        <span className="missing-skill-name">{skill}</span>

        <button
          type="button"
          className="learn-toggle"
          onClick={() => setOpen(!open)}
        >
          {open ? "Hide learning sources" : "View learning sources"}
        </button>
      </div>

      {open && (
        <ul className="learning-list">
          {resources.length > 0 ? (
            resources.map((res, idx) => <li key={idx}>{res}</li>)
          ) : (
            <li>No learning resources available for this skill yet.</li>
          )}
        </ul>
      )}
    </div>
  );
};

/* Main component */
const KeywordGapAnalysis = ({
  matched_skills = [],
  missing_skills = [],
  additional_skills = [],
  learning_suggestions = {}
}) => {
  return (
    <div className="keyword-gap">

      {/* 🔴 Missing Skills */}
      <section className="kg-section">
        <h3>Skills You Should Add</h3>
        <p className="kg-hint">
          These skills are required in the job description but missing from your resume.
        </p>

        {missing_skills.length === 0 ? (
          <div className="success-box">
            Great! Your resume already covers all required skills.
          </div>
        ) : (
          <div className="missing-grid">
            {missing_skills.map((skill) => (
              <MissingSkillCard
                key={skill}
                skill={skill}
                learningSuggestions={learning_suggestions}
              />
            ))}
          </div>
        )}
      </section>

      {/* <section className="kg-section">
        <h3>✅ Direct Matches</h3>

        <div className="skill-chip-group">
          {exact_matches.length > 0 ? (
            exact_matches.map((skill) => {

            const location = matched_skill_locations?.[skill];

            return (
              <div
                key={skill}
                className="match-card"
              >
                <SkillChip
                  skill={skill}
                  type="match"
                />

                {location && (
                  <p className="skill-location">
                    📍 {location.sections.join(" • ")}
                  </p>
                )}
              </div>
            );
          })
          ) : (
            <p className="empty-text">
              No direct matches found.
            </p>
          )}
        </div>
      </section>

      <section className="kg-section">
        <h3>🔗 Related Matches</h3>

        {related_matches.length > 0 ? (
          related_matches.map((match, idx) => (
            <div
              key={idx}
              className="related-match-card"
            >
              <strong>
                {match.jd_skill}
              </strong>

              {" "}via{" "}

              <strong>{match.resume_skill}</strong>

              <p className="skill-location">
                📍 {
                  matched_skill_locations?.[
                    match.resume_skill
                  ]?.sections.join(" • ")
                }
              </p>
            </div>
          ))
        ) : (
          <p className="empty-text">
            No related matches found.
          </p>
        )}
      </section>

      <section className="kg-section">
        <h3>🧠 Semantic Matches</h3>

        {semantic_matches.length > 0 ? (
          semantic_matches.map((match, idx) => (
            <div
              key={idx}
              className="semantic-match-card"
            >
              <strong>
                {match.jd_skill}
              </strong>

              {" "}via{" "}

              <strong>
                {match.resume_skill}
              </strong>

              {" "}({match.score})
            </div>
          ))
        ) : (
          <p className="empty-text">
            No semantic matches found.
          </p>
        )}
      </section> */}

      <section className="kg-section">
        <h3>Matching Skills</h3>

        <div className="skill-chip-group">
          {matched_skills.length > 0 ? (
            matched_skills.map((skill) => (
              <SkillChip
                key={skill}
                skill={skill}
                type="match"
              />
            ))
          ) : (
            <p className="empty-text">
              No matching skills found.
            </p>
          )}
        </div>
      </section>

      {/* ℹ️ Additional Skills (LIMITED) */}
      <section className="kg-section">
        <h3>Additional Skills</h3>
        <p className="kg-hint">
          These skills are present in your resume but not required for this job.
        </p>

        <div className="skill-chip-group">
          {additional_skills.slice(0, 8).length > 0 ? (
            additional_skills.slice(0, 8).map((skill) => (
              <SkillChip key={skill} skill={skill} type="extra" />
            ))
          ) : (
            <p className="empty-text">No additional skills detected.</p>
          )}
        </div>
      </section>

    </div>
  );
};

export default KeywordGapAnalysis;
