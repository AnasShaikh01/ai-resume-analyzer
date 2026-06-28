import os
import re
from collections import Counter
from io import BytesIO
import docx
import fitz  # PyMuPDF

# ==========================================================
# Text Extraction
# ==========================================================

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """
    Extract text from PDF, DOCX or TXT while preserving layout.
    """
    ext = os.path.splitext(filename)[-1].lower()
    text = ""
    if ext == ".pdf":
        doc = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )
        for page in doc:
            blocks = page.get_text("blocks")
            # Top-to-bottom then left-to-right
            blocks = sorted(
                blocks,
                key=lambda b: (b[1], b[0])
            )
            for block in blocks:
                block_text = block[4].strip()
                if block_text:
                    text += block_text + "\n"
            text += "\n"
        doc.close()

    elif ext == ".docx":
        document = docx.Document(
            BytesIO(file_bytes)
        )
        for para in document.paragraphs:
            if para.text.strip():
                text += para.text.strip() + "\n"
    elif ext == ".txt":
        text = file_bytes.decode(
            "utf-8",
            errors="ignore"
        )
    else:
        raise ValueError(
            f"Unsupported file type: {ext}"
        )
    return text.strip()

# ==========================================================
# Header / Footer Removal
# ==========================================================

PAGE_REGEX = re.compile(
    r"page\s*\d+(\s*of\s*\d+)?",
    re.IGNORECASE
)

def remove_headers_footers(
    text,
    repeat_threshold=2
):
    """
    Remove repeated headers / footers while
    preserving document structure.
    """
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]
    counts = Counter(lines)
    repeated = {
        line
        for line, count in counts.items()
        if (
            count >= repeat_threshold
            and len(line) < 120
        )
    }

    cleaned = [
        line
        for line in lines
        if (
            line not in repeated
            and not PAGE_REGEX.search(line)
        )
    ]
    return "\n".join(cleaned)

# ==========================================================
# Resume Preprocessing
# ==========================================================

def preprocess_resume(text):
    """
    Preserve line breaks because
    Resume Section Parser depends on them.
    """
    text = remove_headers_footers(text)

    text = re.sub(
        r"[^\w\s,.\-+#/&\n]",
        " ",
        text
    )
    # Collapse spaces only
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )
    # Preserve newlines
    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )
    return text.strip().lower()

# ==========================================================
# JD Preprocessing
# ==========================================================

def preprocess_jd(text):
    """
    JDs don't require formatting.
    Convert into a clean paragraph.
    """
    text = re.sub(
        r"[^\w\s,.\-+#/&]",
        " ",
        text
    )
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    return text.strip().lower()

# ==========================================================
# Backward Compatibility
# ==========================================================

def preprocess(text):
    """
    Temporary wrapper.
    Existing code continues working.
    Later we'll replace all calls with:
        preprocess_resume()
        preprocess_jd()
    """
    return preprocess_resume(text)