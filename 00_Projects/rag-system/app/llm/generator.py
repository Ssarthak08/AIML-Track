import google.generativeai as genai
from typing import List

from app.config import config
from app.schemas.chunk import Chunk


class Generator:

    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def _build_prompt(self, query: str, chunks: List[Chunk]) -> str:
        context = "\n\n".join([chunk.text for chunk in chunks])


        prompt = f"""
You are a helpful AI assistant.

Answer the question ONLY using the provided context.
Do NOT use any external knowledge.

If the answer is not present in the context, say:
"I don't know based on the provided documents."

---------------------
Context:
{context}
---------------------

Question:
{query}

Answer:
"""
        return prompt

    def generate(self, query: str, chunks: List[Chunk]) -> str:
        # 🔥 Build prompt
        prompt = self._build_prompt(query, chunks)

        # 🔥 Call Gemini
        response = self.model.generate_content(prompt)

        return response.text