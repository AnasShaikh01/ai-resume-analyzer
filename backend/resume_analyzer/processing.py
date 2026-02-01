import os
import re
from collections import Counter
from io import BytesIO

import docx
import fitz  # PyMuPDF


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """
    Extract text from resume file given raw bytes + filename.
    Supports PDF, DOCX, TXT.
    """
    ext = os.path.splitext(filename)[-1].lower()
    text = ""

    if ext == ".pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()

    elif ext == ".docx":
        doc = docx.Document(BytesIO(file_bytes)) # Use BytesIO for in-memory files
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext == ".txt":
        text = file_bytes.decode("utf-8", errors="ignore")

    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return text.strip()


PAGE_REGEX = re.compile(r'page\s*\d+(\s*of\s*\d+)?', re.I)

def remove_headers_footers(text, min_len=5, repeat_threshold=2):
    """
    Removes repeated short lines (likely headers/footers)
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    cnt = Counter(lines)
    repeated = {l for l, c in cnt.items() if c >= repeat_threshold and len(l) < 120}
    filtered = [l for l in lines if l not in repeated and not PAGE_REGEX.search(l)]
    return "\n".join(filtered)

def normalize_text(text):
    """
    Remove unwanted symbols and normalize whitespace
    """
    # Keep letters, numbers, comma, dot, dash, plus (# for C# etc.)
    text = re.sub(r"[^a-zA-Z0-9\s,.\-+#/&]", " ", text)
    text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
    return text.strip()

def preprocess(text):
    """
    Full preprocessing pipeline:
    - Remove headers/footers
    - Clean symbols
    - Lowercase
    """
    text = remove_headers_footers(text)
    text = normalize_text(text)
    return text.lower()