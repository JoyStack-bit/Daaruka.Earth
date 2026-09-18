from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag.rag_service import answer_question


app = FastAPI(
    title="Daarukaa.Earth Biodiversity Intelligence API",
    description="AI-powered environmental intelligence system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Daarukaa.Earth AI Environmental Scientist API",
        "status": "running"
    }


# --------------------------------------------------
# RAG QUESTION ENDPOINT
# --------------------------------------------------

@app.post("/api/ask")
def ask_question(request: QuestionRequest):

    result = answer_question(request.question)

    return result