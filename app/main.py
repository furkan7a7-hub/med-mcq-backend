import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import subjects, topics, questions, quizzes, explanations, import_csv

app = FastAPI(title="Med MCQ Backend (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(subjects.router, prefix="")
app.include_router(topics.router, prefix="")
app.include_router(questions.router, prefix="")
app.include_router(quizzes.router, prefix="")
app.include_router(explanations.router, prefix="")
app.include_router(import_csv.router, prefix="")
