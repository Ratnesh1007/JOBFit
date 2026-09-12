from src.embeddings import generate_embeddings
from src.vector_store import search_faiss


def match_requirement(
    requirement,
    index,
    resume_chunks,
    top_k=2,
    category="Other"
):
    """
    Find the most relevant resume chunks for a given job requirement,
    prioritizing Work Experience and Project sections for experience requirements.
    """

    if not resume_chunks or index is None:
        return []

    # Convert requirement to embedding
    query_embedding = generate_embeddings(
        [requirement]
    )

    # Fetch slightly more candidates to filter/re-rank by section context
    fetch_k = min(max(top_k * 2, 4), len(resume_chunks))

    similarities, indices = search_faiss(
        index,
        query_embedding,
        k=fetch_k
    )

    candidates = []
    seen_indices = set()

    for similarity, idx in zip(similarities, indices):
        idx_int = int(idx)
        if idx_int < 0 or idx_int >= len(resume_chunks) or idx_int in seen_indices:
            continue

        seen_indices.add(idx_int)
        chunk = resume_chunks[idx_int]
        
        # Section priority score boost
        priority_boost = 0.0
        req_lower = requirement.lower()
        is_exp_req = (category == "Experience") or any(w in req_lower for w in ["experience", "years", "developing", "building", "working"])

        if is_exp_req:
            if "[Section: WORK EXPERIENCE]" in chunk or "[Section: PROJECTS]" in chunk:
                priority_boost += 0.25
            elif "[Section: CERTIFICATIONS]" in chunk or "[Section: SKILLS]" in chunk:
                priority_boost -= 0.15

        adjusted_similarity = float(similarity) + priority_boost

        candidates.append({
            "similarity": float(similarity),
            "adjusted_similarity": adjusted_similarity,
            "chunk": chunk
        })

    # Sort candidates by adjusted similarity
    candidates.sort(key=lambda x: x["adjusted_similarity"], reverse=True)

    results = []
    for cand in candidates[:top_k]:
        results.append({
            "similarity": cand["similarity"],
            "chunk": cand["chunk"]
        })

    return results