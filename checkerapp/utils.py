from docx import Document
import os
import re

def analyze_document_and_extract_fields(file_path):
    _, ext = os.path.splitext(file_path)
    text = ""

    if ext.lower() == ".pdf":
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])

    elif ext.lower() == ".docx":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    elif ext.lower() in ['.txt', '.eml']:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

    return extract_fields_from_text(text)