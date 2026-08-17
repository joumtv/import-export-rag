from fastapi import FastAPI

from app.services.document_service import load_documents
from app.services.rag_service import search_documents
from app.services.ai_service import generate_answer
from app.services.confidence_service import evaluate_confidence

from app.database import engine, Base, SessionLocal
from app import models
from app.models import QuestionHistory


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Import-Export Regulation AI",
    description="RAG system for import-export regulations"
)


@app.get("/")
def root():
    return {
        "message": "Import-Export RAG API is running!"
    }


@app.get("/documents")
def get_documents():

    documents = load_documents("../documents")

    return {
        "total_chunks": len(documents),
        "documents": documents
    }


@app.get("/search")
def search(question: str):

    results = search_documents(question)

    return {
        "question": question,
        "results": results
    }


@app.get("/ask")
def ask(question: str):

    # Step 1: Search relevant document chunks
    results = search_documents(question)

    # Step 2: Evaluate confidence
    confidence = evaluate_confidence(results)

    # Default values
    answer = None
    sources = []

    # Step 3: Decide whether to answer
    if not confidence["should_answer"]:

        status = "HUMAN_REVIEW_REQUIRED"

    else:

        # Generate answer using Gemini
        answer = generate_answer(question, results)

        status = "ANSWER_GENERATED"

        # Use the most relevant retrieved source
        best_result = results[0]

        sources = [{
            "document_name": best_result["document_name"],
            "page": best_result["page"],
            "score": round(best_result["score"], 3)
        }]

    # Step 4: Save every request to database
    db = SessionLocal()

    try:
        history = QuestionHistory(
            question=question,
            answer=answer,
            confidence_score=confidence["score"],
            confidence_level=confidence["level"],
            status=status
        )

        db.add(history)
        db.commit()
        db.refresh(history)

    finally:
        db.close()

    # Step 5: Return response
    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "status": status,
        "sources": sources
    }