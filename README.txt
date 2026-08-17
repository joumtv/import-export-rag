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

Demo question (English - vietnamese)
-------------
1. What are Members encouraged to use as a basis for import, export, or transit formalities and procedures?
expectation answer: 
    Members are encouraged to use relevant international standards or parts thereof as a basis for their import, export, or transit formalities and procedures.

2. What responsibilities does each Member have regarding cooperation and coordination among border control authorities and agencies?
expectation answer:
    Each Member shall ensure that its authorities and agencies responsible for border controls and procedures related to the importation, 
    exportation, and transit of goods cooperate with one another and coordinate their activities to facilitate trade. Additionally, they shall, 
    to the extent possible and practicable, cooperate on mutually agreed terms with other Members sharing a common border to coordinate procedures at border crossings. 
    This may include alignment of working days and hours, alignment of procedures and formalities, development and sharing of common facilities, and joint controls.

3. What does the Agreement say about cooperation between border control authorities?
expectation answer:
    The Agreement states that each Member shall ensure cooperation and coordination among their authorities and agencies responsible for border controls to facilitate trade. 
    Additionally, Members are encouraged to cooperate on mutually agreed terms with neighboring Members to coordinate border crossing procedures. 
    This cooperation may include aligning working days and hours, procedures and formalities, developing common facilities, and conducting joint controls.

4. Người khai hải quan có những quyền và nghĩa vụ gì theo quy định của Luật Hải quan?
expectation answer:
    Người khai hải quan có những quyền và nghĩa vụ sau theo quy định của Luật Hải quan: 
    Nghĩa vụ:
    1. Khai hải quan và làm thủ tục hải quan theo quy định.
    2. Cung cấp đầy đủ, chính xác thông tin để cơ quan hải quan thực hiện xác định trước mã số, xuất xứ, trị giá hải quan đối với hàng hóa.
    3. Chịu trách nhiệm trước pháp luật về sự xác thực của nội dung đã khai và các chứng từ đã nộp, xuất trình.
    Quyền hạn không được đề cập trong các tài liệu được cung cấp.

5. Cơ quan hải quan có trách nhiệm và quyền hạn gì trong việc thu thập và cung cấp thông tin hải quan?
expectation answer:
    Cơ quan hải quan có trách nhiệm thu thập thông tin từ các nguồn như hoạt động nghiệp vụ hải quan và bộ, cơ quan ngang bộ có liên quan. 
    Đồng thời, tổ chức, cá nhân cũng có quyền yêu cầu cơ quan hải quan cung cấp thông tin liên quan đến quyền, nghĩa vụ của mình. 
    Các bên liên quan đến hoạt động xuất khẩu, nhập khẩu cũng có trách nhiệm cung cấp thông tin cho cơ quan hải quan theo quy định của pháp luật.

# Author

Mitthavong Benjouly

Software Engineering Student
Ton Duc Thang University
