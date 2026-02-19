# ⚡ MW Agent Chat

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![Gradio](https://img.shields.io/badge/Gradio-4.16.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**MW Agent Chat** is a professional, privacy-focused RAG (Retrieval-Augmented Generation) system. It enables users to upload PDF and DOCX files and interact with them using advanced AI models through a sleek, dual-interface (Web UI & REST API).

---

## 🌟 Key Features

- **Multi-File Ingestion:** Upload and process multiple PDF/DOCX files simultaneously.
- **Intelligent RAG Pipeline:** Context-aware answers with visible citations.
- **Hybrid Chat Engine:** Seamlessly blends document knowledge with conversation history.
- **Dual Interface:** 
  - 🖥️ **Gradio UI:** Interactive web-based chat.
  - 🔌 **FastAPI:** Fully documented REST API for developers.
- **Local Vector Store:** Uses FAISS for efficient, local similarity search.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- HuggingFace API Token

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/MW-Agent-Chat.git
   cd MW-Agent-Chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   Create a `.env` file:
   ```env
   HF_TOKEN=your_huggingface_token
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

   - **Web UI:** [http://127.0.0.1:7860](http://127.0.0.1:7860)
   - **API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📚 Documentation

For detailed information, please refer to the `docs/` directory:

- [📖 User & Developer Guide](docs/USER_GUIDE.md) - Detailed usage instructions and code overview.
- [📄 Software Requirements Specification (SRS)](docs/SRS.md) - Technical specifications and architecture.

---

## 🛠️ Project Structure

```bash
nitro-hybrid-chat/
├── app.py              # Main entry point (FastAPI + Gradio)
├── chat_engine.py      # Core RAG logic & LLM orchestration
├── file_loader.py      # File parsing & text chunking
├── llm_client.py       # HuggingFace API client
├── chat_memory.py      # In-memory conversation history
├── retrieval.py        # Vector database management
├── requirements.txt    # Project dependencies
└── docs/               # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.
