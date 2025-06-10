# File: src/core/parsing.py
import pdfplumber
from typing import List, Dict, Any, Tuple

def parse_cvs(uploaded_files: List[Any]) -> Tuple[List[Dict[str, str]], List[str]]:
    cv_texts, errors = [], []
    for file in uploaded_files:
        try:
            with pdfplumber.open(file) as pdf:
                text = "".join([p.extract_text() or "" for p in pdf.pages if p.extract_text()])
            if text.strip(): cv_texts.append({"filename": file.name, "text": text})
        except Exception as e:
            errors.append(f"Gagal memproses file '{file.name}': {e}")
    return cv_texts, errors