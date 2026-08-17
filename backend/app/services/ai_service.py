import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, search_results: list):

    context = ""

    for i, result in enumerate(search_results, start=1):
        context += f"""
[SOURCE {i}]
Document: {result['document_name']}
Page: {result['page']}

Content:
{result['text']}

--------------------
"""

    prompt = f"""
You are an AI assistant for import-export regulations.

Answer the user's question using ONLY the retrieved document context.

STRICT RULES:

1. Do NOT use outside knowledge.
2. Do NOT invent facts.
3. Only use information supported by the context.
4. If the context does not contain enough information, respond exactly:
"I could not find enough information in the provided documents to answer this question."

USER QUESTION:
{question}

RETRIEVED DOCUMENT CONTEXT:
{context}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return {
            "success": True,
            "answer": response.text,
            "error": None
        }

    except Exception as e:

        error_message = str(e)

        return {
            "success": False,
            "answer": None,
            "error": error_message
        }