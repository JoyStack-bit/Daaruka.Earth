from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found in .env")


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

CHROMA_DIR = BASE_DIR / "data" / "processed" / "chroma_db"


# --------------------------------------------------
# OPENAI CLIENT
# --------------------------------------------------

client = OpenAI(api_key=api_key)


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


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

print(f"Knowledge base contains {collection.count()} chunks.")


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

question = input("\nAsk Daaruka.Earth a question: ")

print("\nSearching scientific knowledge...")

question_embedding = embedding_model.encode(question).tolist()


# --------------------------------------------------
# RETRIEVE RELEVANT CHUNKS
# --------------------------------------------------

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=5
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]


# --------------------------------------------------
# BUILD SCIENTIFIC CONTEXT
# --------------------------------------------------

context_parts = []

for i, document in enumerate(documents):

    source = metadatas[i]["source"]
    chunk_id = metadatas[i]["chunk_id"]

    context_parts.append(
        f"""
SOURCE: {source}
CHUNK: {chunk_id}

{document}
"""
    )


context = "\n".join(context_parts)


# --------------------------------------------------
# SYSTEM INSTRUCTIONS
# --------------------------------------------------

system_prompt = """
You are Daaruka.Earth, a scientific environmental knowledge assistant.

Answer the user's question using the scientific context provided below.

Rules:

1. Use the provided scientific context as the primary source of evidence.
2. Do not invent scientific facts that are not supported by the context.
3. If the context does not contain enough information to answer confidently,
   say that the available sources do not provide enough information.
4. Give a clear and understandable answer.
5. Explain scientific relationships rather than simply copying the source.
6. At the end, provide a "Sources" section listing the source documents used.
7. Do not claim that a source says something unless it is actually present
   in the retrieved context.
"""


# --------------------------------------------------
# SEND TO OPENAI
# --------------------------------------------------

print("\nGenerating answer...\n")

response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=system_prompt,
    input=f"""
Scientific context:

{context}


User question:

{question}
"""
)


# --------------------------------------------------
# DISPLAY ANSWER
# --------------------------------------------------

print("===================================")
print("DAARUKA.EARTH")
print("===================================\n")

print(response.output_text)

print("\n===================================")