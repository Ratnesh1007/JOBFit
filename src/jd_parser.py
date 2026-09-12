import re


def load_jd_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_requirements(text):
    lines = text.split("\n")
    requirements = []

    requirement_keywords = [
        "experience",
        "years of experience",
        "professional experience",
        "skills",
        "skill",
        "proficiency",
        "proficient",
        "expertise",
        "knowledge",
        "familiarity",
        "understanding",
        "programming",
        "bachelor",
        "bachelor's",
        "master",
        "master's",
        "degree",
        "education",
        "certification",
        "certified",
        "certificate",
        "must have",
        "required",
        "requirement",
        "preferred",
        "nice to have",
        "good to have",
        "desirable",
        "problem-solving",
        "problem solving",
        "communication",
        "leadership",
        "teamwork",
        "collaboration"
    ]

    section_headers = [
        "requirements",
        "qualifications",
        "skills",
        "responsibilities",
        "required qualifications",
        "required qualification",
        "preferred qualifications",
        "preferred qualification",
        "preferred skills",
        "what we're looking for",
        "what we are looking for"
    ]

    current_section = "OTHER"

    mandatory_sections = [
        "requirements",
        "required qualifications",
        "required qualification",
        "mandatory qualifications",
        "mandatory qualification"
    ]

    preferred_sections = [
        "preferred qualifications",
        "preferred qualification",
        "preferred skills",
        "nice to have",
        "good to have",
        "desirable"
    ]

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove bullet symbols for requirement text
        cleaned_line = re.sub(
            r"^[•\-\*\u2022▪◦\d+\.]\s*",
            "",
            line
        ).strip()

        if not cleaned_line:
            continue

        # Strip markdown header characters (#, *, :) for heading comparison
        line_lower = re.sub(r"^[#\*\s]+|[:\*\s]+$", "", cleaned_line.lower()).strip()

        # Detect section headings
        if line_lower in section_headers:
            if line_lower in mandatory_sections:
                current_section = "MANDATORY"
            elif line_lower in preferred_sections:
                current_section = "PREFERRED"
            else:
                current_section = "OTHER"

            continue

        # Detect headings containing important section words
        if (
            "required qualification" in line_lower
            or "required skill" in line_lower
            or "mandatory qualification" in line_lower
            or "requirements" in line_lower
        ):
            current_section = "MANDATORY"
            continue

        if (
            "preferred qualification" in line_lower
            or "preferred skill" in line_lower
            or "nice to have" in line_lower
        ):
            current_section = "PREFERRED"
            continue

        # Determine whether this line is a requirement
        is_requirement = any(
            keyword in line_lower
            for keyword in requirement_keywords
        )

        was_bullet = bool(
            re.match(
                r"^[•\-\*\u2022▪◦]\s*",
                line
            )
        )

        if is_requirement or was_bullet:

            requirements.append({
                "text": cleaned_line,
                "importance": current_section
            })

    # Remove duplicate requirements
    unique_requirements = []

    for requirement in requirements:
        already_exists = any(
            existing["text"].lower()
            == requirement["text"].lower()
            for existing in unique_requirements
        )

        if not already_exists:
            unique_requirements.append(requirement)

    return unique_requirements