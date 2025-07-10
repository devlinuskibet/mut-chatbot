import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from tqdm import tqdm

# Load the embedding model (384-dimensional)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone client with your API key
pc = Pinecone(api_key="pcsk_3Ew2Fb_5MQGNN9CGfzJZYiAU4e3MdspC6fK4L7BdCztLyuuoVvgALFuxy6csDny8tfnpoo")

# Connect to your Pinecone index
index = pc.Index("mut-chatbot")  # Use your actual index name

# Function to chunk long text into small segments
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to read and chunk a file
def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return chunk_text(text)

# Read all .txt files from the knowledge base folder
data_folder = "C:/Users/linzs/Desktop/Agent/knowledge_base"
all_chunks = []
metadata_list = []

for filename in os.listdir(data_folder):
    if filename.endswith(".txt"):
        topic = filename.replace(".txt", "")
        path = os.path.join(data_folder, filename)
        chunks = process_file(path)
        all_chunks.extend(chunks)
        metadata_list.extend([{"topic": topic}] * len(chunks))

# Upload embeddings in batches
batch_size = 50
for i in tqdm(range(0, len(all_chunks), batch_size)):
    batch_texts = all_chunks[i:i+batch_size]
    batch_vectors = model.encode(batch_texts).tolist()
    ids = [f"id-{i+j}" for j in range(len(batch_texts))]
    metadata = metadata_list[i:i+batch_size]
    index.upsert(vectors=list(zip(ids, batch_vectors, metadata)))
