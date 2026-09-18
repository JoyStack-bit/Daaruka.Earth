# Daaruka.Earth 🌍

**AI-Powered Environmental Intelligence using Retrieval-Augmented Generation (RAG)**

Daaruka.Earth is an AI-powered environmental intelligence platform that answers questions related to **biodiversity, soil, forests, water, climate, and human impact** using trusted scientific sources.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from environmental documents and generate grounded answers with **source and page-level citations**.

---

## 🚀 Features

- AI-powered environmental question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- ChromaDB vector database
- OpenAI-powered answer generation
- Page-level source citations
- React-based interactive chat interface
- FastAPI backend
- Covers multiple environmental domains

---

## 🏗️ Architecture

```text
User
  ↓
React + Vite Frontend
  ↓
FastAPI Backend
  ↓
Sentence Transformer Embeddings
  ↓
ChromaDB Vector Database
  ↓
Relevant Document Chunks
  ↓
OpenAI
  ↓
Grounded Answer + Source Citations
  ↓
React UI

## 🛠️ Tech Stack

### Frontend
- **React** — User interface
- **Vite** — Frontend development and build tool
- **JavaScript**
- **CSS**

### Backend
- **Python**
- **FastAPI** — REST API
- **Uvicorn** — ASGI server

### AI & RAG
- **OpenAI** — AI answer generation
- **Sentence Transformers** — Text embeddings
- **ChromaDB** — Vector database
- **PyPDF** — PDF text extraction

📂 Project Structure
Daaruka.Earth/
├── backend/
│   └── app/
│       ├── main.py
│       └── rag/
│           ├── ingest.py
│           ├── embed.py
│           ├── retrieve.py
│           ├── rag_answer.py
│           └── rag_service.py
│
├── data/
│   ├── documents/
│   └── processed/
│       └── chunks.json
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md

⚙️ Setup
1. Clone the repository
git clone https://github.com/JoyStack-bit/Daaruka.Earth.git
cd Daaruka.Earth

2. Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn pypdf sentence-transformers chromadb openai python-dotenv

Create:
backend/.env

Add:
OPENAI_API_KEY=your_api_key_here
Never commit the API key to GitHub.

3. Add source documents
Place the required environmental PDF documents inside:
data/documents/
The PDFs used during development include sources from organizations such as FAO, IPBES, and IPCC.

4. Start the backend
From the backend directory:
uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

5. Start the frontend
Open another terminal:
cd frontend
npm install
npm run dev

Frontend:
http://localhost:5173


🧠 RAG Pipeline
Environmental PDFs are processed page-by-page.
Documents are split into searchable chunks.
Sentence Transformer generates embeddings.
Embeddings are stored in ChromaDB.
A user's question is converted into an embedding.
Relevant document chunks are retrieved.
Retrieved context is provided to the OpenAI model.
The system generates a grounded environmental answer.
Sources are displayed with document name and page number.


🎯 Project Goal
The goal of Daaruka.Earth is to make reliable environmental knowledge more accessible through an AI interface while maintaining traceability to the underlying scientific sources.


🔮 Future Improvements
Expand the environmental knowledge base
Add more scientific and government datasets
Improve retrieval and ranking
Add multilingual support
Add environmental data visualizations
Integrate real-time environmental datasets
Deploy the platform to the cloud


👨‍💻 Author
Swayam Bhaskar
B.Tech — Electronics and Computer Science