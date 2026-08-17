from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text.strip()
        })

    return pages


def split_text(text, chunk_size=500, overlap=100):

    #Split text into smaller chunks.then check the answer 

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def load_documents(documents_folder: str):
    documents = []

    folder = Path(documents_folder)

    for pdf_file in folder.glob("*.pdf"):

        pages = extract_text_from_pdf(str(pdf_file))

        for page in pages:

            chunks = split_text(page["text"])

            for chunk_index, chunk in enumerate(chunks):

                documents.append({
                    "document_name": pdf_file.name,
                    "page": page["page"],
                    "chunk_id": chunk_index,
                    "text": chunk
                })

    return documents