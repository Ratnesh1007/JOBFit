def classify_requirement(requirement):
    text = requirement.lower()

    if any(word in text for word in [
        "experience",
        "years",
        "worked",
        "professional experience"
    ]):
        return "Experience"

    if any(word in text for word in [
        "degree",
        "bachelor",
        "master",
        "education",
        "b.tech",
        "b.e.",
        "computer science"
    ]):
        return "Education"

    if any(word in text for word in [
        "certification",
        "certified",
        "certificate"
    ]):
        return "Certification"

    if any(word in text for word in [
        "python",
        "java",
        "sql",
        "machine learning",
        "docker",
        "aws",
        "react",
        "javascript",
        "spring",
        "api",
        "git",
        "github",
        "kubernetes",
        "cloud",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "scikit-learn"
    ]):
        return "Technical Skill"

    if any(word in text for word in [
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "problem-solving",
        "analytical",
        "collaboration"
    ]):
        return "Soft Skill"

    return "Other"


def classify_importance(requirement, section=""):
    """
    Classify a requirement as MANDATORY, PREFERRED, or OTHER.

    The section heading is used because requirements such as
    'Strong Python programming skills' may not contain words
    like 'required' themselves.
    """

    text = requirement.lower()
    section_text = section.lower()

    mandatory_keywords = [
        "required",
        "mandatory",
        "must have",
        "must-have",
        "essential",
        "minimum qualification",
        "minimum qualifications",
        "required qualification",
        "required qualifications"
    ]

    preferred_keywords = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "good to have",
        "good-to-have",
        "desirable",
        "preferred qualification",
        "preferred qualifications"
    ]

    # Check the section heading first
    if any(keyword in section_text for keyword in mandatory_keywords):
        return "MANDATORY"

    if any(keyword in section_text for keyword in preferred_keywords):
        return "PREFERRED"

    # Then check the actual requirement
    if any(keyword in text for keyword in mandatory_keywords):
        return "MANDATORY"

    if any(keyword in text for keyword in preferred_keywords):
        return "PREFERRED"

    return "OTHER"