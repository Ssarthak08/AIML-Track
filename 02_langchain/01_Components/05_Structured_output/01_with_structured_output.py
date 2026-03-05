# Typed Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model='models/gemini-2.5-flash',
    temperature=0.5
)