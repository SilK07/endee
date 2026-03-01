from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag import chat
from fastapi.middleware.cors import CORSMiddleware
from rag import process_uploaded_file

app = FastAPI(title="Endee Agentic Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return chat(request.message)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await process_uploaded_file(file)
    return result
