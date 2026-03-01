import os
import uuid
from sentence_transformers import SentenceTransformer
from endee import Endee

model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local Endee
client = Endee()

INDEX_NAME = "rag_index"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")


def chunk_text(text, chunk_size=200):
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def ingest():
    index = client.get_index(name=INDEX_NAME)

    vectors_to_insert = []

    for file in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            content = f.read()
            chunks = chunk_text(content)

            for chunk in chunks:
                embedding = model.encode(chunk).tolist()

                vectors_to_insert.append({
                    "id": str(uuid.uuid4()),
                    "vector": embedding,
                    "meta": {
                        "text": chunk,
                        "source": file
                    }
                })

    index.upsert(vectors_to_insert)

    print("Ingestion complete!")


if __name__ == "__main__":
    ingest()