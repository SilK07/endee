from google import genai
from sentence_transformers import SentenceTransformer
from endee import Endee
from ddgs import DDGS
from config import GEMINI_API_KEY
import uuid
from pypdf import PdfReader
from docx import Document
import uuid

client_gemini = genai.Client(api_key=GEMINI_API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")

client = Endee()

DOC_INDEX = client.get_index("rag_index")
MEMORY_INDEX = client.get_index("chat_memory")


def get_embedding(text):
    return model.encode(text).tolist()


def retrieve_docs(query, top_k=3):
    results = DOC_INDEX.query(vector=get_embedding(query), top_k=top_k)

    context = []
    for item in results:
        context.append(item["meta"]["text"])

    return "\n".join(context)


def retrieve_memory(query, top_k=3):
    results = MEMORY_INDEX.query(vector=get_embedding(query), top_k=top_k)

    memory = []
    for item in results:
        memory.append(item["meta"]["conversation"])

    return "\n".join(memory)


def store_memory(user_msg, bot_response):
    MEMORY_INDEX.upsert([
        {
            "id": str(uuid.uuid4()),
            "vector": get_embedding(user_msg + " " + bot_response),
            "meta": {
                "conversation": f"User: {user_msg}\nBot: {bot_response}"
            }
        }
    ])

def web_search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join([r["body"] for r in results])


def chat(query):
    doc_context = retrieve_docs(query)
    past_memory = retrieve_memory(query)

    prompt = f"""
You are an AI assistant with long-term memory.

Past Conversation:
{past_memory}

Relevant Knowledge:
{doc_context}

User Question:
{query}

Answer clearly and concisely.
"""

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    answer = response.text

    store_memory(query, answer)

    return {
        "answer": answer
    }


async def process_uploaded_file(file):
    content = ""

    if file.filename.endswith(".txt"):
        content = (await file.read()).decode("utf-8")

    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            content += page.extract_text() or ""

    elif file.filename.endswith(".docx"):
        doc = Document(file.file)
        for para in doc.paragraphs:
            content += para.text + "\n"

    else:
        return {"error": "Unsupported file type"}

    # Chunk text
    words = content.split()
    chunks = [
        " ".join(words[i:i+200])
        for i in range(0, len(words), 200)
    ]

    vectors = []

    for chunk in chunks:
        vectors.append({
            "id": str(uuid.uuid4()),
            "vector": get_embedding(chunk),
            "meta": {
                "text": chunk,
                "source": file.filename
            }
        })

    DOC_INDEX.upsert(vectors)

    return {
        "message": f"{file.filename} uploaded and indexed successfully!",
        "chunks_added": len(chunks)
    }