from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import embed_query, search_index, call_llm

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question = data["question"].strip()

    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    try:
        embedded = embed_query(question)
        context_chunks = search_index(embedded)
        context_text = "\n\n".join(context_chunks)
        answer = call_llm(question, context_text)

        return jsonify({"answer": answer})
    
    except Exception as e:
        print(f"[Server error] {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
