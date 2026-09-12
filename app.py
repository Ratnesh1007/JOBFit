import os
import tempfile
import streamlit as st

from src.pipeline import analyze_resume


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JOBFit - AI Resume & JD Matcher",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# MODERN DESIGN SYSTEM & CUSTOM CSS
# ============================================================

st.markdown("""
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
</head>

<style>
    /* Root Font & Aesthetics */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Layout Spacing */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
        max-width: 1300px !important;
    }

    /* Brand Header Banner */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    .brand-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .brand-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 0.2rem;
    }

    .brand-badge {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #60A5FA;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Enterprise KPI Card Grid */
    .kpi-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
    }

    .kpi-blue::before { background: linear-gradient(90deg, #3B82F6, #60A5FA); }
    .kpi-emerald::before { background: linear-gradient(90deg, #10B981, #34D399); }
    .kpi-amber::before { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .kpi-purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }

    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }

    .kpi-subtext {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 0.3rem;
    }

    /* Keyword Pills */
    .pill-matched {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px 4px;
    }

    .pill-missing {
        background: rgba(244, 63, 94, 0.12);
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #FB7185;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px 4px;
    }

    /* Requirement Badges */
    .status-fulfilled {
        color: #34D399;
        font-weight: 700;
    }
    .status-partial {
        color: #FBBF24;
        font-weight: 700;
    }
    .status-missing {
        color: #F87171;
        font-weight: 700;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94A3B8;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(30, 41, 59, 0.7) !important;
        color: #38BDF8 !important;
        border-bottom: 2px solid #38BDF8 !important;
    }

    /* Primary Button Styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.01em !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SAMPLE JD TEMPLATE
# ============================================================

SAMPLE_JD = """We are looking for a Senior AI / Python Engineer to design, build, and deploy scalable machine learning applications and RESTful APIs.

Required Qualifications (Mandatory):
- 3+ years of professional experience developing software using Python
- Strong experience with web frameworks such as FastAPI or Flask
- Hands-on experience with SQL databases like PostgreSQL or MySQL
- Proficient with Docker containerization and Git version control
- Bachelor's degree in Computer Science, Software Engineering, or a related field
- Strong problem-solving and communication skills

Preferred Qualifications (Nice to Have):
- Experience with Machine Learning frameworks like PyTorch or TensorFlow
- Knowledge of Generative AI, Large Language Models (LLMs), LangChain, and RAG architectures
- Familiarity with Vector Databases such as FAISS, Pinecone, or ChromaDB
- Hands-on experience deploying applications on AWS or GCP
- Experience with Kubernetes and CI/CD pipelines"""


# ============================================================
# BRAND HEADER BANNER
# ============================================================

st.markdown("""
<div class="brand-container">
    <div>
        <div class="brand-title">📄 JOBFit Intelligence</div>
        <div class="brand-subtitle">Enterprise Resume Screening & Job Compatibility Matching Platform</div>
    </div>
    <div class="brand-badge">
        <span>⚡ Real-Time Engine Active</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")
    
    analysis_mode = st.radio(
        "Processing Speed & Reasoning Mode:",
        options=["⚡ Lightning Mode (1–2 sec)", "🤖 Deep AI Mode (3–5 sec)"],
        index=0,
        help="Lightning Mode uses fast vector search and section heuristics. Deep AI Mode uses Llama 3.2 3B for single-pass reasoning."
    )
    
    mode_key = "fast" if "Lightning" in analysis_mode else "deep"
    
    st.divider()

    st.markdown("### 🛡️ Section Evidence Rules")
    st.info(
        "**Strict Verification Active**\n\n"
        "• Certifications & Skills lists are **never** counted as Work Experience.\n"
        "• FULFILLED status requires verified bullet points from Work Experience or Projects sections."
    )
    
    st.divider()
    st.caption("🚀 Version 2.4 | FAISS Vector Store + FastEmbed")


# ============================================================
# INPUT SECTION
# ============================================================

col_input1, col_input2 = st.columns([1, 1], gap="large")

with col_input1:
    st.markdown("### 1️⃣ Resume Upload")
    uploaded_resume = st.file_uploader(
        "Upload Candidate Resume (PDF format)",
        type=["pdf"],
        help="Upload candidate resume in PDF format."
    )

with col_input2:
    st.markdown("### 2️⃣ Target Job Description")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("✨ Load Sample JD Template", use_container_width=True):
            st.session_state["jd_input"] = SAMPLE_JD
    with col_btn2:
        if st.button("🗑️ Clear JD Text", use_container_width=True):
            st.session_state["jd_input"] = ""
        
    jd_default = st.session_state.get("jd_input", "")
    
    jd_text = st.text_area(
        "Paste the job description below",
        value=jd_default,
        height=220,
        placeholder="Paste target job description here..."
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

analyze_button = st.button(
    f"🚀 Run JOBFit Evaluation ({'⚡ Lightning Engine' if mode_key == 'fast' else '🤖 Deep AI Engine'})",
    type="primary",
    use_container_width=True
)


# ============================================================
# HELPER: GENERATE MARKDOWN REPORT
# ============================================================

def generate_markdown_report(results):
    score = results["jd_match_score"]
    rq = results["resume_quality"]
    
    report = []
    report.append(f"# JOBFit Enterprise Evaluation Report\n")
    report.append(f"**Overall JD Match Score:** {score}/100\n")
    report.append(f"- **Requirement Match Score:** {results['requirement_match_score']:.2f}%")
    report.append(f"- **Keyword Match Score:** {results['keyword_match_score']:.2f}%")
    report.append(f"- **Resume Quality Score:** {rq['quality_score']}/100\n")
    
    report.append("## Requirement Summary")
    report.append(f"- ✅ Fulfilled: {results['fulfilled']}")
    report.append(f"- ⚠️ Partially Fulfilled: {results['partially_fulfilled']}")
    report.append(f"- ❌ Not Fulfilled: {results['not_fulfilled']}\n")
    
    report.append("## Keyword Analysis")
    report.append(f"**Matched Keywords ({len(results['matched_keywords'])}):** " + ", ".join(results["matched_keywords"]))
    report.append(f"**Missing Keywords ({len(results['missing_keywords'])}):** " + ", ".join(results["missing_keywords"]) + "\n")
    
    report.append("## Detailed Requirement Breakdown")
    for res in results["analysis_results"]:
        report.append(f"### Requirement: {res['requirement']}")
        report.append(f"- **Category:** {res['category']} | **Importance:** {res['importance']} | **Status:** {res['status']}")
        report.append(f"- **Confidence:** {res.get('confidence', 0)}")
        report.append(f"- **Reason:** {res.get('reason', '')}")
        if res.get("evidence"):
            report.append(f"- **Evidence:** {res['evidence']}")
        report.append("")
        
    report.append("## Resume Quality Audit")
    report.append(f"- **Word Count:** {rq['length']['word_count']} ({rq['length']['rating']})")
    report.append(f"- **Action Verbs:** {rq['achievements']['action_words']}")
    report.append(f"- **Quantified Metrics:** {rq['achievements']['metrics']}")
    
    contact_list = [k.capitalize() for k, v in rq['contact_info'].items() if v]
    report.append(f"- **Contact Info Included:** {', '.join(contact_list) if contact_list else 'None'}")
    
    sections_list = [k for k, v in rq['sections'].items() if v]
    report.append(f"- **Sections Found:** {', '.join(sections_list) if sections_list else 'None'}")
    
    return "\n".join(report)


# ============================================================
# ANALYSIS EXECUTION
# ============================================================

if analyze_button:

    if uploaded_resume is None:
        st.error("❌ Please upload a candidate resume PDF.")
        st.stop()

    if not jd_text.strip():
        st.error("❌ Please enter or load a job description.")
        st.stop()

    temp_resume = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    temp_resume.write(uploaded_resume.getbuffer())
    temp_resume.close()
    resume_path = temp_resume.name

    try:
        with st.status("🚀 JOBFit Engine Processing...", expanded=True) as status:
            
            def on_status_change(message):
                status.write(message)
                
            results = analyze_resume(
                resume_path,
                jd_text,
                mode=mode_key,
                status_callback=on_status_change
            )
            
            status.update(
                label="✅ Analysis Complete!",
                state="complete",
                expanded=False
            )

        st.divider()

        score = results["jd_match_score"]
        rq = results["resume_quality"]

        # ====================================================
        # EXECUTIVE KPI DASHBOARD
        # ====================================================
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.markdown(f"""
            <div class="kpi-card kpi-blue">
                <div class="kpi-label">Overall Match Score</div>
                <div class="kpi-value">{score}<span style="font-size:1.2rem;color:#94A3B8;">/100</span></div>
                <div class="kpi-subtext">Composite ATS Rating</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi2:
            st.markdown(f"""
            <div class="kpi-card kpi-emerald">
                <div class="kpi-label">Requirement Match</div>
                <div class="kpi-value">{results['requirement_match_score']:.1f}<span style="font-size:1.2rem;color:#94A3B8;">%</span></div>
                <div class="kpi-subtext">Mandatory & Preferred Criteria</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown(f"""
            <div class="kpi-card kpi-amber">
                <div class="kpi-label">Keyword Alignment</div>
                <div class="kpi-value">{results['keyword_match_score']:.1f}<span style="font-size:1.2rem;color:#94A3B8;">%</span></div>
                <div class="kpi-subtext">Technical Skill Coverage</div>
            </div>
            """, unsafe_allow_html=True)

        with kpi4:
            st.markdown(f"""
            <div class="kpi-card kpi-purple">
                <div class="kpi-label">Resume Quality</div>
                <div class="kpi-value">{rq['quality_score']}<span style="font-size:1.2rem;color:#94A3B8;">/100</span></div>
                <div class="kpi-subtext">Formatting & Structure Rating</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.progress(min(max(float(score) / 100, 0.0), 1.0))

        if score >= 80:
            st.success("🟢 **Strong Fit Candidate:** Resume demonstrates high alignment with core mandatory requirements and technical skills.")
        elif score >= 65:
            st.info("🔵 **Good Match:** Meets major qualifications, but has targeted skill gaps in preferred areas.")
        elif score >= 50:
            st.warning("🟡 **Moderate Fit:** Meets some qualifications, but lacks several mandatory technical skills or experience depth.")
        else:
            st.error("🔴 **Low Compatibility:** Significant gaps detected across mandatory experience and technical keywords.")

        st.write("")

        # ====================================================
        # TABBED DASHBOARD RESULTS
        # ====================================================
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Executive Summary",
            "🔍 Requirement Evaluation",
            "🔑 Keyword Matrix",
            "📑 Structural Audit",
            "💡 Action Roadmap"
        ])

        # ----------------------------------------------------
        # TAB 1: EXECUTIVE SUMMARY
        # ----------------------------------------------------
        with tab1:
            st.markdown("### 📋 Executive Summary & Breakdown")

            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.markdown(f"""
                <div style="background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3); border-radius:10px; padding:1rem; text-align:center;">
                    <div style="color:#34D399; font-size:0.9rem; font-weight:600;">FULFILLED CRITERIA</div>
                    <div style="color:#F8FAFC; font-size:2rem; font-weight:800;">{results['fulfilled']}</div>
                </div>
                """, unsafe_allow_html=True)

            with r_col2:
                st.markdown(f"""
                <div style="background:rgba(245, 158, 11, 0.1); border:1px solid rgba(245, 158, 11, 0.3); border-radius:10px; padding:1rem; text-align:center;">
                    <div style="color:#FBBF24; font-size:0.9rem; font-weight:600;">PARTIALLY FULFILLED</div>
                    <div style="color:#F8FAFC; font-size:2rem; font-weight:800;">{results['partially_fulfilled']}</div>
                </div>
                """, unsafe_allow_html=True)

            with r_col3:
                st.markdown(f"""
                <div style="background:rgba(244, 63, 94, 0.1); border:1px solid rgba(244, 63, 94, 0.3); border-radius:10px; padding:1rem; text-align:center;">
                    <div style="color:#FB7185; font-size:0.9rem; font-weight:600;">UNFULFILLED CRITERIA</div>
                    <div style="color:#F8FAFC; font-size:2rem; font-weight:800;">{results['not_fulfilled']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.markdown("### 📥 Export Evaluation Report")
            report_text = generate_markdown_report(results)
            st.download_button(
                label="📥 Download Full Evaluation Report (.md)",
                data=report_text,
                file_name="jobfit_evaluation_report.md",
                mime="text/markdown"
            )

        # ----------------------------------------------------
        # TAB 2: REQUIREMENT EVALUATION
        # ----------------------------------------------------
        with tab2:
            st.markdown("### 🔍 Verified Requirement Matrix")
            st.caption("Section-aware semantic evaluation matching each JD requirement against resume evidence.")

            for result in results["analysis_results"]:
                status_val = result["status"]
                importance = result["importance"]

                if status_val == "FULFILLED":
                    status_badge = '<span class="status-fulfilled">✅ FULFILLED</span>'
                elif status_val == "PARTIALLY_FULFILLED":
                    status_badge = '<span class="status-partial">⚠️ PARTIALLY FULFILLED</span>'
                else:
                    status_badge = '<span class="status-missing">❌ NOT FULFILLED</span>'

                if importance == "MANDATORY":
                    imp_badge = '<span class="badge-mandatory">🔴 MANDATORY</span>'
                elif importance == "PREFERRED":
                    imp_badge = '<span class="badge-preferred">🟡 PREFERRED</span>'
                else:
                    imp_badge = '<span style="color:#94A3B8;font-weight:600;">⚪ GENERAL</span>'

                expander_title = f"{'✅' if status_val == 'FULFILLED' else ('⚠️' if status_val == 'PARTIALLY_FULFILLED' else '❌')} [{importance}] {result['requirement']}"

                with st.expander(expander_title):
                    col_a, col_b = st.columns(2)

                    with col_a:
                        st.markdown(f"**Category:** {result['category']}")
                        st.markdown(f"**Requirement Priority:** {imp_badge}", unsafe_allow_html=True)

                    with col_b:
                        st.markdown(f"**Evaluation Status:** {status_badge}", unsafe_allow_html=True)
                        st.markdown(f"**Confidence Rating:** `{result.get('confidence', 0.0)*100:.0f}%`")

                    st.markdown("**📝 Verification Details:**")
                    st.write(result.get("reason", "No explanation available."))

                    st.markdown("**📄 Verified Resume Evidence:**")
                    evidence = result.get("evidence", "")
                    if evidence:
                        st.info(evidence)
                    else:
                        st.warning("No direct supporting work experience or project evidence found.")

        # ----------------------------------------------------
        # TAB 3: KEYWORD MATRIX
        # ----------------------------------------------------
        with tab3:
            st.markdown("### 🔑 Technical Keywords Matrix")
            st.caption("Comparison between target keywords extracted from Job Description vs Candidate Resume.")

            k_col1, k_col2 = st.columns(2, gap="medium")

            with k_col1:
                st.markdown(f"#### ✅ Matched Keywords ({len(results['matched_keywords'])})")
                if results['matched_keywords']:
                    pills_html = "".join([f'<span class="pill-matched">✓ {kw}</span>' for kw in results['matched_keywords']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                else:
                    st.write("No matching technical keywords found.")

            with k_col2:
                st.markdown(f"#### ❌ Missing Keywords ({len(results['missing_keywords'])})")
                if results['missing_keywords']:
                    pills_html = "".join([f'<span class="pill-missing">✗ {kw}</span>' for kw in results['missing_keywords']])
                    st.markdown(pills_html, unsafe_allow_html=True)
                else:
                    st.success("No major missing technical keywords detected!")

        # ----------------------------------------------------
        # TAB 4: RESUME STRUCTURAL AUDIT
        # ----------------------------------------------------
        with tab4:
            st.markdown("### 📑 Resume Structural & Impact Audit")

            q_col1, q_col2 = st.columns(2, gap="large")

            with q_col1:
                st.markdown("#### 📬 Contact & Links Audit")
                c_info = rq["contact_info"]
                st.write(f"{'✅' if c_info['email'] else '❌'} **Email Address:** {'Detected' if c_info['email'] else 'Missing'}")
                st.write(f"{'✅' if c_info['phone'] else '❌'} **Phone Number:** {'Detected' if c_info['phone'] else 'Missing'}")
                st.write(f"{'✅' if c_info['linkedin'] else '❌'} **LinkedIn URL:** {'Detected' if c_info['linkedin'] else 'Missing'}")
                st.write(f"{'✅' if c_info['github'] else '❌'} **GitHub Repository Link:** {'Detected' if c_info['github'] else 'Missing'}")

                st.markdown("#### 📏 Resume Word Density")
                len_info = rq["length"]
                st.write(f"**Word Count:** {len_info['word_count']} words")
                st.write(f"**Length Rating:** {len_info['rating']}")

            with q_col2:
                st.markdown("#### 📂 Section Completeness")
                sec_info = rq["sections"]
                for sec_name, present in sec_info.items():
                    st.write(f"{'✅' if present else '⚠️'} **{sec_name}:** {'Verified' if present else 'Missing'}")

                st.markdown("#### ⚡ Achievement Impact Metrics")
                ach_info = rq["achievements"]
                st.write(f"**Strong Action Verbs Found:** {ach_info['action_words']}")
                st.write(f"**Quantified Accomplishment Metrics:** {ach_info['metrics']}")

        # ----------------------------------------------------
        # TAB 5: ACTION ROADMAP
        # ----------------------------------------------------
        with tab5:
            st.markdown("### 💡 Prioritized Improvement Roadmap")
            st.write("Follow these prioritized action points to improve candidate ATS passing rates:")

            unfulfilled_mandatory = [
                r for r in results["analysis_results"]
                if r["importance"] == "MANDATORY" and r["status"] == "NOT_FULFILLED"
            ]

            if unfulfilled_mandatory:
                st.markdown("#### 🚨 Priority 1: Address Mandatory Skill Gaps")
                for idx, item in enumerate(unfulfilled_mandatory, 1):
                    st.error(
                        f"**{idx}. Missing Mandatory Requirement:** \"{item['requirement']}\"\n\n"
                        f"*Recommendation:* Incorporate project experience or work bullet points demonstrating this skill."
                    )

            if results["missing_keywords"]:
                st.markdown("#### 🔑 Priority 2: Integrate Missing Technical Keywords")
                missing_str = ", ".join([f"`{kw}`" for kw in results["missing_keywords"][:12]])
                st.warning(f"Incorporate these missing technical keywords: {missing_str}")

            st.markdown("#### 🛠️ Priority 3: Formatting & Impact Enhancements")
            c_info = rq["contact_info"]
            if not c_info["linkedin"]:
                st.info("💡 Include a professional LinkedIn profile link.")
            if not c_info["github"]:
                st.info("💡 Include a GitHub profile link to showcase code repositories.")
            if rq["achievements"]["action_words"] < 5:
                st.info("💡 Strengthen bullet points with action verbs (*Engineered*, *Architected*, *Optimized*, *Implemented*).")
            if not rq["achievements"]["has_metrics"]:
                st.info("💡 Quantify accomplishments with numbers and percentages (e.g., *Reduced latency by 35%*).")

            st.success("🎉 Implementation of the recommendations above will significantly increase candidate ATS match scores!")

    except Exception as error:
        st.error("❌ An error occurred while evaluating the resume.")
        st.exception(error)

    finally:
        if os.path.exists(resume_path):
            os.remove(resume_path)