from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.document_service import load_documents
from app.services.rag_service import search_documents
from app.services.ai_service import generate_answer
from app.services.confidence_service import evaluate_confidence

from app.database import engine, Base, SessionLocal
from app.models import QuestionHistory


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Import-Export Regulation AI",
    description="RAG system for import-export regulations"
)


# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    #Search relevant document chunks
    results = search_documents(question)

    # valuate retrieval confidence
    confidence = evaluate_confidence(results)

    answer = None
    sources = []
    status = "HUMAN_REVIEW_REQUIRED"

    # Only call AI if retrieval confidence is sufficient
    if confidence["should_answer"]:

        # Generate answer
        ai_result = generate_answer(question, results)

        # Handle AI service error
        if not ai_result["success"]:

            status = "AI_SERVICE_UNAVAILABLE"

            return {
                "question": question,
                "answer": None,
                "confidence": confidence,
                "status": status,
                "sources": [],
                "error": ai_result["error"]
            }

        answer = ai_result["answer"]

        abstain_message = (
            "I could not find enough information in the provided "
            "documents to answer this question."
        )

        # check whether AI abstained
        if abstain_message.lower() in answer.lower():

            answer = None

            confidence = {
                "level": "LOW",
                "should_answer": False,
                "score": confidence["score"],
                "message": (
                    "Relevant text was retrieved, but the evidence "
                    "was not sufficient to answer the question reliably."
                )
            }

            status = "HUMAN_REVIEW_REQUIRED"

        else:

            # Answer successfully generated
            status = "ANSWER_GENERATED"

            best_result = results[0]

            sources = [{
                "document_name": best_result["document_name"],
                "page": best_result["page"],
                "score": round(best_result["score"], 3)
            }]

    # Save to database
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

    # Return response
    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "status": status,
        "sources": sources
    }

@app.get("/history")
def get_history():

    db = SessionLocal()

    try:
        history = (
            db.query(QuestionHistory)
            .order_by(QuestionHistory.created_at.desc())
            .all()
        )

        return [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "confidence_score": item.confidence_score,
                "confidence_level": item.confidence_level,
                "status": item.status,
                "created_at": item.created_at
            }
            for item in history
        ]

    finally:
        db.close()