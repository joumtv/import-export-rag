from sentence_transformers import SentenceTransformer
from app.services.document_service import load_documents
import numpy as np


# Load AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def search_documents(
    question,
    documents_folder="../documents",
    top_k=3,
    min_score=0.30
):

    # Load all document chunks
    documents = load_documents(documents_folder)

    if not documents:
        return []

    # Extract text
    texts = [doc["text"] for doc in documents]

    # Create embeddings
    question_embedding = model.encode(question)
    document_embeddings = model.encode(texts)

    results = []

    for i, document in enumerate(documents):

        score = cosine_similarity(
            question_embedding,
            document_embeddings[i]
        )

        # Only keep sufficiently relevant chunks
        if score >= min_score:
            results.append({
                **document,
                "score": float(score)
            })

    # Sort highest score first
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]