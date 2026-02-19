# 🔥 MW Agent - COMPLETE LINE-BY-LINE CODE DOCUMENTATION

**Date:** February 19, 2026  
**Version:** 1.0  
**Detail Level:** LINE-BY-LINE ANALYSIS WITH EXAMPLES

---

## 📚 Table of Contents
1. [app.py - Main Application](#apppy)
2. [chat_engine.py - Response Generation](#chat_enginepy)
3. [llm_client.py - LLM Integration](#llm_clientpy)
4. [file_loader.py - File Processing](#file_loaderpy)
5. [chat_memory.py - Memory Management](#chat_memorypy)
6. [retrieval.py - Document Retrieval](#retrievalpy)
7. [requirements.txt - Dependencies](#requirementstxt)

---

# 🎯 app.py - Main Application Entrypoint

## Section 1: Imports (Lines 1-4)

### Line 1: `import gradio as gr`
```python
import gradio as gr
```

**What it does:**
- Imports the Gradio library and gives it the nickname `gr` for quick reference
- Gradio is a Python library for building beautiful web interfaces for ML models
- Creates a way to interact with the AI chatbot through a web browser

**Why we use it:**
- Provides pre-built UI components (buttons, text boxes, chat displays)
- Handles all web server complexity automatically
- No need to write HTML/CSS/JavaScript

**Example usage:**
```python
gr.Textbox()        # Creates an input text field
gr.Button("Click")  # Creates a clickable button
gr.Chatbot()        # Creates a chat display area
```

**Real-world analogy:**
Think of Gradio like a restaurant menu builder. Instead of describing every plate individually, you use Gradio's templates to quickly build a professional user interface.

---

### Lines 2-3: `from fastapi import FastAPI, UploadFile, File` and `from typing import List`
```python
from fastapi import FastAPI, UploadFile, File
from typing import List
```

**What it does:**
- **FastAPI:** Web framework for building REST APIs (web servers that send/receive data)
- **UploadFile:** Special type for handling file uploads from users
- **File:** Parameter marker that tells FastAPI "this is a file upload parameter"
- **List:** Python type hint that means "a list of items"

**Why we use them:**
- **FastAPI:** Modern, fast web framework with built-in documentation
- **UploadFile:** Handles file uploads safely and efficiently
- **typing.List:** Makes code self-documenting by showing what type of data we expect

**Example:**
```python
@api.post("/upload")
async def upload_endpoint(files: List[UploadFile] = File(...)):
    # This function accepts a list of uploaded files
    pass
```

**Breaking it down:**
- `files: List[UploadFile]` = "files must be a list of uploaded files"
- `File(...)` = "This is a file upload, and it's required (... means required)"

---

### Line 4: `import threading`
```python
import threading
```

**What it does:**
- Imports Python's threading module
- Allows running two programs simultaneously on the same computer
- Threading lets multiple things happen "at the same time"

**Why we need it:**
- Our application needs to run BOTH:
  1. Gradio UI (web interface on port 7860)
  2. FastAPI API (REST API on port 8000)
- Without threading, starting one would prevent the other from running
- Threading allows both to run in parallel

**Real-world analogy:**
Like a chef (main thread) directing two cooks (worker threads):
- Cook 1: Handles Gradio UI requests
- Cook 2: Handles FastAPI API requests
Both work simultaneously without waiting for each other.

**Code later shows:**
```python
gradio_thread = threading.Thread(target=start_gradio, daemon=True)
# Creates a new thread that runs the start_gradio function
```

---

### Lines 7-8: Custom Module Imports
```python
from file_loader import process_uploads
from chat_engine import generate_response
```

**What it does:**
- Imports functions from files WE CREATED in the same project
- `process_uploads`: Function that handles file uploads and extracts text
- `generate_response`: Function that generates AI responses

**Why:**
- Code organization and reusability
- Each file has one main responsibility:
  - `file_loader.py` = handles files
  - `chat_engine.py` = generates responses
- Makes code easier to understand and maintain

**Similar to:**
```python
# Like importing from a library:
from datetime import datetime  # Python's library

# But these are OUR custom libraries:
from file_loader import process_uploads  # Our file
from chat_engine import generate_response  # Our file
```

---

## Section 2: Global Variables (Line 10)

### Line 10: `chat_history = []`
```python
chat_history = []
```

**What it does:**
- Creates an empty list called `chat_history`
- This list will store all messages (user and assistant)
- "Global" means it's accessible from any function in this file

**Why it's important:**
- Tracks the complete conversation history
- Needed so both Gradio UI and FastAPI API can access same conversation
- Persists during the entire session (until app restarts)

**How it's used:**
```python
# Example: After a user sends a message
chat_history = [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI stands for Artificial Intelligence..."},
    {"role": "user", "content": "Tell me more"},
    {"role": "assistant", "content": "AI involves machine learning..."}
]
```

**⚠️ Important limitation:**
- Data is lost when app restarts
- Not saved to database or file
- Only exists in computer's RAM memory

---

## Section 3: FastAPI Server Setup (Line 12)

### Line 12: `api = FastAPI(title="MW Agent API")`
```python
api = FastAPI(title="MW Agent API")
```

**What it does:**
- Creates a new FastAPI web server object
- `title="MW Agent API"` sets the name shown in documentation

**Why:**
- FastAPI is like a constructor for building web APIs
- The `api` object will handle all HTTP requests (GET, POST, etc.)
- Creates automatic API documentation at `/docs`

**What this creates:**
- A web server that listens for HTTP requests
- Automatically creates interactive API documentation
- Handles routing (directing requests to right functions)

**Real-world analogy:**
Like opening a store:
- `FastAPI()` = building the store
- `title="MW Agent API"` = store name on the door
- The store is now ready to receive customers (requests)

---

## Section 4: API Endpoints

### Lines 14-19: Upload Endpoint

```python
@api.post("/upload")
async def upload_endpoint(files: List[UploadFile] = File(...)):
    results = []
    for f in files:
        content = await f.read()
        results.append(f"{f.filename}: {len(content)} bytes")
    return {"uploaded": results}
```

**Breaking it down line by line:**

#### `@api.post("/upload")`
- **Decorator** that registers this function as an HTTP POST endpoint
- `@api.post` = "When someone POSTs to this endpoint, run this function"
- `"/upload"` = the URL path (e.g., `http://localhost:8000/upload`)
- **POST** = HTTP method used to submit data to server

**When would you use this:**
```
1. User opens: http://localhost:8000/upload?filename=test.pdf
2. FastAPI routes the request to upload_endpoint()
3. Function processes it and returns JSON response
```

---

#### `async def upload_endpoint(files: List[UploadFile] = File(...))`

**Breaking it down:**
- `async def` = Asynchronous function (can pause and resume)
- Why async? Multiple users might upload simultaneously
- Prevents blocking other operations while waiting for file read
- `files: List[UploadFile]` = Expects multiple file uploads
- `= File(...)` = Tells FastAPI "this is a file parameter, required"

**Why async matters:**
```
Synchronous (blocking):
User 1 uploads → App waits 5 seconds to finish → User 2 waits
Total time: 10 seconds

Asynchronous (non-blocking):
User 1 uploads → App starts User 2 upload too → Both at once
Total time: 5 seconds
```

---

#### `results = []`
- Creates empty list to store results
- Each file upload result will be added here

#### `for f in files:`
- Loops through each uploaded file
- `f` is a temporary variable representing one file at a time

**Example:**
```python
files = [
    UploadFile(filename="document1.pdf"),
    UploadFile(filename="document2.docx"),
    UploadFile(filename="image.png")
]

# Loop iteration 1: f = UploadFile(filename="document1.pdf")
# Loop iteration 2: f = UploadFile(filename="document2.docx")
# Loop iteration 3: f = UploadFile(filename="image.png")
```

---

#### `content = await f.read()`
- **await** = "Wait for this to complete (but don't block other things)"
- `f.read()` = Read the file's binary content into memory
- `content` = Stores the raw file data as bytes

**Why await?**
- Reading files takes time
- `await` allows other operations to continue while waiting
- Returns control to event loop (scheduler)

**Example:**
```python
content = b'\x89PNG\r\n\x1a\n...'  # Binary file data
len(content) = 1024  # File is 1024 bytes
```

---

#### `results.append(f"{f.filename}: {len(content)} bytes")`
- **f-string** (formatted string) creates readable text
- `f.filename` = name of the file (like "document.pdf")
- `len(content)` = file size in bytes
- Creates message like: "document.pdf: 15340 bytes"
- Adds message to `results` list

**Example:**
```python
if f.filename = "report.pdf" and len(content) = 25600:
    Message added: "report.pdf: 25600 bytes"
```

---

#### `return {"uploaded": results}`
- Returns JSON response to the user
- **JSON** = standardized format for sending data

**Example response:**
```json
{
  "uploaded": [
    "document1.pdf: 25600 bytes",
    "document2.docx: 15340 bytes",
    "image.png: 102400 bytes"
  ]
}
```

---

### Lines 21-30: Chat Endpoint

```python
@api.post("/chat")
async def chat_endpoint(message: str):
    global chat_history
    chat_history.append({"role": "user", "content": message})

    full_answer = ""
    for chunk in generate_response(message):
        full_answer += chunk

    chat_history.append({"role": "assistant", "content": full_answer})
    return {"answer": full_answer, "conversation": chat_history}
```

**Line by line:**

#### `@api.post("/chat")`
- Register this function for POST requests to `/chat` endpoint
- User sends message here to get AI response

#### `async def chat_endpoint(message: str)`
- Function accepts a message parameter
- `message: str` = message must be a string
- Async so multiple users can chat simultaneously

#### `global chat_history`
- Tells Python "use the global chat_history variable (not a local one)"
- Modifying it here affects the variable defined at line 10

**Why declare global?**
```python
# Without global, this creates a LOCAL variable:
chat_history = []  # Only exists inside this function

# With global, this modifies the GLOBAL variable:
global chat_history
chat_history = []  # Affects the variable from line 10
```

---

#### `chat_history.append({"role": "user", "content": message})`
- Adds user's message to conversation history
- Creates dictionary with:
  - `"role": "user"` = indicates this is from the user
  - `"content": message` = the actual message text

**Example:**
```python
chat_history.append({
    "role": "user",
    "content": "What is machine learning?"
})

# chat_history now contains:
# [{"role": "user", "content": "What is machine learning?"}]
```

---

#### `full_answer = ""`
- Creates empty string to collect AI response
- Will accumulate the answer word-by-word

#### `for chunk in generate_response(message):`
- Calls `generate_response()` to get AI response
- Returns chunks (pieces) of the response one at a time
- Loop adds each chunk to `full_answer`

**Why chunks?**
- Streaming = returning response word-by-word
- User sees response appear progressively (like typing)
- Better user experience than waiting 5+ seconds

**Example:**
```python
Chunks from AI:
1. "Machine"
2. " learning"
3. " is"
4. " artificial"
5. " intelligence"

After loop:
full_answer = "Machine learning is artificial intelligence"
```

---

#### `full_answer += chunk`
- Concatenates (joins) each chunk to previous text
- `+=` means "add to existing value"

**Step by step:**
```python
full_answer = ""
full_answer += "Machine"              # "Machine"
full_answer += " learning"            # "Machine learning"
full_answer += " is"                  # "Machine learning is"
full_answer += " artificial"          # "Machine learning is artificial"
full_answer += " intelligence"        # "Machine learning is artificial intelligence"
```

---

#### `chat_history.append({"role": "assistant", "content": full_answer})`
- Adds complete AI response to history
- `"role": "assistant"` = response from AI

**Final chat_history:**
```python
[
    {"role": "user", "content": "What is machine learning?"},
    {"role": "assistant", "content": "Machine learning is artificial intelligence..."}
]
```

---

#### `return {"answer": full_answer, "conversation": chat_history}`
- Returns JSON with:
  - `"answer"` = just the AI's response
  - `"conversation"` = complete chat history

**JSON response example:**
```json
{
  "answer": "Machine learning is artificial intelligence...",
  "conversation": [
    {"role": "user", "content": "What is machine learning?"},
    {"role": "assistant", "content": "Machine learning is artificial intelligence..."}
  ]
}
```

---

### Lines 32-34: Clear Endpoint

```python
@api.post("/clear")
def clear_endpoint():
    global chat_history
    chat_history = []
    return {"status": "cleared"}
```

**Line by line:**

#### `@api.post("/clear")`
- POST endpoint to clear conversation
- URL: `http://localhost:8000/clear`

#### `def clear_endpoint()` (not async)
- No async needed because operation is instant
- Doesn't need to wait for anything

#### `global chat_history`
- Indicates we're modifying the global variable

#### `chat_history = []`
- Resets to empty list (clears all messages)

#### `return {"status": "cleared"}`
- Returns confirmation JSON

---

### Lines 36-38: Health Check Endpoint

```python
@api.get("/")
def root():
    return {"message": "MW Agent API is running!"}
```

**What it does:**
- **GET** request (retrieve data, not submit)
- `/` = root URL (just `http://localhost:8000`)
- Returns message confirming API is running
- Used to check if server is alive

**Example:**
```bash
$ curl http://localhost:8000/
{"message":"MW Agent API is running!"}
```

---

### Lines 40-42: Favicon Endpoint

```python
@api.get("/favicon.ico")
def favicon():
    return ""
```

**What it does:**
- Browsers automatically request `favicon.ico` (the tiny website icon)
- This endpoint handles that request
- Returns empty string (no icon)
- Prevents error messages in logs

**Why needed:**
Without this, you'd see constant "404 favicon not found" errors in logs.

---

## Section 5: Gradio UI Functions

### Lines 44-65: Handle Chat Function

```python
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
    
    chat_history[-1]["content"] = partial_answer
    yield (
        [{"role": msg["role"], "content": msg["content"]} for msg in chat_history],
        ""
    )
```

**Line by line:**

#### `def handle_chat(message, history):`
- Called when user sends message in Gradio UI
- `message` = what user typed
- `history` = conversation history from UI
- Note: Different from API's `chat_history` global variable

#### `history = history or []`
- Python shortcut for "if history is None, use empty list"
- Ensures history is always a list (never None)

**Equivalent to:**
```python
if history is None:
    history = []
```

---

#### `chat_history.append({"role": "user", "content": message})`
- Add user's message to global chat history

#### `chat_history.append({"role": "assistant", "content": ""})`
- Add empty assistant response placeholder
- Will be filled with actual response next

**Structure at this point:**
```python
chat_history = [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": ""}  # Empty, will be filled
]
```

---

#### `for partial_answer in generate_response(message):`
- Loop through response chunks from AI
- `partial_answer` = one piece of response

#### `chat_history[-1]["content"] = partial_answer`
- **[-1]** = last item in list (the empty assistant message)
- `.["content"]` = access the "content" field
- Replaces empty string with new partial response

**Example:**
```python
# Initial:
chat_history[-1] = {"role": "assistant", "content": ""}

# After 1st chunk:
chat_history[-1] = {"role": "assistant", "content": "Machine"}

# After 2nd chunk:
chat_history[-1] = {"role": "assistant", "content": "Machine learning"}

# After 3rd chunk:
chat_history[-1] = {"role": "assistant", "content": "Machine learning is..."}
```

---

#### `yield (...)`
- **yield** = return value but keep function running
- Called multiple times (once per chunk)
- Returns response to Gradio UI for display

**Why yield?**
```
Regular return: Function stops, returns once
Yield: Function continues, returns multiple times

Like a generator/stream of data instead of all-at-once
```

---

#### The yield tuple: `[..., ""]`
```python
yield (
    [{"role": msg["role"], "content": msg["content"]} for msg in chat_history],
    ""
)
```

**Breaking it down:**
- First element: List comprehension creating readable format
- Second element: Empty string ""

**What the list comprehension does:**
```python
[{"role": msg["role"], "content": msg["content"]} for msg in chat_history]

# Equivalent to:
result = []
for msg in chat_history:
    result.append({"role": msg["role"], "content": msg["content"]})
# Returns: result
```

**Real example:**
```python
# If chat_history is:
[
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Machine"}
]

# The list comprehension produces:
[
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Machine"}
]
# (Same thing - just copying relevant fields)
```

---

#### Why second element is `""`?
- Gradio UI expects tuple: (chat_display, input_field_value)
- `""` = clear the input field after sending
- User can type next message

---

### Lines 67-77: Clear Chat Function

```python
def clear_chat():
    global chat_history
    chat_history = []
    try:
        from chat_memory import history as memory_history
        memory_history.clear()
    except ImportError:
        pass
    return []
```

**Line by line:**

#### `def clear_chat():`
- Function to clear conversation (called from Gradio button)

#### `global chat_history`
- Indicates we're modifying global variable

#### `chat_history = []`
- Empty the list

#### `try: ... except ImportError: pass`
- **try block** = attempt to run code
- **except block** = if error occurs, handle it

**Specific error handling:**
```python
try:
    from chat_memory import history as memory_history
    memory_history.clear()
except ImportError:
    # If chat_memory doesn't exist or can't import, ignore the error
    pass
```

**Why?**
- Code tries to clear persistent memory too
- If it fails, doesn't crash the app
- Graceful error handling

#### `return []`
- Returns empty list to Gradio
- Clears chat display in UI

---

### Lines 79-102: Create Gradio Interface

```python
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
```

**Breaking this down:**

#### `def start_gradio():`
- Function to build and launch Gradio interface
- Called in separate thread (runs in background)

#### `with gr.Blocks() as demo:`
- **Context manager** (with statement)
- Creates container for all UI components
- `as demo` = variable name for the interface

**What is gr.Blocks?**
- Gradio's layout system
- Organizes components (buttons, text boxes, etc.)
- Like an HTML container

---

#### `gr.Markdown("# MW Agent")`
- Creates markdown heading
- Displays "# MW Agent" as large title

**In browser:**
```
MW Agent
========
(displayed as large heading)
```

---

#### `with gr.Tab("Upload Files"):`
- Creates a tab named "Upload Files"
- All components inside are part of this tab

**Result:**
```
[Upload Files] [Chat]
```

---

#### `file_input = gr.File(...)`
```python
file_input = gr.File(
    file_types=[".pdf", ".docx"],
    file_count="multiple"
)
```

**What it does:**
- Creates file upload component
- `file_types=[".pdf", ".docx"]` = only accept these formats
- `file_count="multiple"` = allow uploading multiple files
- Stores reference in `file_input` variable

---

#### `upload_button = gr.Button("Upload")`
- Creates clickable button
- Labeled "Upload"
- Stored in `upload_button` variable

---

#### `upload_result = gr.Textbox(label="File Texts")`
- Creates text display area
- `label="File Texts"` = label shown above box
- Will display file extraction results

---

#### `upload_button.click(process_uploads, file_input, upload_result)`
- **Event handler** = "when button is clicked, do something"
- `process_uploads` = function to call
- `file_input` = pass this as input
- `upload_result` = display return value here

**When user clicks Upload button:**
```
1. Get files from file_input
2. Call process_uploads(files)
3. Display return value in upload_result
```

---

#### `with gr.Tab("Chat"):`
- Creates "Chat" tab
- Components below go in this tab

---

#### `chatbot = gr.Chatbot(label="Assistant")`
- Creates chat display component
- Shows conversation history
- `label="Assistant"` = header text

**Displays like:**
```
Assistant
─────────
User: Hi
Assistant: Hello!
User: How are you?
Assistant: I'm doing well, thank you!
```

---

#### `message_input = gr.Textbox(...)`
```python
message_input = gr.Textbox(
    placeholder="Type your message here and press Enter..."
)
```

- Text input field
- `placeholder` = hint text shown when empty

---

#### `clear_button = gr.Button("Clear Conversation")`
- Button to clear chat
- Labeled "Clear Conversation"

---

#### `message_input.submit(handle_chat, [message_input, chatbot], [chatbot, message_input])`
- **Event handler** for text submission (Enter key or Send)
- `handle_chat` = function to call
- `[message_input, chatbot]` = inputs (what gets sent to function)
- `[chatbot, message_input]` = outputs (what gets updated)

**Flow:**
```
User types message → Presses Enter
     ↓
Function: handle_chat(message, chatbot)
     ↓
Updates: chatbot display, clears message_input
```

---

#### `clear_button.click(clear_chat, None, chatbot)`
- When clear button clicked
- Call `clear_chat()` function
- `None` = no inputs
- `chatbot` = update this display

---

#### `demo.queue()`
- Enables request queuing
- Handles multiple concurrent requests
- Prevents server overload

**Why?**
```
Without queue():
Multiple users → First come, first served (blocking)

With queue():
Multiple users → All handled, queued if needed (non-blocking)
```

---

#### `demo.launch(server_name="127.0.0.1", server_port=7860, share=False)`
- **Launches** the web interface
- `server_name="127.0.0.1"` = localhost (only on this computer)
- `server_port=7860` = runs on port 7860
- `share=False` = don't create public link

**Result:**
```
Gradio URL: http://127.0.0.1:7860
Open in browser to access UI
```

---

## Section 6: Main Execution (Lines 104-111)

```python
if __name__ == "__main__":
    import uvicorn
    import time

    gradio_thread = threading.Thread(target=start_gradio, daemon=True)
    gradio_thread.start()

    time.sleep(1)

    uvicorn.run(api, host="127.0.0.1", port=8000)
```

---

### `if __name__ == "__main__":`
- Checks if script is run directly (not imported)
- Prevents code running if file imported as module

**Example:**
```python
# File: app.py

def my_function():
    print("Hello")

if __name__ == "__main__":
    my_function()

# When you run: python app.py
# Output: Hello

# When you run: from app import my_function
# Output: (nothing - if block skipped)
```

---

### `import uvicorn` and `import time`
- Now imports these modules
- `uvicorn` = ASGI server for FastAPI
- `time` = time operations

**Why import here?**
- Only needed if script runs directly
- Saves memory if file imported elsewhere

---

### `gradio_thread = threading.Thread(target=start_gradio, daemon=True)`
- Creates new thread object
- `target=start_gradio` = function to run in thread
- `daemon=True` = thread stops when main program stops

**Why daemon=True?**
```
daemon=True: Thread is subsidiary
- If main program exits, thread dies too
- Doesn't keep program alive

daemon=False: Thread is independent
- Main program waits for thread to finish
- Keeps program alive
```

---

### `gradio_thread.start()`
- **Starts the thread**
- Runs `start_gradio()` in background
- Gradio UI launches at http://127.0.0.1:7860

---

### `time.sleep(1)`
- **Pause for 1 second**
- Gives Gradio time to start before FastAPI starts

**Why?**
```
Without sleep:
FastAPI starts immediately
Might start before Gradio finishes initializing
Could cause port conflicts

With sleep:
Gradio gets 1 second head start
Then FastAPI starts
Cleaner startup
```

---

### `uvicorn.run(api, host="127.0.0.1", port=8000)`
- **Starts FastAPI server**
- `api` = the FastAPI app (defined at line 12)
- `host="127.0.0.1"` = localhost only
- `port=8000` = runs on port 8000

**Result:**
```
FastAPI API: http://127.0.0.1:8000
API docs:   http://127.0.0.1:8000/docs
```

---

### **Overall Execution Flow:**
```
1. Python runs app.py
2. If run directly (not imported):
   a. Create background thread for Gradio
   b. Start Gradio thread (port 7860 web UI)
   c. Wait 1 second
   d. Start FastAPI server (port 8000 API)
3. Both run simultaneously
   - User can access: http://127.0.0.1:7860 (UI)
   - Developer can use: http://127.0.0.1:8000 (API)
```

---

---

# 💬 chat_engine.py - Response Generation

## Overview
This file generates AI responses based on user messages using context from files and chat history.

---

## Line-by-Line Breakdown

### Lines 1-3: Imports

```python
from llm_client import stream_chat_response
from chat_memory import save_exchange, get_context
from retrieval import answer_with_sources
from file_loader import stored_chunks
```

**Each import explained:**

#### `from llm_client import stream_chat_response`
- Imports function that calls the LLM
- `stream_chat_response()` = gets response from AI model
- Returns response word-by-word (streaming)

**Example usage:**
```python
for chunk in stream_chat_response("What is AI?"):
    print(chunk)  # Prints one word at a time
```

---

#### `from chat_memory import save_exchange, get_context`
- `save_exchange()` = saves Q&A pair to memory
- `get_context()` = retrieves previous conversations

**Example:**
```python
save_exchange("What is AI?", "AI is artificial intelligence...")
context = get_context(last_n=5)  # Last 5 exchanges
```

---

#### `from retrieval import answer_with_sources`
- Imports function for semantic search
- Would search uploaded documents
- Currently imported but not used

---

#### `from file_loader import stored_chunks`
- Imports list of text chunks from uploaded files
- `stored_chunks = ["text from file 1", "text from file 2", ...]`

---

### Line 5: Function Definition

```python
def generate_response(user_message):
```

- Main function that generates AI responses
- Takes user's message as input
- Returns response (via yield for streaming)

---

### Lines 7-8: Get Context Variables

```python
    memory_context = get_context()
    file_context = "\n".join(stored_chunks)
```

**Line 7:** `memory_context = get_context()`
- Calls `get_context()` from chat_memory module
- Returns formatted string of last 5 Q&A pairs
- Default is 5, can be changed in chat_memory.py

**Example return value:**
```
Question: What is ML?
Answer: Machine learning is...
Question: Tell me more
Answer: ML involves neural networks...
```

---

**Line 8:** `file_context = "\n".join(stored_chunks)`
- Joins all text chunks with newlines
- `"\n"` = newline character
- Creates single string from list of chunks

**Visual example:**
```python
# Before (list):
stored_chunks = [
    "--- document.pdf ---\nChapter 1: Introduction...",
    "--- document.pdf ---\nChapter 2: Methods...",
    "--- document.pdf ---\nChapter 3: Results..."
]

# After (string):
file_context = "--- document.pdf ---\nChapter 1: Introduction...
--- document.pdf ---\nChapter 2: Methods...
--- document.pdf ---\nChapter 3: Results..."
```

---

### Lines 10-12: Limit Context Window

```python
    if len(file_context) > 3000:
        file_context = file_context[-3000:]
```

**Line 10:** `if len(file_context) > 3000:`
- Check if file context is larger than 3000 characters
- **len()** = counts characters

**Why limit?**
- LLM has maximum input length
- Too much context slows down response
- Better to use most recent/relevant parts

---

**Line 12:** `file_context = file_context[-3000:]`
- **[-3000:]** = last 3000 characters
- Python slicing: negative index counts from end
- Keeps most recent information

**Explanation:**
```python
text = "ABCDEFGHIJKLMNOPQRST"  # 20 characters
text[-5:]  # Last 5 characters: "PQRST"
text[-10:]  # Last 10 characters: "KLMNOPQRST"

file_context = "....text repeated 5000 times...."
file_context[-3000:]  # Keep only last 3000 characters
```

---

### Lines 14-18: Language Detection

```python
    if all(ord(c) < 128 for c in user_message.replace(" ", "")):
        language = "English"
    else:
        language = "Arabic"
```

**Breaking this down:**

#### `user_message.replace(" ", "")`
- Removes all spaces from message
- Focuses on actual characters

**Example:**
```python
"Hello world" → "Helloworld"
"مرحبا بالعالم" → "مرحباالعالم"
```

---

#### `ord(c) < 128`
- **ord()** = gets ASCII value of character
- **ASCII** = encoding for English characters (0-127)
- Characters with value < 128 are English alphabet

**Examples:**
```python
ord('A') = 65  (< 128, English)
ord('ا') = 1575 (> 128, Arabic)
ord('م') = 1605 (> 128, Arabic)
```

---

#### `all(...)`
- Returns True if ALL characters satisfy condition
- Returns False if ANY character doesn't satisfy

**Example:**
```python
all([True, True, True])      # True (all are True)
all([True, False, True])     # False (one is False)
all([ord(c) < 128 for c in "Hello"])    # True (all English)
all([ord(c) < 128 for c in "مرحبا"])    # False (all Arabic)
```

---

#### Full condition:
```python
if all(ord(c) < 128 for c in user_message.replace(" ", "")):
```

Reads as: "If all non-space characters are ASCII (< 128), it's English"

**Result:**
```python
message = "What is AI?"
# All chars < 128 → language = "English"

message = "ما هو الذكاء الاصطناعي"
# Contains chars > 128 → language = "Arabic"
```

---

### Lines 20-43: Build Prompt

```python
    prompt = f"""
You are an intelligent assistant.

You have two sources of information:

1) File contents:
{file_context}

2) Conversation context:
{memory_context}

Important instructions:

- If the files contain useful information -> use it
- If the files are not useful -> ignore them and respond naturally
- Never say the information is not found unless the question is specifically about the files
- Always respond in a natural and helpful way
- **Do not cut sentences or words**
- **Complete the sentence fully before writing any part of the answer**
- If using streaming or progressive text generation, pause until the sentence is complete.

User message:
{user_message}

Respond in {language}.
"""
```

**What is this?**
- Multi-line f-string (formatted string literal)
- `f"""..."""` = f-string with triple quotes (allows newlines)
- Template for LLM with everything it needs to know

**Breaking down the prompt structure:**

**Role definition:**
```
You are an intelligent assistant.
```
- Tells LLM what to act as

---

**Context sources:**
```
1) File contents:
{file_context}

2) Conversation context:
{memory_context}
```
- Shows LLM what information is available
- `{file_context}` = inserts actual file content
- `{memory_context}` = inserts conversation history

**Example after substitution:**
```
You are an intelligent assistant.

You have two sources of information:

1) File contents:
--- document.pdf ---
Chapter 1: Introduction to AI...
Chapter 2: Machine Learning Methods...

2) Conversation context:
Question: What is AI?
Answer: AI stands for Artificial Intelligence...
```

---

**Instructions:**
```
- If the files contain useful information -> use it
- If the files are not useful -> ignore them and respond naturally
- Never say the information is not found unless specifically asked
- Always respond naturally
- Don't cut sentences mid-word
- Complete sentences fully before starting answer
```

These tell LLM HOW to respond (behavior guidelines)

---

**User query:**
```
User message:
{user_message}
```
- The actual question to answer

---

**Language instruction:**
```
Respond in {language}.
```
- `{language}` = "English" or "Arabic"
- Tells LLM what language to use

**Final prompt looks like:**
```
You are an intelligent assistant.

You have two sources of information:

1) File contents:
Modern AI techniques include deep learning, machine learning, and natural language processing...

2) Conversation context:
Question: What is machine learning?
Answer: Machine learning is a subset of AI...

Important instructions:
- If files contain useful info, use it
- Otherwise respond naturally
... more instructions...

User message:
Give me more examples of AI applications

Respond in English.
```

---

### Lines 46-50: Generate Response

```python
    full_answer = ""

    for partial in stream_chat_response(prompt):
        full_answer = partial
        yield full_answer
```

**Line 46:** `full_answer = ""`
- Initialize empty string for accumulating response

**Line 48:** `for partial in stream_chat_response(prompt):`
- Calls LLM with the prompt
- Returns chunks of response one at a time
- Loop processes each chunk

**What `stream_chat_response()` returns:**
```
Iteration 1: "Machine"
Iteration 2: "Machine learning"
Iteration 3: "Machine learning is"
Iteration 4: "Machine learning is a"
... continues until complete
```

---

**Line 49:** `full_answer = partial`
- Updates `full_answer` with latest chunk
- Contains cumulative response so far

---

**Line 50:** `yield full_answer`
- **Yields** current state to caller
- Returns value but function continues
- Called multiple times (once per chunk)

**Why yield?**
- Allows streaming response
- UI/API can show partial response
- Better user experience

**Example:**
```python
# Without yield (all at once):
response = "Machine learning is artificial intelligence..."
return response
# User waits 5 seconds, then sees entire response

# With yield (chunked):
yield "Machine"
yield "Machine learning"
yield "Machine learning is"
... more yields...
yield "Machine learning is artificial intelligence..."
# User sees response appear progressively
```

---

### Line 52: Save to Memory

```python
    save_exchange(user_message, full_answer)
```

- Saves Q&A pair to chat memory
- Stores for future context
- Function from chat_memory module

**What gets saved:**
```python
{
    "question": "What is machine learning?",
    "answer": "Machine learning is artificial intelligence..."
}
```

**Why?**
- Next call to `get_context()` includes this exchange
- Creates conversational continuity
- Makes AI remember previous topics

---

---

# 🤖 llm_client.py - LLM Integration

## Overview
This file handles communication with the LLM (Language Model) via Hugging Face's API.

---

## Line-by-Line Analysis

### Lines 1-5: Imports and Environment Setup

```python
import requests
import json
from dotenv import load_dotenv
import os
```

---

#### `import requests`
- Library for making HTTP requests
- Used to communicate with LLM API

**What it does:**
```python
response = requests.post(url, data=data)
# Makes HTTP POST request to API
```

---

#### `import json`
- Library for handling JSON (JavaScript Object Notation)
- LLM API returns JSON data
- Converts between JSON strings and Python objects

**Example:**
```python
json_string = '{"name": "John", "age": 30}'
python_dict = json.loads(json_string)
# {"name": "John", "age": 30}
```

---

#### `from dotenv import load_dotenv`
- Loads environment variables from `.env` file
- Keeps secrets out of code

**What's in .env:**
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@host/db
```

---

#### `import os`
- Operating system module
- Used to access environment variables

**Example:**
```python
import os
api_key = os.getenv("API_KEY")
# Gets value from environment or .env
```

---

### Line 6: Load Environment

```python
load_dotenv()
```

- Reads .env file
- Makes variables available via `os.getenv()`

**What happens:**
```
.env file contains:
HF_TOKEN=hf_abc123...

After load_dotenv():
os.getenv("HF_TOKEN") returns "hf_abc123..."
```

---

### Line 7: Get API Token

```python
API_TOKEN = os.getenv("HF_TOKEN")
```

- Retrieves Hugging Face API token from environment
- Token authenticates requests to Hugging Face API

**Example value:**
```
API_TOKEN = "hf_7KXQmYzRfHwI8kP2oLjNqM3rStUvWxYzAbCdEf"
```

**Why secret?**
- Token is like a password
- Gives access to your account
- Should never be in code, only in .env

---

### Lines 9: API Endpoint

```python
API_URL = "https://router.huggingface.co/v1/chat/completions"
```

- URL of Hugging Face's chat API
- Where we send prompts and get responses
- "router" = load balancer that routes to available servers

**What happens:**
```
POST to API_URL:
Send: {"model": "deepseek", "messages": [...]}
Receive: {"choices": [{"delta": {"content": "response text"}}]}
```

---

### Lines 11-13: Request Headers

```python
REQUEST_HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
}
```

- Dictionary of HTTP headers for requests
- `"Authorization"` = authentication header
- `f"Bearer {API_TOKEN}"` = inserts token value

**Example value:**
```
{
    "Authorization": "Bearer hf_7KXQmYzRfHwI8kP2oLjNqM3rStUvWxYzAbCdEf"
}
```

**How it's used:**
```python
response = requests.post(
    API_URL,
    headers=REQUEST_HEADERS,  # Includes auth token
)
```

---

### Line 15: Model Selection

```python
LLM_MODEL = "deepseek-ai/DeepSeek-V3:novita"
```

- Specifies which AI model to use
- `deepseek-ai/DeepSeek-V3` = model name
- `:novita` = specific provider/version

**Alternative models:**
```python
"meta-llama/Llama-2-70b-chat-hf"
"mistralai/Mistral-7B-Instruct-v0.1"
"gpt2"
```

---

### Lines 18-25: Function Definition and Payload

```python
def stream_chat_response(prompt, max_tokens=2000):

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "stream": True
    }
```

---

#### `def stream_chat_response(prompt, max_tokens=2000):`
- Function that gets streaming response from LLM
- `prompt` = question/instruction for AI
- `max_tokens=2000` = default maximum response length

**Token explanation:**
- Token ≈ 4 characters (approximate)
- 2000 tokens ≈ 8000 characters ≈ 4 pages
- Limits response size and API cost

---

#### Building the payload (request body):

```python
payload = {
    "model": LLM_MODEL,
    "messages": [...],
    "max_tokens": max_tokens,
    "stream": True
}
```

**Each field:**

- `"model": LLM_MODEL` = which AI model to use
- `"messages": [{"role": "user", "content": prompt}]` = conversation
  - `"role": "user"` = message is from user
  - `"content": prompt` = the actual message/prompt
- `"max_tokens": max_tokens` = max response length
- `"stream": True` = return response as stream (chunks)

**Full example:**
```python
{
    "model": "deepseek-ai/DeepSeek-V3:novita",
    "messages": [
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ],
    "max_tokens": 2000,
    "stream": true
}
```

---

### Lines 27-33: Make API Request

```python
    response = requests.post(
        API_URL,
        headers=REQUEST_HEADERS,
        json=payload,
        stream=True
    )

    if response.status_code != 200:
        yield f"Error {response.status_code}: {response.text}"
        return
```

---

#### `response = requests.post(...)`
- Makes HTTP POST request to API
- `requests.post()` is like sending a form submission

**Parameters:**
- `API_URL` = where to send request
- `headers=REQUEST_HEADERS` = includes auth token
- `json=payload` = request body (converted to JSON)
- `stream=True` = receive response as stream

**Return:**
- `response` = HTTP response object

---

#### `if response.status_code != 200:`
- Checks HTTP status code
- 200 = success
- Other codes mean error (401, 403, 500, etc.)

**Common status codes:**
```
200 = OK (success)
400 = Bad Request (invalid parameters)
401 = Unauthorized (bad token)
403 = Forbidden (access denied)
500 = Server Error (API problem)
```

---

#### Error handling:
```python
if response.status_code != 200:
    yield f"Error {response.status_code}: {response.text}"
    return
```

- If not 200, return error message
- `response.text` = full error details
- `yield` = return to caller
- `return` = stop function

**Example error response:**
```
"Error 401: Unauthorized: Invalid or expired API token"
```

---

### Lines 35-54: Parse Streaming Response

```python
    accumulated_text = ""

    for line in response.iter_lines():
        if not line:
            continue

        decoded_line = line.decode("utf-8")

        if decoded_line.startswith("data:"):
            decoded_line = decoded_line.replace("data:", "").strip()

        if decoded_line == "[DONE]":
            break

        try:
            data = json.loads(decoded_line)

            if "choices" in data:
                delta = data["choices"][0].get("delta", {})

                if "content" in delta:
                    token = delta["content"]
                    accumulated_text += token
                    yield accumulated_text

        except:
            continue
```

---

#### `accumulated_text = ""`
- Stores complete response built up so far
- Updated with each new token

---

#### `for line in response.iter_lines():`
- Iterates through streaming response line-by-line
- Each line is part of the response

**Example stream:**
```
data: {"choices":[{"delta":{"content":"Machine"}}]}
data: {"choices":[{"delta":{"content":" learning"}}]}
data: {"choices":[{"delta":{"content":" is"}}]}
data: [DONE]
```

---

#### `if not line: continue`
- Skip empty lines
- `not line` = if line is empty/None
- `continue` = go to next iteration

---

#### `decoded_line = line.decode("utf-8")`
- Converts bytes to string
- `bytes` = binary data from network
- `decode("utf-8")` = convert to readable text

**Example:**
```python
line = b'data: {"choices":...}'  # bytes
decoded_line = 'data: {"choices":...}'  # string
```

---

#### `if decoded_line.startswith("data:"):`
- Checks if line starts with "data:" prefix
- Streaming API adds this prefix to each line

---

#### `decoded_line = decoded_line.replace("data:", "").strip()`
- Removes "data:" prefix
- `.strip()` = removes whitespace from start/end

**Example:**
```python
before = 'data: {"choices":...}'
after = '{"choices":...}'  # "data:" removed
```

---

#### `if decoded_line == "[DONE]":`
- Checks for end marker
- API sends "[DONE]" when response complete
- `break` = exit loop

---

#### `try: ... except: continue`
- Try to parse JSON
- If error, skip line and move to next
- Prevents crashes from malformed data

---

#### `data = json.loads(decoded_line)`
- Converts JSON string to Python dictionary
- `json.loads()` = parse JSON

**Example:**
```python
json_string = '{"choices":[{"delta":{"content":"Machine"}}]}'
data = json.loads(json_string)
# data = {
#     "choices": [
#         {"delta": {"content": "Machine"}}
#     ]
# }
```

---

#### `if "choices" in data:`
- Checks if "choices" field exists
- API response structure has "choices" field containing responses

---

#### `delta = data["choices"][0].get("delta", {})`
- Gets delta from first choice
- `.get("delta", {})` = get "delta" or empty dict if not found
- "delta" contains incremental content

**Breaking it down:**
```python
data = {
    "choices": [
        {"delta": {"content":"Machine"}} ← [0]
    ]
}

delta = {"content": "Machine"}
```

---

#### `if "content" in delta:`
- Checks if "content" field exists in delta
- Contains the text token

---

#### `token = delta["content"]`
- Extracts the actual text token
- `token` = the text piece to add

**Example:**
```python
delta = {"content": "Machine"}
token = "Machine"

delta = {"content": " learning"}
token = " learning"
```

---

#### `accumulated_text += token`
- Adds token to accumulated response
- `+=` = append to string

**Example:**
```python
accumulated_text = ""
accumulated_text += "Machine"              # "Machine"
accumulated_text += " learning"            # "Machine learning"
accumulated_text += " is"                  # "Machine learning is"
```

---

#### `yield accumulated_text`
- Returns current state to caller
- Function pauses, waits for next `next()` call
- Allows progressive display

**Usage:**
```python
for chunk in stream_chat_response(prompt):
    print(chunk)

# Output:
# Machine
# Machine learning
# Machine learning is
# ... continues
```

---

---

# 📂 file_loader.py - File Processing

## Overview
Handles uploading, reading, and processing PDF and DOCX files.

---

## Line-by-Line Breakdown

### Lines 1-2: Imports

```python
import fitz
from docx import Document
```

---

#### `import fitz`
- Imports PyMuPDF library (fitz = "tools" in Latin)
- Reads and extracts text from PDF files
- `fitz` is the internal name, `PyMuPDF` is package name

**Install:**
```
pip install pymupdf
```

**Why fitz?**
- Fast and efficient PDF processing
- Handles complex PDFs with fonts, images, etc.

---

#### `from docx import Document`
- Imports Document class from python-docx
- Reads and extracts text from DOCX files

**Install:**
```
pip install python-docx
```

---

### Line 4: Global Storage

```python
stored_chunks = []
```

- Global list storing all text chunks from files
- Used by chat_engine to get file context
- Shared across functions

**Example content:**
```python
[
    "--- document.pdf ---\nChapter 1: Introduction...",
    "--- document.pdf ---\nChapter 2: Methods...",
    "--- document.pdf ---\nChapter 3: Results...",
    "--- guide.docx ---\nSection A: Getting Started...",
    "--- guide.docx ---\nSection B: Advanced Topics..."
]
```

---

### Lines 6-11: Extract PDF Text

```python
def extract_pdf_text(file_path):
    pdf_doc = fitz.open(file_path)
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text
```

---

#### `def extract_pdf_text(file_path):`
- Function to extract text from PDF
- `file_path` = path to PDF file

**Example:**
```python
extract_pdf_text("document.pdf")
extract_pdf_text("/path/to/file.pdf")
```

---

#### `pdf_doc = fitz.open(file_path)`
- Opens PDF file using PyMuPDF
- `pdf_doc` = PDF document object
- Allows accessing pages and content

**Example:**
```python
pdf_doc = fitz.open("research_paper.pdf")
# Now can iterate through pages
```

---

#### `text = ""`
- Initialize empty string for collecting text

---

#### `for page in pdf_doc:`
- Loops through each page in PDF
- `page` = one page object

**Example PDF with 3 pages:**
```
Iteration 1: page = Page 1
Iteration 2: page = Page 2
Iteration 3: page = Page 3
```

---

#### `text += page.get_text()`
- Extracts text from current page
- `get_text()` = gets all text on page as string
- `+=` = appends to existing text

**Example:**
```python
page.get_text() returns: "This is page 1 content."
text = ""
text += "This is page 1 content."  # "This is page 1 content."

page.get_text() returns: "This is page 2 content."
text += "This is page 2 content."  # "This is page 1 content.This is page 2 content."
```

---

#### `return text`
- Returns complete PDF text

---

### Lines 13-16: Extract DOCX Text

```python
def extract_docx_text(file_path):
    word_doc = Document(file_path)
    return "\n".join([p.text for p in word_doc.paragraphs])
```

---

#### `def extract_docx_text(file_path):`
- Function to extract text from DOCX
- `file_path` = path to DOCX file

---

#### `word_doc = Document(file_path)`
- Opens DOCX file using python-docx
- `word_doc` = Document object

---

#### `word_doc.paragraphs`
- List of all paragraphs in document
- Each paragraph has `.text` property

**Example:**
```python
word_doc.paragraphs = [
    Paragraph("Introduction"),
    Paragraph("This is the first section."),
    Paragraph("Methods"),
    Paragraph("We used the following approach...")
]
```

---

#### `[p.text for p in word_doc.paragraphs]`
- List comprehension extracting text from each paragraph
- Equivalent to:

```python
texts = []
for p in word_doc.paragraphs:
    texts.append(p.text)
# texts = ["Introduction", "This is...", "Methods", "We used..."]
```

---

#### `"\n".join([...])`
- Joins all texts with newline characters
- Creates single string with paragraphs on separate lines

**Example:**
```python
texts = ["Introduction", "This is...", "Methods"]
"\n".join(texts) returns:
"Introduction
This is...
Methods"
```

---

#### `return "\n".join(...)`
- Returns complete document text with paragraphs separated

---

### Lines 18-25: Extract Text (Dispatcher)

```python
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)
    else:
        raise ValueError("Unsupported file format")
```

---

#### `def extract_text(file_path):`
- General function that handles any supported format
- "Dispatcher" = routes to appropriate function

---

#### `if file_path.endswith(".pdf"):`
- Checks if filename ends with .pdf
- `.endswith()` = checks file extension

**Example:**
```python
"document.pdf".endswith(".pdf")      # True
"document.docx".endswith(".pdf")     # False
"my.pdf.backup".endswith(".pdf")     # False
```

---

#### `return extract_pdf_text(file_path)`
- If PDF, call PDF extraction function
- Returns extracted text

---

#### `elif file_path.endswith(".docx"):`
- Else if file is DOCX
- Similarly check and extract

---

#### `else: raise ValueError(...)`
- If neither PDF nor DOCX, raise error
- Tells user file format not supported

**Example error:**
```python
extract_text("image.png")
# Raises: ValueError("Unsupported file format")
```

---

### Lines 27-29: Split Text into Chunks

```python
def split_text(text, chunk_size=2000):
    """Split large texts into smaller chunks"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

---

#### `def split_text(text, chunk_size=2000):`
- Splits long text into manageable pieces
- `text` = text to split
- `chunk_size=2000` = default 2000 characters per chunk

---

#### `"""..."""` (Docstring)
- Documentation string explaining function
- Accessible via `help(split_text)`

---

#### List comprehension breakdown:
```python
[text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

**Step by step:**
- `range(0, len(text), chunk_size)` = positions: 0, 2000, 4000, 6000, ...
- `text[i:i+chunk_size]` = slice of 2000 characters
- `[... for ...]` = create list

**Example with 6000 character text:**
```python
text = "A" * 6000  # 6000 A's

chunk_size = 2000
range(0, 6000, 2000) = [0, 2000, 4000]

text[0:2000] = "AAAA...AAAA" (2000 A's)
text[2000:4000] = "AAAA...AAAA" (2000 A's)
text[4000:6000] = "AAAA...AAAA" (2000 A's)

Result: [
    "AAAA...AAAA",
    "AAAA...AAAA",
    "AAAA...AAAA"
]
```

---

### Lines 31-46: Process Uploads

```python
def process_uploads(files):
    """
    Upload files, split them into smaller chunks and store them in memory
    """
    global stored_chunks
    previews = []
    for f in files:
        try:
            text = extract_text(f.name)
            chunks = split_text(text)
            for chunk in chunks:
                formatted_chunk = f"--- {f.name} ---\n{chunk}"
                stored_chunks.append(formatted_chunk)
            previews.append(f"--- {f.name} ---\n{text[:1000]}...")
        except Exception as e:
            previews.append(f"Error in {f.name}: {str(e)}")
    return "\n\n".join(previews)
```

---

#### `def process_uploads(files):`
- Main function called when user uploads files
- `files` = list of uploaded file objects

---

#### `global stored_chunks`
- Indicates we're modifying global variable
- Changes visible to other functions

---

#### `previews = []`
- List to store preview text for display
- Shows user what was uploaded

---

#### `for f in files:`
- Loop through each uploaded file

---

#### `try: ... except Exception as e:`
- **try block** = attempt operations
- **except block** = catch errors

**Why?**
- File upload might fail
- Prevents entire process from crashing

---

#### `text = extract_text(f.name)`
- Extracts text from file
- `f.name` = filename

---

#### `chunks = split_text(text)`
- Splits text into 2000 character chunks
- Returns list of chunks

---

#### `for chunk in chunks:`
- Loops through each chunk

---

#### `formatted_chunk = f"--- {f.name} ---\n{chunk}"`
- Creates formatted chunk with filename header
- f-string includes filename and chunk

**Example:**
```python
formatted_chunk = "--- document.pdf ---\nChapter 1 content here..."
```

**Why add filename?**
- Later, AI knows which file content came from
- Provides context for sources

---

#### `stored_chunks.append(formatted_chunk)`
- Adds formatted chunk to global list
- Makes it available to chat_engine

---

#### `previews.append(f"--- {f.name} ---\n{text[:1000]}...")`
- Shows first 1000 characters to user
- `text[:1000]` = first 1000 chars
- Lets user verify file uploaded correctly

**Example preview:**
```
--- document.pdf ---
Introduction
================

This document provides comprehensive...
(first 1000 characters)...
```

---

#### `except Exception as e:`
- Catches any error
- `e` = the exception object

---

#### `previews.append(f"Error in {f.name}: {str(e)}")`
- Shows error message to user
- Indicates which file failed

**Example error message:**
```
Error in document.pdf: [Errno 2] No such file or directory
```

---

#### `return "\n\n".join(previews)`
- Returns all previews joined with double newlines
- Double newlines = paragraph separations
- Displayed in UI

**Example return:**
```
--- document1.pdf ---
Introduction...

--- document2.docx ---
Chapter 1...

Error in image.png: Unsupported file format
```

---

---

# 🧠 chat_memory.py - Conversation Memory

## Overview
Manages chat history storage and retrieval.

---

## Line-by-Line Breakdown

### Line 1: Global Storage

```python
history = []
```

- Global list storing conversation history
- Persists for entire session
- Shared across all functions

**Example content:**
```python
[
    {
        "question": "What is AI?",
        "answer": "AI stands for Artificial Intelligence..."
    },
    {
        "question": "Tell me more",
        "answer": "AI involves machine learning..."
    }
]
```

---

### Lines 4-7: Save Exchange Function

```python
def save_exchange(question, answer):
    history.append({
        "question": question,
        "answer": answer
    })
```

---

#### `def save_exchange(question, answer):`
- Function to save Q&A pair
- Called after each AI response
- `question` = user's question
- `answer` = AI's answer

---

#### `history.append({...})`
- Adds dictionary to history list
- Dictionary contains one Q&A pair

---

#### `{"question": question, "answer": answer}`
- Dictionary with two fields
- Keys are strings, values from parameters

**Example:**
```python
question = "What is machine learning?"
answer = "Machine learning is a subset of AI..."

save_exchange(question, answer)

# History now contains:
[
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a subset of AI..."
    }
]
```

---

### Lines 10-15: Get Context Function

```python
def get_context(last_n=5):
    return "\n".join([
        f"Question: {item['question']}\nAnswer: {item['answer']}"
        for item in history[-last_n:]
    ])
```

---

#### `def get_context(last_n=5):`
- Function to retrieve conversation context
- `last_n=5` = default retrieve last 5 exchanges

**Why 5?**
- Recent context most relevant
- Older exchanges less important
- Balances context size vs. memory

---

#### `history[-last_n:]`
- **[-last_n:]** = last N items from list
- Negative index = count from end

**Example:**
```python
history = [A, B, C, D, E, F, G, H, I, J]  # 10 items

history[-5:] = [F, G, H, I, J]  # Last 5
history[-3:] = [H, I, J]        # Last 3
history[-1:] = [J]              # Last 1
```

---

#### List comprehension with formatting:
```python
[
    f"Question: {item['question']}\nAnswer: {item['answer']}"
    for item in history[-last_n:]
]
```

**Breaking down:**
- For each item in last N history entries
- Format as: "Question: ...\nAnswer: ..."
- Create list of formatted strings

**Example:**
```python
history = [
    {"question": "What is AI?", "answer": "AI is..."},
    {"question": "Tell me more", "answer": "More details..."}
]

List comprehension produces:
[
    "Question: What is AI?\nAnswer: AI is...",
    "Question: Tell me more\nAnswer: More details..."
]
```

---

#### `"\n".join([...])`
- Joins formatted strings with newlines
- Converts list to single string

**Result:**
```
Question: What is AI?
Answer: AI is...
Question: Tell me more
Answer: More details...
```

**Why this format?**
- Readable for humans
- Easy for AI to understand context
- Includes both questions and answers

---

---

# 📦 requirements.txt - Dependencies

Each line is one package to install via `pip install`:

```
gradio
```
- Library for building web UI
- Creates interface easily

```
fastapi
```
- Framework for building REST APIs
- Modern, fast Python web framework

```
uvicorn
```
- ASGI server for running FastAPI
- Handles concurrent requests

```
langchain
```
- Framework for building LLM applications
- Simplifies integration with AI models

```
langchain-community
```
- Community integrations for LangChain
- Adds support for various tools

```
langchain-huggingface
```
- LangChain integration with Hugging Face
- Access HF embeddings and models

```
sentence-transformers
```
- Library for sentence embeddings
- Used for semantic search

```
faiss-cpu
```
- Vector database (CPU version)
- Fast similarity search

```
pymupdf
```
- PDF reading library (imported as fitz)
- Extracts text from PDFs

```
python-docx
```
- Read/write DOCX files
- Extracts text from Word documents

```
requests
```
- HTTP library for API calls
- Makes requests to LLM API

```
python-dotenv
```
- Loads environment variables from .env
- Manages secrets securely

```
transformers
```
- Hugging Face transformers library
- Access pre-trained models

```
torch
```
- PyTorch deep learning framework
- Required by transformers library
```

---

## Installation

```bash
pip install -r requirements.txt
```

This command installs all packages listed in requirements.txt

---

---

# 🔗 retrieval.py - Document Retrieval

## Overview
Handles semantic search in uploaded documents using embeddings and vector database.

---

## Line-by-Line Breakdown

```python
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from llm_client import stream_chat_response

VECTOR_DB_PATH = "vectordb"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=80
)

vector_store = None
```

---

### Imports
- `os` = filesystem operations
- `RecursiveCharacterTextSplitter` = splits text smartly
- `FAISS` = vector database for similarity search
- `HuggingFaceEmbeddings` = converts text to vectors
- `stream_chat_response` = LLM integration

### Configuration
- `VECTOR_DB_PATH` = where to save/load embeddings
- `embeddings` = model for converting text to vectors
- `text_splitter` = splits text into chunks
  - `chunk_size=600` = 600 characters per chunk
  - `chunk_overlap=80` = 80 chars overlap (for context)
- `vector_store = None` = global storage for vector database

---

```python
def load_vector_store():
    global vector_store
    if os.path.exists(VECTOR_DB_PATH):
        vector_store = FAISS.load_local(...)

def build_vector_store(text):
    global vector_store
    chunks = text_splitter.split_text(text)
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    vector_store.save_local(VECTOR_DB_PATH)

def find_relevant_docs(query, k=3):
    if vector_store is None:
        return []
    return vector_store.similarity_search(query, k=k)
```

### Functions
- `load_vector_store()` = loads existing embeddings
- `build_vector_store()` = creates embeddings from new text
- `find_relevant_docs()` = searches for similar documents

---

---

# ✅ Complete Documentation Summary

This document provides **line-by-line analysis** of all major code files including:

1. **app.py** - Main application (3,000+ words)
2. **chat_engine.py** - Response generation (800+ words)
3. **llm_client.py** - LLM integration (2,000+ words)
4. **file_loader.py** - File processing (1,500+ words)
5. **chat_memory.py** - Memory management (500+ words)
6. **retrieval.py** - Vector search (300+ words)
7. **requirements.txt** - Dependencies (200+ words)

**Total: 10,000+ words of detailed explanations**

---

**Documentation Created:** February 19, 2026  
**Detail Level:** LINE-BY-LINE WITH EXAMPLES  
**Audience:** Developers, students, anyone learning the codebase
