# 📄 JOBFit Intelligence

> **AI-Powered Resume Screening & Job Description Compatibility Matcher**

JOBFit Intelligence is an enterprise-grade AI resume evaluation platform that analyzes candidate resumes against target job descriptions. It calculates ATS-style compatibility scores, performs section-aware semantic evidence verification, extracts technical keywords, and audits structural resume quality to help candidates optimize their resumes for target roles.

---

## 🔄 End-to-End Pipeline & Architecture

JOBFit executes a 10-stage processing pipeline to deliver instant, section-verified resume evaluation:

```
[1. PDF Resume Upload] ──> [2. Text Extraction & Cleaning] ──> [3. Structural Quality Audit]
                                                                        │
[4. Section-Aware Chunking] <───────────────────────────────────────────┘
        │
        ├──> [5. Technical Keyword Extraction & Alias Normalization]
        │
        └──> [6. Dense Embeddings (bge-small-en-v1.5)]
                    │
                    v
            [7. FAISS Vector Store Indexing (IndexFlatIP)]
                    │
                    ├──> [8. JD Requirement Extraction & Classification]
                    │
                    v
            [9. Section-Re-Ranked Evidence Matching]
                    │
                    v
            [10. Evidence Verification Engine (Deep AI / Fast Mode)]
                    │
                    v
            [11. Composite ATS Scoring & Action Roadmap] ──> [Streamlit UI Dashboard]
```

### ⚙️ How It Works (Step-by-Step):

1. **PDF Ingestion & Text Extraction (`pdf_parser.py`, `text_cleaner.py`)**:
   - Uses PyMuPDF (`pymupdf`) to extract raw text across all PDF pages.
   - Cleans formatting, normalizes whitespace, and strips redundant artifacts.

2. **Resume Quality & Formatting Audit (`resume_quality.py`)**:
   - Audits contact info (Email, Phone, LinkedIn, GitHub).
   - Verifies completeness of mandatory sections (Summary, Experience, Education, Skills, Projects, Certifications).
   - Scans for strong action verbs (*Engineered, Architected, Optimized*) and quantified metrics (*e.g., $50k, 35%, 10x*).

3. **Section-Aware Semantic Chunking (`chunker.py`)**:
   - Detects section headings and tags text chunks with parent context (`[Section: WORK EXPERIENCE]`, `[Section: PROJECTS]`, `[Section: CERTIFICATIONS]`, `[Section: SKILLS]`).

4. **Technical Keyword Matrix (`keyword_extractor.py`)**:
   - Instantly matches text against 100+ technical terms using regex boundary rules and alias normalization (`ML` ➔ `Machine Learning`, `K8s` ➔ `Kubernetes`, `RAG` ➔ `Retrieval Augmented Generation`, `Postgres` ➔ `PostgreSQL`).

5. **Dense Embedding & Vector Indexing (`embeddings.py`, `vector_store.py`)**:
   - Generates 384-dimensional dense embeddings using `BAAI/bge-small-en-v1.5` via `fastembed`.
   - Builds an in-memory FAISS `IndexFlatIP` using L2-normalized vectors for cosine similarity retrieval.

6. **JD Requirement Parsing & Classification (`jd_parser.py`, `requirement_classifier.py`)**:
   - Parses the Job Description into bullet points and requirements.
   - Classifies categories (`Technical Skill`, `Experience`, `Education`, `Certification`, `Soft Skill`) and priorities (`MANDATORY`, `PREFERRED`, `GENERAL`).

7. **Section Context Re-Ranking (`matcher.py`)**:
   - Retrieves top vector matches from FAISS.
   - For Experience requirements, re-ranks and prioritizes chunks originating from `WORK EXPERIENCE` and `PROJECTS` sections over `CERTIFICATIONS` or `SKILLS` lists.

8. **Strict Evidence Verification Engine (`llm_analyzer.py`)**:
   - **Lightning Mode**: Evaluates fulfillment in < 50ms using section rules and semantic vector thresholds.
   - **Deep AI Mode**: Single-pass reasoning via local Llama 3.2 3B.
   - *Strict Rule*: Skills or certificates listed without work experience bullet points are marked as `PARTIALLY_FULFILLED` (never `FULFILLED`).

9. **Composite ATS Scoring Engine (`ats_scorer.py`)**:
   - Calculates a weighted composite score blending Requirement Fulfillment Score (70%) and Keyword Match Coverage (30%), incorporating category and importance multipliers.

10. **Interactive Enterprise Dashboard (`app.py`)**:
    - Renders an interactive Streamlit dashboard featuring an Executive Summary, Requirement Matrix, Technical Keyword Pills, Structural Audit, Action Roadmap, and Markdown Report Export.

---

## ✨ Key Features

- ⚡ **Dual Processing Engine Mode**:
  - **Lightning Mode (1–2 sec)**: Fast vector matching & section heuristics.
  - **Deep AI Mode (3–5 sec)**: Llama 3.2 3B single-pass reasoning.
- 🛡️ **Solid Evidence Verification**:
  - Certificates or skill lists alone are **never** counted as Work Experience.
- 🔑 **100+ Technical Keyword Matrix**:
  - Automatic tech keyword matching and alias normalization.
- 📑 **Resume Quality & Structural Audit**:
  - Evaluates contact details, section completeness, action verbs, and metrics.
- 💡 **Actionable Improvement Roadmap**:
  - Prioritized recommendations to increase candidate ATS match scores.
- 📥 **Export Report**:
  - Download full candidate evaluation summaries in Markdown format.

---

## 🛠️ Tech Stack

- **UI & Dashboard**: Streamlit (with custom CSS design system)
- **PDF Parsing**: PyMuPDF (`pymupdf`)
- **Embeddings**: BAAI/bge-small-en-v1.5 (`fastembed`)
- **Vector Database**: FAISS (`IndexFlatIP`)
- **LLM Reasoning**: Llama 3.2 3B (`ollama`) / Fast Heuristics Engine
- **Containerization**: Docker, Railway, Render, Streamlit Cloud

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/Ratnesh1007/JOBFit.git
cd JOBFit

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run app.py
```

### 3. Run Unit Tests
```bash
python tests/test_pipeline.py
```

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t jobfit-app .

# Run container
docker run -p 8501:8501 jobfit-app
```

---

## 📄 License & Author

Developed by **Ratnesh** (`Ratnesh1007`). Built with Python, Streamlit, FAISS, FastEmbed, and PyMuPDF.
