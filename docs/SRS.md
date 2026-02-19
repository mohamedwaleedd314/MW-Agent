# Software Requirements Specification (SRS)
## MW Agent Chat System

### 1. Introduction
**1.1 Purpose**
The purpose of the MW Agent Chat System is to provide a local, privacy-focused RAG (Retrieval-Augmented Generation) solution that allows users to query their own documents (PDF, DOCX) using advanced Large Language Models (LLMs).

**1.2 Scope**
The system acts as a bridge between user documents and LLMs. It ingests files, processes text into vector embeddings, and uses a hybrid chat engine to answer queries based on both document context and conversation history.

### 2. System Architecture
**2.1 Tech Stack**
- **Frontend:** Gradio (Web UI)
- **Backend:** FastAPI (REST API)
- **LLM Engine:** Hosted HuggingFace Inference API (DeepSeek-V3)
- **Vector Database:** FAISS (Local CPU-based)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Language:** Python 3.13+

**2.2 Modules**
- `app.py`: Entry point, orchestrates FastAPI and Gradio.
- `file_loader.py`: Handles file parsing (PDF/DOCX) and chunking.
- `retrieval.py`: Manages FAISS vector store and similarity search.
- `chat_engine.py`: Core logic combining memory, context, and LLM calls.
- `llm_client.py`: Interface for HuggingFace API streaming.
- `chat_memory.py`: Manages session-based conversation history.

### 3. Functional Requirements
**3.1 File Ingestion**
- Users must be able to upload multiple `.pdf` and `.docx` files.
- The system must text-chunk documents (default: 600 chars, 80 overlap).
- The system must generate and store vector embeddings locally.

**3.2 Chat Interface**
- Users can chat in natural language (English/Arabic supported).
- The system must retrieve relevant document chunks for each query.
- Responses must include citations/sources when using document data.
- The system must maintain conversation context (last 5 exchanges).

**3.3 API Support**
- `POST /upload`: Endpoint for file ingestion.
- `POST /chat`: Endpoint for sending queries.
- `POST /clear`: Endpoint for resetting session history.

### 4. Non-Functional Requirements
**4.1 Performance**
- Vector search latency: < 200ms for <10k chunks.
- LLM streaming response start: < 2 seconds.

**4.2 Security**
- API keys (`HF_TOKEN`) must be stored in `.env` and never exposed.
- All processing (except LLM inference) occurs locally.

**4.3 Usability**
- UI must be responsive and clear.
- Error messages (e.g., API failures) must be descriptive.
