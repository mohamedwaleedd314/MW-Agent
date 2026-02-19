import gradio as gr
from fastapi import FastAPI, UploadFile, File
from typing import List
import threading

from file_loader import process_uploads
from chat_engine import generate_response

chat_history = []

api = FastAPI(title="MW Agent API")

@api.post("/upload")
async def upload_endpoint(files: List[UploadFile] = File(...)):
    results = []
    for f in files:
        content = await f.read()
        results.append(f"{f.filename}: {len(content)} bytes")
    return {"uploaded": results}

@api.post("/chat")
async def chat_endpoint(message: str):
    global chat_history
    chat_history.append({"role": "user", "content": message})

    full_answer = ""
    for chunk in generate_response(message):
        full_answer += chunk

    chat_history.append({"role": "assistant", "content": full_answer})
    return {"answer": full_answer, "conversation": chat_history}

@api.post("/clear")
def clear_endpoint():
    global chat_history
    chat_history = []
    return {"status": "cleared"}

@api.get("/")
def root():
    return {"message": "MW Agent API is running!"}

@api.get("/favicon.ico")
def favicon():
    return ""

def handle_chat(message, history):
    history = history or []

    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": ""})

    for partial_answer in generate_response(message):
        chat_history[-1]["content"] = partial_answer
        yield (
            [{"role": msg["role"], "content": msg["content"]} for msg in chat_history],
            ""
        )

def clear_chat():
    global chat_history
    chat_history = []
    try:
        from chat_memory import history as memory_history
        memory_history.clear()
    except ImportError:
        pass
    return []

def start_gradio():
    with gr.Blocks() as demo:
        gr.Markdown("# MW Agent")

        with gr.Tab("Upload Files"):
            file_input = gr.File(file_types=[".pdf", ".docx"], file_count="multiple")
            upload_button = gr.Button("Upload")
            upload_result = gr.Textbox(label="File Texts")

            upload_button.click(process_uploads, file_input, upload_result)

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(label="Assistant")
            message_input = gr.Textbox(placeholder="Type your message here and press Enter...")
            clear_button = gr.Button("Clear Conversation")

            message_input.submit(handle_chat, [message_input, chatbot], [chatbot, message_input])
            clear_button.click(clear_chat, None, chatbot)
            
        demo.queue()
        demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
       

if __name__ == "__main__":
    import uvicorn
    import time

    gradio_thread = threading.Thread(target=start_gradio, daemon=True)
    gradio_thread.start()

    time.sleep(1)

    uvicorn.run(api, host="127.0.0.1", port=8000)
