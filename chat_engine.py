from llm_client import stream_chat_response
from chat_memory import save_exchange, get_context
from retrieval import answer_with_sources
from file_loader import stored_chunks

def generate_response(user_message):

    memory_context = get_context()
    file_context = "\n".join(stored_chunks)

    if len(file_context) > 3000:
        file_context = file_context[-3000:]

    if all(ord(c) < 128 for c in user_message.replace(" ", "")):
        language = "English"
    else:
        language = "Arabic"
    
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
    

    full_answer = ""

    for partial in stream_chat_response(prompt):
        full_answer = partial
        yield full_answer

    save_exchange(user_message, full_answer)
