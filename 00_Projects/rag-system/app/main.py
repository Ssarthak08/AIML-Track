from app.ingestion.loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.pinecone_store import PineconeStore
from app.retrieval.retriever import Retriever
from app.llm.generator import Generator


def ingest(file_path: str):
    print("\n[1] Loading document...")
    docs = DocumentLoader.load(file_path)

    print("[2] Chunking document...")
    chunker = DocumentChunker()
    chunks = chunker.split(docs)

    print(f"[3] Generated {len(chunks)} chunks")

    print("[4] Creating embeddings...")
    embedder = Embedder()
    texts = [chunk.text for chunk in chunks]
    embeddings = embedder.embed_batch(texts)

    print("[5] Storing in Pinecone...")
    vectorstore = PineconeStore()
    vectorstore.upsert(chunks, embeddings)

    print("✅ Ingestion complete!\n")


def ask(query: str):
    print("\n[1] Retrieving relevant chunks...")
    retriever = Retriever()
    chunks = retriever.retrieve(query)

    print(f"[2] Retrieved {len(chunks)} chunks")

    print("[3] Generating answer...")
    generator = Generator()
    answer = generator.generate(query, chunks)

    print("\nAnswer:\n")
    print(answer)
    print("\n")


if __name__ == "__main__":
    # 🔥 STEP 1: Ingest (run once per document)
    file_path = "data/raw/sample.pdf"
    ingest(file_path)

    # 🔥 STEP 2: Ask questions
    while True:
        query = input("Ask a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        ask(query)