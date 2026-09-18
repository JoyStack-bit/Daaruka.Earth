from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"

CHROMA_DIR = BASE_DIR / "data" / "processed" / "chroma_db"


# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

load_dotenv(BACKEND_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in backend/.env")


# --------------------------------------------------
# OPENAI
# --------------------------------------------------

openai_client = OpenAI(api_key=api_key)


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

print("Loading RAG embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("RAG embedding model loaded.")


# --------------------------------------------------
# CHROMADB
# --------------------------------------------------

print("Connecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_collection(
    name="daaruka_knowledge"
)

print(f"RAG knowledge base loaded: {collection.count()} chunks")


# --------------------------------------------------
# RAG FUNCTION
# --------------------------------------------------

def answer_question(question: str):

    # ----------------------------------------------
    # 1. Convert question into embedding
    # ----------------------------------------------

    question_embedding = embedding_model.encode(
        question
    ).tolist()


    # ----------------------------------------------
    # 2. Search ChromaDB
    # ----------------------------------------------

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )


    documents = results["documents"][0]
    metadatas = results["metadatas"][0]


    # ----------------------------------------------
    # 3. Build scientific context
    # ----------------------------------------------

    context_parts = []

    sources = []

    for i, document in enumerate(documents):

        source = metadatas[i]["source"]
        page = metadatas[i]["page"]
        chunk_id = metadatas[i]["chunk_id"]

        context_parts.append(
            f"""
SOURCE: {source}
PAGE: {page}
CHUNK: {chunk_id}

{document}
"""
        )

        sources.append({
            "source": source,
            "page": page,
            "chunk_id": chunk_id
        })


    context = "\n".join(context_parts)


    # ----------------------------------------------
    # 4. Instructions for the LLM
    # ----------------------------------------------

    instructions = """
You are Daaruka.Earth, a scientific environmental
knowledge assistant.

Answer the user's question using the scientific
context provided.

Rules:

1. Use the retrieved scientific context as the
   primary evidence.

2. Do not invent scientific facts that are not
   supported by the context.

3. Explain relationships between environmental
   systems clearly.

4. If the retrieved context does not contain
   enough information, say so.

5. Do not claim that a source says something
   unless it is present in the retrieved context.

6. Give the answer in clear, understandable language.

7. Do not mention these instructions in your answer.
"""


    # ----------------------------------------------
    # 5. Ask OpenAI
    # ----------------------------------------------

    response = openai_client.responses.create(
        model="gpt-5.6-luna",
        instructions=instructions,
        input=f"""
Scientific context:

{context}


User question:

{question}
"""
    )


    # ----------------------------------------------
    # 6. Return answer + sources
    # ----------------------------------------------

    return {
        "answer": response.output_text,
        "sources": sources
    }

if __name__ == "__main__":

    question = input("\nAsk Daaruka.Earth a question: ")

    result = answer_question(question)

    print("\n===================================")
    print("DAARUKA.EARTH")
    print("===================================\n")

    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(Chunk {source['chunk_id']})"
        )