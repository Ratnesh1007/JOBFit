import re


def check_contact_information(text):
    results = {}

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    results["email"] = bool(re.search(email_pattern, text))

    phone_pattern = r"(\+?\d[\d\s().-]{8,}\d)"
    results["phone"] = bool(re.search(phone_pattern, text))

    results["linkedin"] = "linkedin" in text.lower()
    results["github"] = "github" in text.lower()

    return results


def check_resume_sections(text):
    text_lower = text.lower()

    sections = {
        "Summary / Objective": [
            "summary",
            "professional summary",
            "objective",
            "career objective"
        ],
        "Education": [
            "education",
            "academic qualification",
            "academic qualifications"
        ],
        "Experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment"
        ],
        "Skills": [
            "skills",
            "technical skills",
            "technical skill"
        ],
        "Projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],
        "Certifications": [
            "certifications",
            "certification",
            "certificates"
        ]
    }

    results = {}

    for section, keywords in sections.items():
        results[section] = any(
            keyword in text_lower
            for keyword in keywords
        )

    return results


def check_achievement_language(text):
    text_lower = text.lower()

    action_words = [
        "developed",
        "built",
        "created",
        "implemented",
        "designed",
        "optimized",
        "improved",
        "automated",
        "engineered",
        "deployed",
        "led",
        "managed",
        "analyzed",
        "reduced",
        "increased",
        "achieved"
    ]

    metric_pattern = (
        r"(?:[\$\€\£\₹]\s*\d+|\b\d+(?:\.\d+)?\s*(?:%|percent|users|clients|customers|projects|months|years|x|k|m|b|\+)?\b)"
    )

    action_word_count = sum(
        text_lower.count(word)
        for word in action_words
    )

    metric_count = len(
        re.findall(metric_pattern, text_lower)
    )

    return {
        "action_words": action_word_count,
        "metrics": metric_count,
        "has_metrics": metric_count > 0
    }


def check_resume_length(text):
    word_count = len(text.split())

    if word_count < 200:
        rating = "Very Short"
    elif word_count < 400:
        rating = "Short"
    elif word_count <= 1200:
        rating = "Good"
    elif word_count <= 1800:
        rating = "Long"
    else:
        rating = "Very Long"

    return {
        "word_count": word_count,
        "rating": rating
    }


def calculate_quality_score(
    contact_info,
    sections,
    achievements,
    length
):
    score = 0

    # Contact information: 20 points
    if contact_info["email"]:
        score += 5

    if contact_info["phone"]:
        score += 5

    if contact_info["linkedin"]:
        score += 5

    if contact_info["github"]:
        score += 5

    # Important sections: 30 points
    important_sections = [
        "Education",
        "Experience",
        "Skills",
        "Projects"
    ]

    for section in important_sections:
        if sections.get(section, False):
            score += 7.5

    # Achievement language: 30 points
    if achievements["action_words"] >= 5:
        score += 15
    elif achievements["action_words"] >= 2:
        score += 8

    if achievements["has_metrics"]:
        score += 15

    # Resume length: 20 points
    if length["rating"] == "Good":
        score += 20
    elif length["rating"] == "Short":
        score += 15
    elif length["rating"] == "Long":
        score += 12
    elif length["rating"] == "Very Short":
        score += 7
    elif length["rating"] == "Very Long":
        score += 5

    return round(min(score, 100), 2)


def analyze_resume_quality(text):
    contact_info = check_contact_information(text)
    sections = check_resume_sections(text)
    achievements = check_achievement_language(text)
    length = check_resume_length(text)

    quality_score = calculate_quality_score(
        contact_info,
        sections,
        achievements,
        length
    )

    return {
        "quality_score": quality_score,
        "contact_info": contact_info,
        "sections": sections,
        "achievements": achievements,
        "length": length
    }