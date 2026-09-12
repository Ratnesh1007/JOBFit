import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.text_cleaner import clean_text
from src.chunker import split_text
from src.embeddings import generate_embeddings
from src.vector_store import create_faiss_index, search_faiss
from src.matcher import match_requirement
from src.jd_parser import extract_requirements
from src.keyword_extractor import extract_rule_based_keywords, normalize_keyword
from src.requirement_classifier import classify_requirement, classify_importance
from src.ats_scorer import calculate_ats_score, calculate_requirement_match_score, calculate_keyword_match_score
from src.resume_quality import analyze_resume_quality
from src.pipeline import analyze_resume


def test_text_cleaner():
    raw_text = "  Hello   world!  \n\n\n\n  This is   a test.  "
    cleaned = clean_text(raw_text)
    assert "Hello world!" in cleaned and "This is a test." in cleaned


def test_chunker():
    text = "Word " * 200
    chunks = split_text(text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)


def test_vector_store_and_matcher():
    chunks = ["Python developer with FastAPI experience.", "Data scientist with PyTorch and SQL."]
    embeddings = generate_embeddings(chunks)
    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == 384

    index = create_faiss_index(embeddings)
    assert index.ntotal == 2

    matches = match_requirement("Python FastAPI", index, chunks, top_k=2)
    assert len(matches) == 2
    assert "Python developer" in matches[0]["chunk"]


def test_jd_parser():
    jd = """
    Required Qualifications:
    - 3+ years of Python programming experience
    - Strong SQL skills

    Preferred Qualifications:
    - Experience with Docker and Kubernetes
    """
    reqs = extract_requirements(jd)
    assert len(reqs) >= 3
    mandatory_reqs = [r for r in reqs if r["importance"] == "MANDATORY"]
    assert len(mandatory_reqs) >= 2


def test_keyword_extractor():
    text = "Seeking a developer skilled in Python, ML, PostgreSQL, and AWS."
    keywords = extract_rule_based_keywords(text)
    assert "python" in keywords
    assert "machine learning" in keywords
    assert "postgresql" in keywords
    assert "aws" in keywords


def test_ats_scorer():
    results = [
        {"category": "Technical Skill", "importance": "MANDATORY", "status": "FULFILLED"},
        {"category": "Education", "importance": "PREFERRED", "status": "NOT_FULFILLED"}
    ]
    req_score = calculate_requirement_match_score(results)
    assert 0 <= req_score <= 100

    kw_score = calculate_keyword_match_score(["python", "docker"], ["python"])
    assert kw_score == 50.0

    ats = calculate_ats_score(results, ["python", "docker"], ["python"])
    assert 0 <= ats <= 100


def test_resume_quality():
    text = """
    John Doe
    Email: john@example.com | Phone: +1 555-123-4567 | linkedin.com/in/johndoe | github.com/johndoe
    Summary: Experienced Software Engineer.
    Experience: Developed 5 scalable microservices using Python and Docker. Improved query latency by 40%.
    Education: B.S. in Computer Science.
    Skills: Python, Docker, SQL.
    Projects: Personal portfolio app.
    """
    q = analyze_resume_quality(text)
    assert q["quality_score"] > 60
    assert q["contact_info"]["email"] is True
    assert q["contact_info"]["phone"] is True
    assert q["contact_info"]["linkedin"] is True
    assert q["contact_info"]["github"] is True
    assert q["achievements"]["action_words"] >= 2
    assert q["achievements"]["metrics"] >= 1


def test_full_pipeline_with_test_pdf():
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), """
    Jane Smith
    Email: jane@example.com | Phone: 9876543210
    Experience:
    Software Engineer with 4 years experience in Python, FastAPI, Docker, and AWS.
    Built microservices and optimized PostgreSQL database queries.
    Education:
    Bachelor of Technology in Computer Science.
    Skills: Python, FastAPI, Docker, AWS, PostgreSQL, SQL, Git
    """)
    test_pdf_path = "temp_pipeline_test.pdf"
    doc.save(test_pdf_path)
    doc.close()

    try:
        jd = "Required: Python, FastAPI, Docker. Preferred: AWS, PostgreSQL."
        # Test Fast Mode (Lightning)
        output_fast = analyze_resume(test_pdf_path, jd, mode="fast")
        assert output_fast["jd_match_score"] > 50
        assert "python" in output_fast["matched_keywords"]
        assert len(output_fast["analysis_results"]) > 0

        # Test Deep Mode
        output_deep = analyze_resume(test_pdf_path, jd, mode="deep")
        assert output_deep["jd_match_score"] > 50
        assert "python" in output_deep["matched_keywords"]
        assert len(output_deep["analysis_results"]) > 0
    finally:
        if os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)


def test_certifications_vs_work_experience():
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), """
    Alex Johnson
    Email: alex@example.com

    Work Experience:
    Software Developer at TechCorp. Built Python web applications.

    Certifications:
    Certified Kubernetes Administrator (CKA)
    AWS Certified Solutions Architect
    """)
    test_pdf_path = "temp_cert_test.pdf"
    doc.save(test_pdf_path)
    doc.close()

    try:
        jd = "Required: 3+ years experience with Kubernetes and CI/CD pipelines."
        output = analyze_resume(test_pdf_path, jd, mode="fast")
        res = output["analysis_results"][0]
        assert res["status"] in ["PARTIALLY_FULFILLED", "NOT_FULFILLED"]
        assert "CERTIFICATIONS" in res["reason"] or "lacks" in res["reason"] or "No solid work" in res["reason"]
    finally:
        if os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)


if __name__ == "__main__":
    print("Running test_text_cleaner...")
    test_text_cleaner()
    print("Running test_chunker...")
    test_chunker()
    print("Running test_vector_store_and_matcher...")
    test_vector_store_and_matcher()
    print("Running test_jd_parser...")
    test_jd_parser()
    print("Running test_keyword_extractor...")
    test_keyword_extractor()
    print("Running test_ats_scorer...")
    test_ats_scorer()
    print("Running test_resume_quality...")
    test_resume_quality()
    print("Running test_certifications_vs_work_experience...")
    test_certifications_vs_work_experience()
    print("Running test_full_pipeline_with_test_pdf...")
    test_full_pipeline_with_test_pdf()
    print("\nALL PIPELINE UNIT TESTS PASSED SUCCESSFULLY!")
