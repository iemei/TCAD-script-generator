
import fitz

def load_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join(page.get_text() for page in doc)

def load_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks
