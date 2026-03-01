from fastapi import FastAPI
from pydantic import BaseModel
from rag import chat

app = FastAPI(title="Endee Agentic Chat")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return chat(request.message)