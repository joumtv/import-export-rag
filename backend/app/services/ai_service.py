import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_answer(question: str, search_results: list):

    try:

        context = ""

        for i, result in enumerate(search_results, start=1):

            context += f"""
[SOURCE {i}]
Document: {result['document_name']}
Page: {result['page']}
Relevance score: {result['score']:.3f}

Content:
{result['text']}

--------------------
"""

        prompt = f"""
You are an AI assistant for import-export regulations.

Answer the user's question using ONLY the retrieved document context below.

STRICT RULES:

1. Do NOT use outside knowledge.
2. Do NOT invent facts, laws, regulations, or requirements.
3. Only use information directly supported by the context.
4. If the context does not contain enough information, respond exactly:

I could not find enough information in the provided documents to answer this question.

5. Do not mention irrelevant sources.
6. Keep the answer clear and concise.

USER QUESTION:
{question}

RETRIEVED DOCUMENT CONTEXT:
{context}
"""

        response = client.chat.completions.create(

            # Change this model if necessary
            model="openai/gpt-4o-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

        return {
            "success": True,
            "answer": answer,
            "error": None
        }

    except Exception as e:

        print(f"AI Service Error: {e}")

        return {
            "success": False,
            "answer": None,
            "error": str(e)
        }