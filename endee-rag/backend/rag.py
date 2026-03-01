from google import genai
from sentence_transformers import SentenceTransformer
from endee import Endee
from duckduckgo_search import DDGS
from config import GEMINI_API_KEY
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