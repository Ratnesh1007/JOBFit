import re
import json
import ollama


MODEL_NAME = "llama3.2:3b"


# ============================================================
# KEYWORD ALIASES
# ============================================================

KEYWORD_ALIASES = {

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "dl": "deep learning",
    "deep-learning": "deep learning",

    "ai": "artificial intelligence",

    "genai": "generative ai",
    "gen ai": "generative ai",

    "llm": "large language model",
    "llms": "large language model",

    "nlp": "natural language processing",

    "cv": "computer vision",

    "js": "javascript",
    "javascript": "javascript",

    "ts": "typescript",
    "typescript": "typescript",

    "py": "python",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "mongo": "mongodb",
    "mongodb": "mongodb",

    "k8s": "kubernetes",

    "restful api": "rest api",
    "restful apis": "rest api",
    "rest api": "rest api",
    "rest apis": "rest api",

    "rag": "retrieval augmented generation",

    "vector db": "vector database",
    "vector databases": "vector database",
    "vector database": "vector database",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    "tf": "tensorflow",

    "np": "numpy",

    "pd": "pandas",

    "github": "github",
    "git hub": "github"
}


# ============================================================
# COMMON TECHNICAL KEYWORDS
# ============================================================

COMMON_KEYWORDS = [

    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "C",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "SQLite",
    "Redis",

    "Database",
    "Relational Database",

    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Computer Vision",

    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",

    "Generative AI",
    "Large Language Model",
    "Retrieval Augmented Generation",
    "LangChain",
    "LangGraph",
    "Vector Database",
    "FAISS",
    "Embeddings",
    "Sentence Transformers",

    "HTML",
    "CSS",
    "React",
    "Angular",
    "Node.js",
    "Express",
    "Flask",
    "Django",
    "FastAPI",
    "Spring",
    "Spring Boot",

    "REST API",
    "API",
    "Microservices",

    "Docker",
    "Kubernetes",
    "Jenkins",
    "Terraform",
    "Ansible",

    "AWS",
    "Azure",
    "GCP",
    "Google Cloud",
    "Cloud",

    "Linux",

    "Git",
    "GitHub",
    "GitLab",
    "Bitbucket",

    "Postman",
    "Jira",

    "Data Analysis",
    "Data Science",
    "Data Visualization",

    "Power BI",
    "Tableau",
    "Excel",

    "Object-Oriented Programming",
    "OOP",

    "Agile",
    "Scrum"
]


# ============================================================
# NORMALIZE KEYWORD
# ============================================================

def normalize_keyword(keyword):

    keyword = keyword.lower().strip()

    keyword = re.sub(
        r"\s+",
        " ",
        keyword
    )

    keyword = KEYWORD_ALIASES.get(
        keyword,
        keyword
    )

    return keyword


# ============================================================
# RULE-BASED KEYWORD EXTRACTION
# ============================================================

def extract_rule_based_keywords(text):

    text_lower = text.lower()

    found_keywords = []

    all_search_terms = list(COMMON_KEYWORDS) + list(KEYWORD_ALIASES.keys())

    # Sort by length so multi-word keywords
    # are detected before shorter ones.
    sorted_keywords = sorted(
        set(all_search_terms),
        key=len,
        reverse=True
    )

    for keyword in sorted_keywords:

        pattern = r"(?<!\w)" + re.escape(
            keyword.lower()
        ) + r"(?!\w)"

        if re.search(
            pattern,
            text_lower
        ):

            normalized = normalize_keyword(
                keyword
            )

            if normalized not in found_keywords:
                found_keywords.append(
                    normalized
                )

    return found_keywords


# ============================================================
# LLM KEYWORD EXTRACTION
# ============================================================

def extract_llm_keywords(text):

    system_prompt = """
You are a keyword extraction system for JOBFit,
an AI resume screening application.

Extract important technical skills, tools,
frameworks, programming languages, databases,
cloud platforms, certifications, methodologies,
and important domain-specific terms.

Rules:

1. Extract only keywords explicitly present
   in the provided text.

2. Do not invent skills.

3. Do not explain the keywords.

4. Return ONLY valid JSON.

Required format:

{
    "keywords": [
        "Python",
        "Machine Learning",
        "FastAPI"
    ]
}
"""

    user_prompt = f"""
Extract important job/resume keywords from
the following text:

{text}

Return ONLY valid JSON.
"""

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
                "num_predict": 500
            },
            keep_alive="10m"
        )

        response_text = (
            response["message"]["content"]
        )

        result = json.loads(
            response_text
        )

        keywords = result.get(
            "keywords",
            []
        )

        if not isinstance(
            keywords,
            list
        ):
            return []

        normalized_keywords = []

        for keyword in keywords:

            if not isinstance(
                keyword,
                str
            ):
                continue

            normalized = normalize_keyword(
                keyword
            )

            if normalized:
                normalized_keywords.append(
                    normalized
                )

        return normalized_keywords

    except Exception as error:

        print(
            f"LLM keyword extraction error: {error}"
        )

        return []


# ============================================================
# COMBINED KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text, use_llm=False):

    rule_keywords = (
        extract_rule_based_keywords(text)
    )

    llm_keywords = []
    if use_llm:
        llm_keywords = extract_llm_keywords(text)

    combined = []

    for keyword in (
        rule_keywords + llm_keywords
    ):

        normalized = normalize_keyword(
            keyword
        )

        if normalized not in combined:

            combined.append(
                normalized
            )

    return combined