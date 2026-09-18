from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DIR = BASE_DIR / "data" / "processed" / "chroma_db"

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")

print("\nConnecting to ChromaDB...")
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_collection(name="daaruka_knowledge")

print(f"Knowledge base contains {collection.count()} chunks.")

question = input("\nAsk Daaruka.Earth a question: ")

print("\nSearching scientific knowledge...")

question_embedding = model.encode(question).tolist()

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=5
)

print("\n===================================")
print("RETRIEVED SCIENTIFIC KNOWLEDGE")
print("===================================\n")

for i in range(len(results["documents"][0])):

    document = results["documents"][0][i]
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]

    print(f"RESULT {i + 1}")
    print("-" * 60)

    print(f"Source: {metadata['source']}")
    print(f"Page: {metadata['page']}")
    print(f"Chunk ID: {metadata['chunk_id']}")
    print(f"Distance: {distance:.4f}")

    print("\nText:")
    print(document[:1000])

    print("\n")