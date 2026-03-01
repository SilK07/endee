
# Endee Agentic RAG Chat

  

A full-stack Retrieval-Augmented Generation (RAG) system built using:

  

-  **Endee** (High-performance vector database)

-  **Gemini LLM**

-  **SentenceTransformers (MiniLM 384-d embeddings)**

-  **FastAPI backend**

-  **React chat frontend**

-  **Document ingestion (TXT, PDF, DOCX)**

-  **Long-term semantic memory**

  

------------------------------------------------------------------------

  

## 🚀 Project Overview

  

This project demonstrates how to build an AI assistant powered by vector

search with persistent memory and dynamic file-based knowledge

ingestion.

  

The system:

  

1. Converts documents into dense embeddings\

2. Stores them inside **Endee vector database**\

3. Retrieves relevant chunks using semantic similarity search\

4. Uses **Gemini LLM** to generate grounded answers\

5. Maintains long-term memory using a second vector index\

6. Supports uploading new documents dynamically

  

------------------------------------------------------------------------

  

## 🧠 System Architecture

  

Frontend (React Chat UI)

↓

FastAPI Backend (/chat, /upload)

↓

Endee Vector Database

↓

Gemini LLM

  

------------------------------------------------------------------------

  

## 🔍 How Endee Is Used

  

Endee powers all semantic search operations:

  

-  `rag_index` → Stores document embeddings\

-  `chat_memory` → Stores conversation embeddings\

-  `index.upsert()` → Inserts vectors\

-  `index.query()` → Retrieves semantically similar chunks

  

Each document chunk is stored as:

  

``` json

{

    "id": "uuid",

    "vector": [384-dimensional  embedding],

    "meta": {

        "text": "chunk content",

        "source": "filename"

    }

}

```

------------------------------------------------------------------------

  

# 🖥️ Local Setup Instructions

  

## 1️⃣ Clone Repository

  

```bash
git clone https://github.com/<your-username>/endee.git

cd endee/endee-rag
```

  

------------------------------------------------------------------------

  

## 2️⃣ Run Endee (Vector Database)

  

```bash
docker run -p  8080:8080 endeeio/endee-server:latest
```

  

Endee runs at: http://localhost:8080

  

------------------------------------------------------------------------

  

## 3️⃣ Create Required Indexes

  

Create two indexes via dashboard:

  

- rag_index (dimension: 384, space type: cosine, precision: int8)\

- chat_memory (dimension: 384, space type: cosine, precision: int8)

  

------------------------------------------------------------------------

  

## 4️⃣ Setup Backend

  
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
pip install endee
pip install -q -U google-genai
```
  

Create `.env` file:

  
```
GEMINI_API_KEY="your_gemini_api_key"
ENDEE_BASE_URL=http://localhost:8080/api/v1
```
  

------------------------------------------------------------------------

  

## 5️⃣ Start Backend

  
```bash
uvicorn main:app --reload
```
  

Backend runs at: http://127.0.0.1:8000

  

------------------------------------------------------------------------

  

## 6️⃣ Run Frontend

  
```bash
cd frontend
npm install
npm run dev
```
  

Frontend runs at: http://localhost:5173

  

------------------------------------------------------------------------

  

# 📤 Uploading Documents

  

Supported formats:

  

- .txt

- .pdf

- .docx

  

Uploaded files are extracted, chunked, embedded, and stored in

`rag_index`.

  

------------------------------------------------------------------------

  

# 💬 API Endpoints

  
```
POST /chat

Body: { "message": "What is RAG?" }
  
POST /upload

Form-data: file: `<document>`
```
  
------------------------------------------------------------------------

  

# 🧠 Features

  

- Dense vector search using Endee

- 384-d MiniLM embeddings

- Gemini grounded generation

- Persistent vector memory

- File ingestion

- Modern responsive chat UI

- Full local setup with Docker

  