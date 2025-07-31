import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from tqdm import tqdm

# Initialize Pinecone
PINECONE_API_KEY = "Your own api key"
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connect to index
index = pc.Index("mut-chatbot")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Chunking utility
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Read and chunk your knowledge base
file_path = "C:/Users/linzs/Desktop/Agent/knowledge_base/new.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

chunks = chunk_text(text)
metadata_list = [{"topic": "mut_knowledge_base", "text": chunk} for chunk in chunks]

# Upload in batches
batch_size = 50
for i in tqdm(range(0, len(chunks), batch_size)):
    batch_texts = chunks[i:i + batch_size]
    batch_vectors = model.encode(batch_texts).tolist()
    ids = [f"id-{i + j}" for j in range(len(batch_texts))]
    metadata = metadata_list[i:i + batch_size]
    vectors = [(ids[k], batch_vectors[k], metadata[k]) for k in range(len(batch_texts))]
    index.upsert(vectors=vectors)
