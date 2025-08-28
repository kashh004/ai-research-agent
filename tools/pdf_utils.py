import os
import requests
import fitz  # PyMuPDF
from typing import Dict

os.makedirs("data/pdfs", exist_ok=True)

def download_pdf(url: str, fname: str) -> str:
    path = os.path.join("data/pdfs", fname)
    if not os.path.exists(path):
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    return path

SECTION_KEYS = ["abstract", "introduction", "method", "results", "discussion", "conclusion", "limitations"]

def extract_text_sections(pdf_path: str) -> Dict[str, str]:
    doc = fitz.open(pdf_path)
    full_text = []
    for page in doc:
        full_text.append(page.get_text())
    text = "\n".join(full_text)
    # very naive section splitter; replace with science-parse or patterns
    sections = {k: "" for k in SECTION_KEYS}
    lower = text.lower()
    for i, key in enumerate(SECTION_KEYS):
        idx = lower.find(key)
        if idx == -1:
            continue
        end = len(text)
        for j in range(i+1, len(SECTION_KEYS)):
            nxt = lower.find(SECTION_KEYS[j])
            if nxt != -1:
                end = min(end, nxt)
        sections[key] = text[idx:end].strip()
    sections["full_text"] = text
    return sections
