from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running", "manager": "uv", "server": "uvicorn"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/ask")
def ask(question: str):
    return {f"{question}": "answer"}