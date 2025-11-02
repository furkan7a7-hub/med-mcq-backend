from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .routers import subjects, topics, questions, quizzes, explanations, import_csv

app = FastAPI(
    title="MedMCQ API",
    description="Backend API for MedMCQ platform",
    version="1.0.0"
)

# Allow all origins (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root URL to /docs
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Routers
app.include_router(subjects.router)
app.include_router(topics.router)
app.include_router(questions.router)
app.include_router(quizzes.router)
app.include_router(explanations.router)
app.include_router(import_csv.router)

