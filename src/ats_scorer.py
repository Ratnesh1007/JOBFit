CATEGORY_WEIGHTS = {
    "Technical Skill": 0.40,
    "Experience": 0.25,
    "Education": 0.15,
    "Certification": 0.10,
    "Soft Skill": 0.05,
    "Other": 0.05
}


STATUS_SCORES = {
    "FULFILLED": 1.0,
    "PARTIALLY_FULFILLED": 0.5,
    "NOT_FULFILLED": 0.0
}


IMPORTANCE_WEIGHTS = {
    "MANDATORY": 1.5,
    "PREFERRED": 1.0,
    "OTHER": 0.75
}


def calculate_requirement_score(result):
    """
    Calculate the contribution of one requirement.
    """

    category = result.get(
        "category",
        "Other"
    )

    status = result.get(
        "status",
        "NOT_FULFILLED"
    )

    importance = result.get(
        "importance",
        "OTHER"
    )

    category_weight = CATEGORY_WEIGHTS.get(
        category,
        CATEGORY_WEIGHTS["Other"]
    )

    status_score = STATUS_SCORES.get(
        status,
        0
    )

    importance_weight = IMPORTANCE_WEIGHTS.get(
        importance,
        IMPORTANCE_WEIGHTS["OTHER"]
    )

    return (
        category_weight
        * importance_weight
        * status_score
    )


def calculate_requirement_match_score(results):

    if not results:
        return 0

    total_score = 0
    total_possible_score = 0

    for result in results:

        category = result.get(
            "category",
            "Other"
        )

        importance = result.get(
            "importance",
            "OTHER"
        )

        category_weight = CATEGORY_WEIGHTS.get(
            category,
            CATEGORY_WEIGHTS["Other"]
        )

        importance_weight = IMPORTANCE_WEIGHTS.get(
            importance,
            IMPORTANCE_WEIGHTS["OTHER"]
        )

        possible_score = (
            category_weight
            * importance_weight
        )

        total_possible_score += possible_score

        total_score += calculate_requirement_score(
            result
        )

    if total_possible_score == 0:
        return 0

    return (
        total_score
        / total_possible_score
    ) * 100


def calculate_keyword_match_score(
    jd_keywords,
    resume_keywords
):

    if not jd_keywords:
        return 100

    jd_keywords = {
        keyword.lower().strip()
        for keyword in jd_keywords
    }

    resume_keywords = {
        keyword.lower().strip()
        for keyword in resume_keywords
    }

    matched_keywords = (
        jd_keywords
        .intersection(resume_keywords)
    )

    return (
        len(matched_keywords)
        / len(jd_keywords)
    ) * 100


def calculate_ats_score(
    results,
    jd_keywords=None,
    resume_keywords=None
):

    if jd_keywords is None:
        jd_keywords = []

    if resume_keywords is None:
        resume_keywords = []

    requirement_score = (
        calculate_requirement_match_score(
            results
        )
    )

    keyword_score = (
        calculate_keyword_match_score(
            jd_keywords,
            resume_keywords
        )
    )

    # Requirement fulfillment is more important
    # than simple keyword presence.
    final_score = (
        requirement_score * 0.70
        + keyword_score * 0.30
    )

    return round(
        final_score,
        2
    )