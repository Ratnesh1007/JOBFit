import re


def clean_text(text):
    """
    Clean extracted text by removing unnecessary
    whitespace and blank lines.
    """

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text