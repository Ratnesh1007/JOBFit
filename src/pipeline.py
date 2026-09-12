from src.pdf_parser import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.chunker import split_text
from src.embeddings import generate_embeddings
from src.vector_store import create_faiss_index
from src.jd_parser import extract_requirements
from src.matcher import match_requirement

from src.requirement_classifier import (
    classify_requirement,
    classify_importance
)

from src.llm_analyzer import analyze_requirements

from src.ats_scorer import (
    calculate_ats_score,
    calculate_requirement_match_score,
    calculate_keyword_match_score
)

from src.keyword_extractor import extract_keywords

from src.resume_quality import analyze_resume_quality


def analyze_resume(resume_path, jd_text, mode="deep", status_callback=None):

    def update_status(msg):
        if status_callback:
            status_callback(msg)

    # ========================================================
    # 1. EXTRACT RESUME TEXT
    # ========================================================
    update_status("📄 Extracting text from PDF...")

    raw_resume = extract_text_from_pdf(
        resume_path
    )


    # ========================================================
    # 2. CLEAN RESUME TEXT
    # ========================================================
    cleaned_resume = clean_text(
        raw_resume
    )


    # ========================================================
    # 3. RESUME QUALITY ANALYSIS
    # ========================================================
    update_status("📑 Auditing resume formatting & quality...")

    resume_quality = analyze_resume_quality(
        cleaned_resume
    )


    # ========================================================
    # 4. SPLIT RESUME INTO CHUNKS & EXTRACT KEYWORDS
    # ========================================================
    update_status("🔑 Chunking text & extracting technical keywords...")

    resume_chunks = split_text(
        cleaned_resume
    )

    resume_keywords = extract_keywords(
        cleaned_resume,
        use_llm=False
    )


    # ========================================================
    # 5. GENERATE RESUME EMBEDDINGS & FAISS INDEX
    # ========================================================
    update_status("🧠 Generating Sentence Transformer embeddings & FAISS index...")

    resume_embeddings = generate_embeddings(
        resume_chunks
    )

    index = create_faiss_index(
        resume_embeddings
    )


    # ========================================================
    # 6. EXTRACT JD REQUIREMENTS & KEYWORDS
    # ========================================================
    update_status("📋 Extracting & classifying JD requirements...")

    requirements = extract_requirements(
        jd_text
    )

    jd_keywords = extract_keywords(
        jd_text,
        use_llm=False
    )


    # ========================================================
    # 7. MATCH REQUIREMENTS WITH RESUME
    # ========================================================
    update_status("🔍 Matching requirements against resume chunks...")

    requirements_with_evidence = []

    for requirement_data in requirements:

        requirement = requirement_data["text"]

        category = classify_requirement(
            requirement
        )

        importance = classify_importance(
            requirement,
            requirement_data["importance"]
        )

        evidence = match_requirement(
            requirement,
            index,
            resume_chunks,
            top_k=2
        )

        requirements_with_evidence.append({

            "requirement": requirement,

            "category": category,

            "importance": importance,

            "evidence": evidence

        })


    # ========================================================
    # 8. REQUIREMENT ANALYSIS (DEEP OR FAST)
    # ========================================================
    if mode == "fast":
        update_status("⚡ Evaluating requirements using Fast Vector Heuristics...")
    else:
        update_status("🤖 Running Deep AI requirement analysis (Llama 3.2 3B)...")

    llm_results = analyze_requirements(
        requirements_with_evidence,
        mode=mode
    )


    # ========================================================
    # 12. COMBINE REQUIREMENT + LLM RESULTS
    # ========================================================

    analysis_results = []


    for index_number, item in enumerate(
        requirements_with_evidence
    ):

        llm_result = None


        # ----------------------------------------------------
        # Find matching LLM result
        # ----------------------------------------------------

        for result in llm_results:

            if result.get(
                "requirement_number"
            ) == index_number + 1:

                llm_result = result

                break


        # ----------------------------------------------------
        # Fallback if LLM failed to return a result
        # ----------------------------------------------------

        if llm_result is None:

            llm_result = {

                "status": "NOT_FULFILLED",

                "confidence": 0.0,

                "reason": (
                    "No LLM evaluation was returned."
                ),

                "evidence": ""

            }


        # ----------------------------------------------------
        # Create final requirement result
        # ----------------------------------------------------

        final_result = {

            "requirement": item["requirement"],

            "category": item["category"],

            "importance": item["importance"],

            "status": llm_result.get(
                "status",
                "NOT_FULFILLED"
            ),

            "confidence": llm_result.get(
                "confidence",
                0
            ),

            "reason": llm_result.get(
                "reason",
                ""
            ),

            "evidence": llm_result.get(
                "evidence",
                ""
            )

        }


        analysis_results.append(
            final_result
        )


    # ========================================================
    # 13. REQUIREMENT MATCH SCORE
    # ========================================================

    requirement_match_score = (
        calculate_requirement_match_score(
            analysis_results
        )
    )


    # ========================================================
    # 14. KEYWORD MATCH SCORE
    # ========================================================

    keyword_match_score = (
        calculate_keyword_match_score(
            jd_keywords,
            resume_keywords
        )
    )


    # ========================================================
    # 15. FINAL JOBFIT / ATS SCORE
    # ========================================================

    jd_match_score = calculate_ats_score(
        analysis_results,
        jd_keywords,
        resume_keywords
    )


    # ========================================================
    # 16. MATCHED KEYWORDS
    # ========================================================

    resume_keyword_set = {
        keyword.lower().strip()
        for keyword in resume_keywords
    }


    matched_keywords = [

        keyword

        for keyword in jd_keywords

        if keyword.lower().strip()
        in resume_keyword_set

    ]


    # ========================================================
    # 17. MISSING KEYWORDS
    # ========================================================

    missing_keywords = [

        keyword

        for keyword in jd_keywords

        if keyword.lower().strip()
        not in resume_keyword_set

    ]


    # ========================================================
    # 18. REQUIREMENT STATUS COUNTS
    # ========================================================

    fulfilled = sum(

        1

        for result in analysis_results

        if result["status"]
        == "FULFILLED"

    )


    partially_fulfilled = sum(

        1

        for result in analysis_results

        if result["status"]
        == "PARTIALLY_FULFILLED"

    )


    not_fulfilled = sum(

        1

        for result in analysis_results

        if result["status"]
        == "NOT_FULFILLED"

    )


    # ========================================================
    # 19. RETURN COMPLETE JOBFIT ANALYSIS
    # ========================================================

    return {

        # Resume
        "resume_text": cleaned_resume,

        "resume_chunks": resume_chunks,

        "resume_keywords": resume_keywords,

        # Resume quality
        "resume_quality": resume_quality,

        # Job description
        "jd_text": jd_text,

        "requirements": requirements,

        "jd_keywords": jd_keywords,

        # Requirement analysis
        "analysis_results": analysis_results,

        "fulfilled": fulfilled,

        "partially_fulfilled": partially_fulfilled,

        "not_fulfilled": not_fulfilled,

        # Keywords
        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        # Scores
        "requirement_match_score": round(
            requirement_match_score,
            2
        ),

        "keyword_match_score": round(
            keyword_match_score,
            2
        ),

        "jd_match_score": jd_match_score

    }