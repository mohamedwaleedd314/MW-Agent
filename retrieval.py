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


def load_vector_store():
    global vector_store
    if os.path.exists(VECTOR_DB_PATH):
        vector_store = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )


def build_vector_store(text):
    global vector_store

    chunks = text_splitter.split_text(text)

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    vector_store.save_local(VECTOR_DB_PATH)


def find_relevant_docs(query, k=3):
    if vector_store is None:
        return []

    return vector_store.similarity_search(query, k=k)


def answer_with_sources(question):

    docs = find_relevant_docs(question)

    if not docs:
        return None

    context = ""
    source_previews = []

    for doc in docs:
        context += doc.page_content + "\n\n"
        source_previews.append(doc.page_content[:120])

    prompt = f"""
You are an intelligent assistant specialized in document analysis.

You have excerpts from different files.

Important instructions:

- Information may come from multiple files
- If there are multiple sources -> merge and analyze them
- If a comparison is requested -> clearly explain the differences
- Do not treat the text as a single source
- Provide an accurate and coherent answer

Content:
{context}

Question:
{question}
"""

    full_answer = ""

    for partial in stream_chat_response(prompt):
        full_answer = partial
        yield full_answer

    citations = "\n\nSources:\n"
    for i, src in enumerate(source_previews, 1):
        citations += f"[{i}] {src}...\n"

    yield full_answer + citations



load_vector_store()
