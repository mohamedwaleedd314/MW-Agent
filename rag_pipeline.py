import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from hf_api import query_hf_chat_model_stream

DB_PATH = "vectordb"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=80
)

vectordb = None


def load_vectorstore():
    global vectordb
    if os.path.exists(DB_PATH):
        vectordb = FAISS.load_local(
            DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )


def build_vectorstore(text):
    global vectordb

    chunks = splitter.split_text(text)

    vectordb = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    vectordb.save_local(DB_PATH)


def retrieve_docs(query, k=3):
    if vectordb is None:
        return []

    return vectordb.similarity_search(query, k=k)


def rag_with_citations(question):

    docs = retrieve_docs(question)

    if not docs:
        return None

    context = ""
    sources = []

    for doc in docs:
        context += doc.page_content + "\n\n"
        sources.append(doc.page_content[:120])

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

    for partial in query_hf_chat_model_stream(prompt):
        full_answer = partial
        yield full_answer

    citations = "\n\n Sources:\n"
    for i, src in enumerate(sources, 1):
        citations += f"[{i}] {src}...\n"

    yield full_answer + citations



load_vectorstore()
