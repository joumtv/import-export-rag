# Import-Export Regulation AI

## Project Overview

Import-Export Regulation AI is a document-based question-answering system for import-export regulations.

The system uses Retrieval-Augmented Generation (RAG) to search relevant information from PDF documents. 
The retrieved content is then used by an AI model to generate an answer.

The AI is instructed to answer only based on the retrieved document context. 
If the information is not sufficient, the system returns `HUMAN_REVIEW_REQUIRED`.

---

# 1. How to Run the Project

## Clone the Repository

git clone https://github.com/joumtv/import-export-rag
cd import-export-rag

## Run the Backend

Go to the backend folder:

cd backend

Activate the virtual environment:

**macOS/Linux:**

source venv/bin/activate

Install the required packages if needed:

pip install fastapi uvicorn sqlalchemy python-dotenv openai

Create a `.env` file inside the `backend` folder:

OPENROUTER_API_KEY=your_api_key_here

Start the backend:

uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000

## Run the Frontend

Open another terminal and go to the frontend folder:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Open the URL shown in the terminal.

---

# 2. What I Chose and Why

## Separate Frontend and Backend

I chose a separate frontend and backend architecture.

  - React is used for the user interface.
  - FastAPI handles API requests, document retrieval, AI communication, confidence evaluation, and database operations.

This makes the system easier to organize and develop.

## RAG for Document-Based Answers

I chose Retrieval-Augmented Generation (RAG) because the system needs to answer questions based on import-export regulation documents.

The process is:

User Question
      ↓
Search Relevant PDF Content
      ↓
Evaluate Confidence
      ↓
AI Generates Answer
      ↓
Answer + Source

The AI receives the retrieved document content and is instructed not to use outside information.

## Confidence Evaluation

I added confidence evaluation to check whether the retrieved document content is sufficiently relevant to the user's question.

The system uses:

* HIGH confidence
* MEDIUM confidence
* LOW confidence

If the evidence is insufficient, the system can return:  HUMAN_REVIEW_REQUIRED

This helps reduce unreliable answers.

## Database Instead of In-Memory Storage

I chose SQLite with SQLAlchemy to store question history.

The database stores:

* Question
* Answer
* Confidence score
* Confidence level
* Status
* Creation time

Using a database means the history remains available after restarting the application.

## AI Integration

The project uses the OpenAI Python SDK with OpenRouter to connect to an AI model.

The AI is responsible for generating answers based only on the retrieved document context.

---

# 3. What Already Existed

The original project already included:

* Basic project structure
* Frontend and backend setup
* Import-export regulation PDF documents
* Basic document processing and retrieval
* Basic RAG workflow

---

# 4. What I Built and Improved

I implemented and improved:

* AI answer generation using retrieved document content
* OpenRouter API integration
* Strict prompts to ensure answers are based only on the documents
* Answer abstention when the information is insufficient
* Confidence evaluation
* HIGH, MEDIUM, and LOW confidence handling
* Source document and page display
* SQLite database integration
* SQLAlchemy database models
* Question and answer history storage
* `/history` API endpoint
* Question history display on the frontend
* Improved frontend display for answers, confidence, sources, and status

---

# System Architecture

User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
Document Retrieval (RAG)
  ↓
Confidence Evaluation
  ↓
AI Answer Generation
  ↓
Answer + Sources
  ↓
SQLite Database
Question History

# Author

Mitthavong Benjouly

Software Engineering Student
Ton Duc Thang University
