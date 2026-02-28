from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator_code import run_code_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    problem: str
    language: str

@app.post("/generate")
def generate_code(request: CodeRequest):
    return run_code_pipeline(
        problem=request.problem,
        language=request.language
    )
