import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")

    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "rag-index")

    GEMINI_MODEL: str = "gemini-2.5-flash"

    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 100))

    TOP_K: int = int(os.getenv("TOP_K", 5))


config = Config()