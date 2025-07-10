# 🤖 MUT Chatbot – Murang'a University of Technology Assistant

A smart web-based chatbot built to assist students, staff, and visitors at **Murang'a University of Technology** with accurate and real-time information about the university. It leverages vector search (Pinecone), sentence embeddings, and LLMs (Mistral via OpenRouter) to provide precise answers based on an internal knowledge base.

---

## 🔧 Technologies Used

| Technology        | Role                                 |
|------------------|--------------------------------------|
| **Python**       | Backend logic and embedding          |
| **Flask**        | API Server                           |
| **SentenceTransformers** | For creating semantic vector embeddings |
| **Pinecone**     | Vector database for storing knowledge |
| **OpenRouter (Mistral)** | Large Language Model for generating responses |
| **HTML/CSS/JS**  | Web frontend interface                |
| **Render**       | Backend deployment platform (cloud)  |
| **Vercel/Netlify** | Frontend deployment platform       |

---

## 📂 Project Structure

mut-chatbot/
│
├── app/
│ ├── chatbot.py # Main Flask app
│ ├── utils.py # Embedding, search, and LLM call logic
│ ├── frontend/
│ │ └── index.html # Web interface for the chatbot
│
├── knowledge_base/
│ ├── *.txt # Knowledge base files for Pinecone embedding
│ └── embed_and_upload.py # Script to embed and upload to Pinecone
│
├── requirements.txt # All dependencies
├── render.yaml # Optional: for deployment on Render
└── README.md # You're reading it!

yaml
Copy
Edit

---

## 🚀 Features

- 📚 Embeds knowledge from static `.txt` files into Pinecone
- 🔍 Performs vector search to find the most relevant chunks
- 🤖 Queries Mistral-7B via OpenRouter for high-quality answers
- 💬 Simple web-based frontend for asking questions
- ☁️ Ready for full-stack deployment on the web

---

## ⚙️ Requirements

- Python 3.10+
- Git
- Pinecone account and index
- OpenRouter API key
- Optional (for deployment): Render and Vercel accounts

---

## 🧠 How It Works

1. **Knowledge Upload:** `.txt` files from the knowledge base are broken into chunks, embedded using `all-MiniLM-L6-v2`, and uploaded to Pinecone.
2. **Query Flow:**
   - User asks a question through the frontend.
   - Question is embedded and matched against Pinecone vectors.
   - The most relevant content is passed into the LLM (Mistral via OpenRouter).
   - A response is generated and displayed in the chat window.

---

## 🛠️ Local Setup Instructions

### 1. Clone the Project

```bash
git clone https://github.com/YOUR_USERNAME/mut-chatbot.git
cd mut-chatbot
2. Create Virtual Environment and Install Dependencies
bash
Copy
Edit
conda create -n mut-agent python=3.10
conda activate mut-agent
pip install -r requirements.txt
3. Prepare .txt Knowledge Files
Add your .txt files inside the knowledge_base/ directory. For example:

diff
Copy
Edit
- admissions.txt
- clubs.txt
- contacts.txt
4. Embed and Upload to Pinecone
Update the Pinecone API key inside embed_and_upload.py, then run:

bash
Copy
Edit
cd knowledge_base
python embed_and_upload.py
5. Run Flask Server
Update OpenRouter API key inside utils.py or chatbot.py, then run:

bash
Copy
Edit
cd app
python chatbot.py
Flask should start on: http://127.0.0.1:5000

🌐 Deployment Guide
Backend (Flask)
Push your code to GitHub

Create a new Web Service on Render

Use:

Start Command: python app/chatbot.py

Add OPENROUTER_API_KEY and PINECONE_API_KEY in the environment settings

Frontend (HTML)
Push your frontend/ folder to a new GitHub repo

Deploy using Vercel or Netlify

In your HTML, make sure fetch("/ask") points to the full URL of your Flask API on Render

📌 Example Question Types
"How do I apply for a diploma program?"

"Who is the Dean of Students?"

"What clubs are available at MUT?"

"When does the semester begin?"

