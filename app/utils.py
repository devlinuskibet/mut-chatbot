# === Embedding Model ===
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests

model = SentenceTransformer('all-MiniLM-L6-v2')

# === Pinecone Setup ===
PINECONE_API_KEY = "your api key"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("mut-chatbot")

# === OpenRouter Settings ===
OPENROUTER_API_KEY = "your api key"
LLM_MODEL = "mistralai/mistral-7b-instruct"

# Embed question
def embed_query(query):
    return model.encode([query])[0].tolist()

# Search Pinecone
def search_index(embedded_query, top_k=3):
    try:
        response = index.query(vector=embedded_query, top_k=top_k, include_metadata=True, namespace="__default__")
        results = []
        for match in response['matches']:
            meta = match.get('metadata', {})
            topic = meta.get('topic', 'No Topic')
            text = meta.get('text', '')
            results.append(f"{topic}: {text}")
        return results
    except Exception as e:
        print(f"[Pinecone Error] {e}")
        return []

# Call LLM via OpenRouter
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
            print(f"[OpenRouter Error] {response.status_code}: {response.text}")
            return "Sorry, the language model failed to respond."
    except Exception as e:
        print(f"[OpenRouter Exception] {e}")
        return "Sorry, there was an error contacting the AI service."
