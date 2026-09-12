import re
import json
import ollama


MODEL_NAME = "llama3.2:3b"


# ==========================================
# BATCH REQUIREMENT ANALYSIS
# ==========================================

def heuristic_fallback_analysis(requirements_with_evidence):
    """
    Strict, section-aware semantic & evidence analysis.
    Distinguishes between solid work/project experience vs weak skill/certification listings.
    """
    results = []

    for i, item in enumerate(requirements_with_evidence, start=1):
        requirement = item["requirement"]
        category = item.get("category", "Other")
        evidence = item.get("evidence", [])

        max_sim = 0.0
        best_chunk = ""
        best_section = "GENERAL"

        for ev in evidence:
            sim = ev.get("similarity", 0.0)
            chunk_text = ev.get("chunk", "")
            if sim > max_sim:
                max_sim = sim
                best_chunk = chunk_text
                sec_match = re.search(r"\[Section:\s*([A-Z\s]+)\]", chunk_text)
                if sec_match:
                    best_section = sec_match.group(1).strip()

        req_lower = requirement.lower()
        req_words = set(re.findall(r"\b\w{3,}\b", req_lower))
        ev_words = set(re.findall(r"\b\w{3,}\b", best_chunk.lower())) if best_chunk else set()
        overlap = len(req_words.intersection(ev_words)) / max(len(req_words), 1)

        is_experience_req = (category == "Experience") or any(
            w in req_lower for w in ["experience", "years", "developing", "building", "working", "engineer", "developer"]
        )

        has_action_verbs = any(
            verb in best_chunk.lower()
            for verb in ["developed", "built", "implemented", "engineered", "managed", "designed", "created", "architected", "worked"]
        )

        is_from_work_or_project = best_section in ["WORK EXPERIENCE", "PROJECTS"]
        is_from_cert_or_skill = best_section in ["CERTIFICATIONS", "SKILLS"]

        if is_experience_req:
            if is_from_work_or_project and (max_sim >= 0.45 or overlap >= 0.35 or has_action_verbs):
                status = "FULFILLED"
                confidence = round(min(max(max_sim, overlap, 0.85), 0.95), 2)
                reason = f"✅ Solid evidence verified in '{best_section}' section showing hands-on application."
            elif is_from_cert_or_skill and (max_sim >= 0.40 or overlap >= 0.3):
                status = "PARTIALLY_FULFILLED"
                confidence = 0.55
                reason = f"⚠️ Listed in '{best_section}' section, but lacks explicit work experience or project achievements."
            elif max_sim >= 0.45 and has_action_verbs:
                status = "FULFILLED"
                confidence = round(min(max_sim, 0.85), 2)
                reason = "✅ Supporting work experience evidence identified in resume text."
            elif max_sim >= 0.30 or overlap >= 0.2:
                status = "PARTIALLY_FULFILLED"
                confidence = 0.45
                reason = "⚠️ Partial evidence found, but full hands-on experience is not explicitly demonstrated."
            else:
                status = "NOT_FULFILLED"
                confidence = round(max(max_sim, 0.1), 2)
                reason = "❌ No solid work experience or project evidence found for this requirement."
        else:
            if max_sim >= 0.55 or overlap >= 0.45:
                status = "FULFILLED"
                confidence = round(min(max(max_sim, overlap, 0.80), 0.95), 2)
                reason = "✅ Resume evidence directly supports this requirement."
            elif max_sim >= 0.35 or overlap >= 0.2:
                status = "PARTIALLY_FULFILLED"
                confidence = round(max(max_sim, overlap, 0.50), 2)
                reason = "⚠️ Partial evidence found in resume text."
            else:
                status = "NOT_FULFILLED"
                confidence = round(max(max_sim, 0.1), 2)
                reason = "❌ No clear supporting evidence found in resume."

        results.append({
            "requirement_number": i,
            "status": status,
            "confidence": confidence,
            "reason": reason,
            "evidence": best_chunk[:300] if best_chunk else ""
        })

    return results


# ==========================================
# BATCH REQUIREMENT ANALYSIS
# ==========================================

def analyze_requirements(
    requirements_with_evidence,
    mode="deep"
):
    """
    Analyze all JD requirements in a single
    Llama request with fallback.
    """

    if not requirements_with_evidence:
        return []

    if mode == "fast":
        return heuristic_fallback_analysis(requirements_with_evidence)

    # ==========================================
    # BUILD REQUIREMENT + EVIDENCE TEXT
    # ==========================================

    analysis_input = ""

    for i, item in enumerate(
        requirements_with_evidence,
        start=1
    ):

        requirement = item["requirement"]
        category = item["category"]
        evidence = item["evidence"]

        evidence_text = ""

        for j, ev in enumerate(
            evidence,
            start=1
        ):

            evidence_text += (
                f"Evidence {j}: "
                f"{ev['chunk']}\n"
            )

        analysis_input += f"""
REQUIREMENT {i}

Requirement:
{requirement}

Category:
{category}

Resume Evidence:
{evidence_text}

----------------------------------------
"""


    # ==========================================
    # SYSTEM PROMPT WITH STRICT ACCURACY RULES
    # ==========================================

    system_prompt = """
You are JOBFit, an AI-powered resume screening system.

You must evaluate multiple job requirements against the provided resume evidence.

STRICT ACCURACY RULES:

1. CERTIFICATIONS & SKILLS LISTS ARE NOT WORK EXPERIENCE:
   - A certificate (e.g., "Certified Kubernetes Administrator") or a skill listed in a "SKILLS" list is NOT solid proof of work experience.
   - If a requirement asks for "Experience", "Years of experience", or "Hands-on experience", and the ONLY evidence comes from a CERTIFICATIONS or SKILLS section:
     -> Mark as PARTIALLY_FULFILLED or NOT_FULFILLED (NEVER FULFILLED).
     -> Reason must state: "Skill/Cert listed in resume, but no work experience or project bullet points found."

2. FULFILLED REQUIRES EXPLICIT WORK / PROJECT APPLICATION:
   - Mark as FULFILLED ONLY when the resume explicitly shows work experience, job responsibilities, project descriptions, or accomplishments from WORK EXPERIENCE or PROJECTS sections demonstrating the skill in action.

3. NO PRESUMPTIONS:
   - Never presume experience based on unrelated certificates. Only base evaluation on explicit text in resume evidence.

STATUS DEFINITIONS:

FULFILLED:
Clear work experience or project evidence supports the complete requirement.

PARTIALLY_FULFILLED:
Only some parts of the requirement are supported, or skill is listed in Certifications/Skills without work experience.

NOT_FULFILLED:
No meaningful supporting evidence exists.

Return ONLY valid JSON format:

{
    "results": [
        {
            "requirement_number": 1,
            "status": "FULFILLED",
            "confidence": 0.90,
            "reason": "The resume explicitly demonstrates work experience for this requirement.",
            "evidence": "Relevant resume evidence."
        }
    ]
}
"""


    # ==========================================
    # USER PROMPT
    # ==========================================

    user_prompt = f"""
Evaluate all of the following job requirements.

Return one result for EVERY requirement.

{analysis_input}

Return ONLY valid JSON.
"""


    # ==========================================
    # CALL LLAMA ONCE
    # ==========================================

    try:

        response = ollama.chat(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            format="json",

            options={
                "temperature": 0,
                "num_predict": 1500
            },

            keep_alive="10m"
        )

        response_text = (
            response["message"]["content"]
        )

        result = json.loads(
            response_text
        )

        results = result.get(
            "results",
            []
        )

        if not isinstance(
            results,
            list
        ) or not results:
            return heuristic_fallback_analysis(requirements_with_evidence)


        # ======================================
        # VALIDATE RESULTS
        # ======================================

        validated_results = []

        allowed_statuses = {
            "FULFILLED",
            "PARTIALLY_FULFILLED",
            "NOT_FULFILLED"
        }

        for item in results:

            status = item.get(
                "status",
                "NOT_FULFILLED"
            )

            if status not in allowed_statuses:

                status = "NOT_FULFILLED"


            try:

                confidence = float(
                    item.get(
                        "confidence",
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                confidence = 0.0


            confidence = max(
                0.0,
                min(
                    1.0,
                    confidence
                )
            )


            validated_results.append({

                "requirement_number": item.get(
                    "requirement_number",
                    len(validated_results) + 1
                ),

                "status": status,

                "confidence": round(
                    confidence,
                    2
                ),

                "reason": str(
                    item.get(
                        "reason",
                        ""
                    )
                ),

                "evidence": str(
                    item.get(
                        "evidence",
                        ""
                    )
                )
            })


        return validated_results


    except Exception as error:

        print(
            f"\nLLM batch analysis error: {error}. Using heuristic fallback."
        )

        return heuristic_fallback_analysis(requirements_with_evidence)