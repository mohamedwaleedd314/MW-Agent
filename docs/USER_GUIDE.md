# MW Agent Chat - User & Developer Guide

##  Getting Started

### Prerequisites
- **Python 3.11+** installed.
- **HuggingFace Account** (for API Token).
- **Git** (for version control).

### Installation (Local)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/rag-project.git
   cd rag-project
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```env
   HF_TOKEN=hf_your_token_here
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   - **Gradio UI:** [http://127.0.0.1:7860](http://127.0.0.1:7860)
   - **API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  Usage Guide

### Using the Web Interface (Gradio)
1. **Upload Files:** Go to the "Upload Files" tab. Select one or more `.pdf` or `.docx` files and click "Upload".
2. **Chat:** Switch to the "Chat" tab. Type your question.
   - The system will use information from your uploaded files if relevant.
   - It will also remember the last 5 turns of conversation.
3. **Clear History:** Click "Clear Conversation" to reset the memory.

### Using the REST API
You can interact programmatically using curl or any HTTP client.

**Upload a File:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@MyDocument.pdf'
```

**Chat:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat?message=Summarize%20the%20document' \
  -H 'accept: application/json'
```

**Clear Memory:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/clear' \
  -H 'accept: application/json'
```

---

## 🛠️ Developer Guide

### Code Structure
- **`app.py`**: The main entry point. Initializes FastAPI and Gradio.
- **`file_loader.py`**: Handles file reading and text chunking logic.
- **`retrieval.py`**: Manages the FAISS vector store and embedding generation.
- **`chat_engine.py`**: Coordinates the RAG pipeline (Retrieval + Generation).
- **`llm_client.py`**: Handles communication with the HuggingFace Inference API.
- **`chat_memory.py`**: Simple in-memory list for chat history.

### Extensibility
- **Adding File Types:** Modify `file_loader.py` to support `.txt` or `.md`.
- **Replacing LLM:** Update `llm_client.py` to point to a local Ollama instance or OpenAI API.
- **Persistent Storage:** Replace `chat_memory.py` with a database (SQLite/PostgreSQL).
