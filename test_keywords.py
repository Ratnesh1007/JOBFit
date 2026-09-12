from src.keyword_extractor import extract_keywords


text = """
We are looking for a Software Engineer with
Python, FastAPI, LangChain, RAG, Docker,
AWS, PostgreSQL and Machine Learning experience.
"""


keywords = extract_keywords(text)


print("\nExtracted Keywords:")
print("=" * 50)

for keyword in keywords:
    print("-", keyword)

print(
    f"\nTotal keywords: {len(keywords)}"
)