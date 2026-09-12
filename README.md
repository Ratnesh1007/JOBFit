# 📄 JOBFit Intelligence

> **AI-Powered Resume Screening & Job Description Compatibility Matcher**

JOBFit Intelligence is an enterprise-grade AI resume evaluation application that analyzes candidate resumes against job descriptions. It calculates ATS-style compatibility scores, performs section-aware semantic evidence verification, extracts technical keywords, and audits structural resume quality to help candidates optimize their resumes for target roles.

---

## ✨ Key Features

- ⚡ **Dual Processing Engine**:
  - **Lightning Mode (1–2 sec)**: Instant semantic vector matching using Sentence Transformers (`bge-small-en-v1.5`), FAISS, and rule-based heuristics.
  - **Deep AI Mode (3–5 sec)**: Deep contextual reasoning powered by a single-pass Llama 3.2 3B model.
- 🛡️ **Section-Aware Solid Evidence Verification**:
  - Distinguishes between verified work experience bullet points vs. standalone skill lists or certificates.
  - Certifications & Skills lists are **never** counted as Work Experience for experience requirements.
- 🔑 **Technical Keywords Matrix**:
  - Rule-based keyword matching & normalization across 100+ technologies (languages, frameworks, cloud platforms, tools, databases).
- 📑 **Resume Quality & Structural Audit**:
  - Evaluates contact details (Email, Phone, LinkedIn, GitHub), mandatory resume sections, action verb density, and quantified metrics.
- 💡 **Actionable Improvement Roadmap**:
  - Generates prioritized recommendations for missing mandatory skills, missing keywords, and formatting fixes.
- 📥 **Export Evaluation Report**:
  - Export full candidate evaluation summaries in Markdown format with one click.

---

## 🛠️ Tech Stack & Architecture

- **Frontend & UI**: Streamlit (with custom CSS design system & dark mode compatibility)
- **PDF Extraction**: PyMuPDF (`pymupdf`)
- **Text Embeddings**: BAAI/bge-small-en-v1.5 (`fastembed`)
- **Vector Database**: FAISS (`IndexFlatIP`)
- **AI Model / Reasoning**: Llama 3.2 3B (`ollama`) / Fast Heuristic Engine
- **Containerization & Deployment**: Docker, Railway, Render, Streamlit Cloud

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- (Optional) [Ollama](https://ollama.com/) with `llama3.2:3b` model installed for Deep AI Mode.

### 2. Installation
```bash
# Clone the repository
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

### 3. Run the Application
```bash
streamlit run app.py
```

---

## 🧪 Running Unit Tests

Run the complete pipeline verification suite:
```bash
python tests/test_pipeline.py
```

---

## 🐳 Docker Deployment

Build and run the production container locally:
```bash
# Build Docker image
docker build -t jobfit-app .

# Run container
docker run -p 8501:8501 jobfit-app
```

Deploy 24/7 on [Railway.app](https://railway.app) or [Render.com](https://render.com) by connecting your GitHub repository `Ratnesh1007/JOBFit`.

---

## 📄 License & Attribution

Developed by **Ratnesh** (`Ratnesh1007`). Built with Python, Streamlit, FAISS, and FastEmbed.
