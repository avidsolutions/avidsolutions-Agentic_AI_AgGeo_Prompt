from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptSection(BaseModel):
    section: str
    content: str

@app.get("/")
def health_check():
    return {"status": "OK"}

@app.post("/analyze")
def analyze(data: PromptSection):
    return {
        "section": data.section,
        "word_count": len(data.content.split())
    }