import re

SECTION_HEADERS = {
    "WORK EXPERIENCE": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history"
    ],
    "PROJECTS": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects"
    ],
    "EDUCATION": [
        "education",
        "academic qualification",
        "academic qualifications",
        "education & credentials"
    ],
    "CERTIFICATIONS": [
        "certifications",
        "certification",
        "licenses & certifications",
        "certificates"
    ],
    "SKILLS": [
        "skills",
        "technical skills",
        "skills & tools",
        "core competencies"
    ],
    "SUMMARY": [
        "summary",
        "professional summary",
        "about me",
        "profile"
    ]
}


def detect_section_header(line):
    line_clean = re.sub(r"^[#\*\s\u2022\-]+|[:\*\s]+$", "", line.lower()).strip()
    for section, keywords in SECTION_HEADERS.items():
        if line_clean in keywords or any(line_clean == kw for kw in keywords):
            return section
    return None


def split_text(text, chunk_size=500, chunk_overlap=50):
    """
    Section-aware text chunking that tags chunks with their parent resume section.
    """
    if not text:
        return []

    lines = text.split("\n")
    sections = []
    current_section = "GENERAL"
    current_lines = []

    for line in lines:
        detected = detect_section_header(line)
        if detected:
            if current_lines:
                sections.append((current_section, "\n".join(current_lines)))
                current_lines = []
            current_section = detected
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_section, "\n".join(current_lines)))

    chunks = []
    for sec_title, sec_text in sections:
        sec_text = sec_text.strip()
        if not sec_text:
            continue

        start = 0
        text_length = len(sec_text)
        while start < text_length:
            end = start + chunk_size
            chunk_body = sec_text[start:end].strip()
            if chunk_body:
                chunks.append(f"[Section: {sec_title}] {chunk_body}")
            if end >= text_length:
                break
            start = end - chunk_overlap

    if not chunks:
        # Fallback if section tagging produced nothing
        start = 0
        text_length = len(text)
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(f"[Section: GENERAL] {chunk}")
            if end >= text_length:
                break
            start = end - chunk_overlap

    return chunks