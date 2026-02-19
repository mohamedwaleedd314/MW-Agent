import gradio as gr
from fastapi import FastAPI, UploadFile, File
from typing import List
import threading

from ingestion import upload_files
from chat_hybrid import hybrid_chat

conversation_history = []

# -------------------- FastAPI --------------------
app = FastAPI(title="  Chat API")

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    texts = []
    for f in files:
        content = await f.read()
        texts.append(f"{f.filename}: {len(content)} bytes")
    return {"uploaded": texts}

@app.post("/chat")
async def chat_api(message: str):
    global conversation_history
    conversation_history.append({"role": "user", "content": message})

    full_answer = ""
    for chunk in hybrid_chat(message):
        full_answer += chunk  # Accumulate all text chunks

    conversation_history.append({"role": "assistant", "content": full_answer})
    return {"answer": full_answer, "conversation": conversation_history}

@app.post("/clear")
def clear_api():
    global conversation_history
    conversation_history = []
    return {"status": "cleared"}

@app.get("/")
def root():
    return {"message": "⚡ Nitro Hybrid Chat API is running!"}

@app.get("/favicon.ico")
def favicon():
    return ""
#  Gradio 
def chat_gradio(message, history):
    history = history or []

    conversation_history.append({"role": "user", "content": message})
    conversation_history.append({"role": "assistant", "content": ""})

    for partial_answer in hybrid_chat(message):
        conversation_history[-1]["content"] = partial_answer
        yield (
            [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history],
            ""
        )
        
        
    conversation_history[-1]["content"] = partial_answer
    yield (
            [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history],
            ""
        )

def clear_gradio():
    global conversation_history
    conversation_history = []
    try:
        from memory import conversation_history as memory_history
        memory_history.clear()
    except ImportError:
        pass
    return []

def run_gradio():
    with gr.Blocks() as demo:
        gr.Markdown("# ⚡Nitro")

        with gr.Tab("📂 Upload Files"):
            file_input = gr.File(file_types=[".pdf", ".docx"], file_count="multiple")
            upload_btn = gr.Button("Upload")
            upload_output = gr.Textbox(label="File Texts")

            upload_btn.click(upload_files, file_input, upload_output)

        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(label="Assistant")
            msg = gr.Textbox(placeholder="Type your message here and press Enter...")
            clear = gr.Button("Clear Conversation")

            msg.submit(chat_gradio, [msg, chatbot], [chatbot, msg])
            clear.click(clear_gradio, None, chatbot)
            
        demo.queue()
        demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
       

if __name__ == "__main__":
    import uvicorn
    import time

    t = threading.Thread(target=run_gradio, daemon=True)
    t.start()

    time.sleep(1)

    uvicorn.run(app, host="127.0.0.1", port=8000)
