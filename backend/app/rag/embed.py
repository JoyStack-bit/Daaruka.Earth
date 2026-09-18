from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

CHUNKS_FILE = PROCESSED_DIR / "chunks.json"

CHROMA_DIR = PROCESSED_DIR / "chroma_db"


# --------------------------------------------------
# LOAD CHUNKS
# --------------------------------------------------

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks.")


# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# --------------------------------------------------
# CREATE / CONNECT TO CHROMADB
# --------------------------------------------------

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# --------------------------------------------------
# REMOVE OLD COLLECTION
# --------------------------------------------------

print("Removing old knowledge collection...")

try:
    client.delete_collection(
        name="daaruka_knowledge"
    )

    print("Old collection deleted.")

except Exception:
    print("No existing collection found.")


# --------------------------------------------------
# CREATE FRESH COLLECTION
# --------------------------------------------------

collection = client.create_collection(
    name="daaruka_knowledge"
)

print("Fresh ChromaDB collection created.")


# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

documents = []
metadatas = []
ids = []

for i, chunk in enumerate(chunks):

    documents.append(chunk["text"])

    metadatas.append({
        "source": chunk["source"],
        "page": chunk["page"],
        "chunk_id": chunk["chunk_id"]
    })

    ids.append(f"chunk_{i}")


# --------------------------------------------------
# GENERATE EMBEDDINGS
# --------------------------------------------------

print(
    f"\nGenerating embeddings for "
    f"{len(documents)} chunks..."
)

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

print("Embeddings generated.")


# --------------------------------------------------
# STORE EMBEDDINGS IN BATCHES
# --------------------------------------------------

print("\nStoring embeddings in ChromaDB...")

BATCH_SIZE = 5000

for start in range(
    0,
    len(documents),
    BATCH_SIZE
):

    end = start + BATCH_SIZE

    collection.add(
        ids=ids[start:end],
        documents=documents[start:end],
        embeddings=embeddings[start:end].tolist(),
        metadatas=metadatas[start:end]
    )

    print(
        f"Stored chunks "
        f"{start} to {min(end, len(documents))}"
    )


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n===================================")
print("RAG KNOWLEDGE BASE REBUILT")
print("===================================")

print(
    f"Documents stored: "
    f"{collection.count()}"
)

print(
    f"Database location: "
    f"{CHROMA_DIR}"
)