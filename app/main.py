from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .routers import subjects, topics, questions, quizzes, explanations 

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
from fastapi.middleware.cors import CORSMiddleware

# السماح للواجهة تتصل من أي مكان (مثل StackBlitz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # تقدر تحدد دومين معين بدال النجمة لو تريد أمان أكثر
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# هذا المسار يخلي السيرفر يجاوب بـ 200 OK بدل التحويل
@app.get("/healthz", include_in_schema=False)
def health_check():
    return {"ok": True}


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

