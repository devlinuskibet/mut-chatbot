from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests

# === Embedding Model ===
model = SentenceTransformer('all-MiniLM-L6-v2')

# === Pinecone Setup ===
PINECONE_API_KEY = "your apikey"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("mut-chatbot")

# === OpenRouter Settings ===
OPENROUTER_API_KEY = "your api key"
LLM_MODEL = "mistralai/mistral-7b-instruct"

# === Embedding Function ===
def embed_query(query):
    return model.encode([query])[0].tolist()

# === Search in Pinecone Vector DB ===
def search_index(embedded_query, top_k=3):
    try:
        response = index.query(vector=embedded_query, top_k=top_k, include_metadata=True)
        return [
            f"{match['metadata']['topic']}: {match['metadata'].get('text', '')}"
            for match in response.get('matches', [])
        ]
    except Exception as e:
        print(f"[Pinecone error] {e}")
        return []

# === LLM Completion ===
def call_llm(question, context):
    prompt = f"""You are an assistant for Murang'a University of Technology students.
Answer the question using the context below.

Context:
{context}

Question: {question}
Answer:"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        if response.ok:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"[OpenRouter error] {response.status_code}: {response.text}")
            return "Sorry, the language model failed to respond."
    except Exception as e:
        print(f"[Request exception] {e}")
        return "Sorry, there was an error contacting the AI service."
