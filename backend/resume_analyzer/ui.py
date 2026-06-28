import re
import streamlit as st

# Correct imports from our new modular structure
from .processing import extract_text_from_file, preprocess
from .extraction import load_skills, check_ats_compliance
from .analysis import analyze_resume_against_jd
from .llm import get_report_structured
from .reporting import generate_pdf_report

def _handle_form_submission(resume_file, job_descriptions, model, api_key):
    """Helper function to process form submission and run analysis."""
    if not resume_file or not any(jd.strip() for jd in job_descriptions):
        st.warning("⚠ Please upload a Resume and enter at least one Job Description.")
        return

    file_bytes = resume_file.read()
    file_ext = resume_file.name.split(".")[-1].lower() if "." in resume_file.name else ""

    try:
        raw_resume = extract_text_from_file(file_bytes, resume_file.name)
    except Exception as e:
        st.error(f"Failed to extract text from the uploaded file: {e}")
        return

    st.session_state.resume = preprocess(raw_resume)
    st.session_state.job_descriptions = [jd for jd in job_descriptions if jd.strip()]

    try:
        ats_compliance = check_ats_compliance(file_bytes, file_ext)
        all_skills = load_skills("skills.csv")
    except Exception as e:
        st.error(f"Failed to load necessary resources: {e}")
        return

    st.session_state.results = []
    with st.spinner("🔎 Analyzing resume against Job Descriptions..."):
        for jd in st.session_state.job_descriptions:
            try:
                res = analyze_resume_against_jd(
                    model, st.session_state.resume, jd, all_skills, api_key
                )
                res["ats_compliance"] = ats_compliance
                st.session_state.results.append(res)
            except Exception as e:
                st.error(f"Error analyzing JD: {e}")

    st.session_state['analysis_triggered'] = True
    st.session_state.page = "results"
    st.rerun()

def show_form(model, api_key):
    """Display the main form for uploading resume and JDs."""
    if 'jd_count' not in st.session_state:
        st.session_state.jd_count = 1

    st.markdown("### Step 1: Upload Resume")
    resume_file = st.file_uploader(
        "Upload your Resume/CV (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"]
    )

    st.markdown("### Step 2: Paste Job Descriptions")
    job_descriptions = []
    for i in range(st.session_state.jd_count):
        jd = st.text_area(f"Job Description {i+1}", key=f"jd_{i}")
        job_descriptions.append(jd)

    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        if st.button("Add JD"):
            st.session_state.jd_count += 1
            st.rerun()
    with col2:
        if st.session_state.jd_count > 1 and st.button("Remove JD"):
            st.session_state.jd_count -= 1
            st.rerun()

    if st.button("Analyze Resume", type="primary"):
        _handle_form_submission(resume_file, job_descriptions, model, api_key)

def show_results(api_key):
    """Display the analysis results in tabs."""
    st.subheader("📑 Per-JD Analysis Results")

    if not st.session_state.results:
        st.error("No JD analysis results available. Please try again.")
        return

    tabs = st.tabs([f"JD {i+1}" for i in range(len(st.session_state.results))])

    for idx, res in enumerate(st.session_state.results):
        with tabs[idx]:
            overall = res.get("overall_score", 0)
            requirements = res.get("requirements_score", 0)
            keywords = res.get("keywords_score", 0)

            st.subheader("📊 Resume Score")
            st.markdown(f"""
                <div class="score-row">
                    <div class="score-card overall"><div class="circle">{overall}%</div><div class="label">Overall Score</div></div>
                    <div class="score-card requirements"><div class="circle">{requirements}%</div><div class="label">Requirements Score</div></div>
                    <div class="score-card keywords"><div class="circle">{keywords}%</div><div class="label">Keywords Score</div></div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🛡 ATS Compliance Check"):
                compliance = res.get("ats_compliance", {})
                checks = {
                    "multi_column": "Multi-column Layout",
                    "non_standard_fonts": "Non-standard Fonts",
                    "images": "Images or Graphics",
                    "tables": "Tables"
                }
                for key, description in checks.items():
                    if compliance.get(key):
                        st.error(f"❌ [ISSUE] {description}: Detected")
                    else:
                        st.success(f"✅ [OK] {description}: Not Detected")

            st.subheader("📊 Keyword Gap Analysis (Skills)")
            jd_skills, matching, missing, extra = res.get('jd_skills', []), res.get('matching_skills', []), res.get('missing_skills', []), res.get('extra_skills', [])
            match_percent = int((len(matching) / len(jd_skills)) * 100) if jd_skills else 0
            st.write(f"**Skill Match: {match_percent}%**")
            st.progress(match_percent / 100)
            st.info(f"✅ Matching: {len(matching)} | ⚠ Missing: {len(missing)} | 💡 Extra: {len(extra)}")

            with st.expander("✅ Direct Matches"):
                exact_matches = res.get(
                    "exact_matches",
                    []
                )
                if exact_matches:
                    st.markdown(
                        " ".join(
                            [
                                f"<span class='matching-skill'>{s}</span>"
                                for s in exact_matches
                            ]
                        ),
                        unsafe_allow_html=True
                    )
                else:
                    st.write(
                        "No direct matches found."
                    )

            with st.expander("🔗 Related Matches"):
                related_matches = res.get(
                    "related_matches",
                    []
                )
                if related_matches:
                    for match in related_matches:
                        st.success(
                            f"{match['jd_skill']} "
                            f"(via {match['resume_skill']})"
                        )
                else:
                    st.write(
                        "No related matches found."
                    )

            with st.expander("🧠 Semantic Matches"):
                semantic_matches = res.get(
                    "semantic_matches",
                    []
                )
                if semantic_matches:
                    for match in semantic_matches:
                        st.info(
                            f"{match['jd_skill']} "
                            f"(via {match['resume_skill']}) "
                            f"[Score: {match['score']}]"
                        )
                else:
                    st.write(
                        "No semantic matches found."
                    )
                    
            with st.expander("⚠ Missing Skills"):
                if missing:
                    for s in missing:
                        st.markdown(f"<div class='missing-skill'>{s}</div>", unsafe_allow_html=True)
                        suggestions = res.get("learning_suggestions", {}).get(s)
                        if isinstance(suggestions, list) and suggestions:
                            for sug in suggestions:
                                title = sug.get("title", "Resource")
                                url = sug.get("url", "")
                                tag = "📘 Doc/Tutorial" if sug.get("type") == "doc" else "🎥 Video/Course"
                                clean_title = re.sub(r"^\s*\d+[\.\-)]\s*", "", title)
                                st.markdown(f"  - {tag}: [{clean_title}]({url})" if url else f"  - {tag}: {clean_title}")
                else:
                    st.write("Great job! You have all the skills listed in the job description.")

            with st.expander("💡 Extra Skills (Not in Job Description)"):
                if extra:
                    st.markdown(" ".join([f"<span class='extra-skill'>{s}</span>" for s in extra]), unsafe_allow_html=True)
                else:
                    st.write("No extra skills were found that were not in the job description.")
                    
            st.subheader("🤖 AI Feedback Report")
            ai_text = res.get("ai_raw")
            if not ai_text:
                st.warning("⚠️ AI Feedback not available for this JD (API error or quota limit).")
                if st.button(f"🔄 Retry AI Feedback for JD {idx+1}", key=f"retry_ai_{idx}"):
                    ai_report_retry = get_report_structured(st.session_state.resume, res.get("jd_text", ""), api_key)
                    if ai_report_retry:
                        res["ai_raw"] = ai_report_retry
                        st.session_state.results[idx] = res
                        st.success("✅ AI Feedback generated successfully!")
                        st.rerun()
            else:
                # Convert newlines to <br> tags for proper HTML rendering in the div
                html_formatted_text = ai_text.replace('\n', '<br>')
                st.markdown(f"<div class='ai-report'>{html_formatted_text}</div>", unsafe_allow_html=True)

                # Generate and display the single PDF download button
                pdf_bytes = generate_pdf_report(idx, res)
                st.download_button(
                    label="📄 Download Report as PDF",
                    data=pdf_bytes,
                    file_name=f"JD{idx+1}_resume_report.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_report_{idx}"
                )
