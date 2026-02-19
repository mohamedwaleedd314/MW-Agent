import fitz
from docx import Document

stored_chunks = []

def extract_pdf_text(file_path):
    pdf_doc = fitz.open(file_path)
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text

def extract_docx_text(file_path):
    word_doc = Document(file_path)
    return "\n".join([p.text for p in word_doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)
    else:
        raise ValueError("Unsupported file format")

def split_text(text, chunk_size=2000):
    """Split large texts into smaller chunks"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def process_uploads(files):
    """
    Upload files, split them into smaller chunks and store them in memory
    """
    global stored_chunks
    previews = []
    for f in files:
        try:
            text = extract_text(f.name)
            chunks = split_text(text)
            for chunk in chunks:
                formatted_chunk = f"--- {f.name} ---\n{chunk}"
                stored_chunks.append(formatted_chunk)
            previews.append(f"--- {f.name} ---\n{text[:1000]}...")
        except Exception as e:
            previews.append(f"Error in {f.name}: {str(e)}")
    return "\n\n".join(previews)
