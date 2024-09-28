import os
import hashlib
from uuid import uuid4
from typing import Any
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_chroma import Chroma

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
openai_llm = OpenAI(api_key=OPENAI_API_KEY, verbose=True, model=OPENAI_MODEL)
openai_embedding = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY, model=OPENAI_EMBEDDING_MODEL
)


def generate_coverletter(user_id: str, job_description: str):
    """
    outline of what the agent would do
    1. at first it would take in
        - user info
        - previous cover letters and job descriptions (only the successful one)
    2. take in the target job description
    3. produce a cover letter by type (type = "upwork_proposal", "application")
    """

    prompt = _format_base_prompt(user_id, job_description)
    # print("successfully constructed the prompt", prompt)


def _get_vector_store(user_id: str | None = None):
    persist_directory = os.path.abspath("./store")
    vector_store = Chroma(
        embedding_function=openai_embedding,
        persist_directory=persist_directory,
        collection_name=(
            f"collection-{user_id}"
            if user_id
            else "collection-multi-step-coverletter-agent"
        ),
    )
    return vector_store


def _get_user_history(user_id: str) -> list:
    # TODO
    return []


def _get_user_profile_data(user_id: str):
    docpath = os.path.abspath("./agent/assets/test-data--profile.pdf")
    doc_data = PyPDFLoader(docpath).load()
    ids = [
        hashlib.md5(doc.page_content.encode(), usedforsecurity=False).hexdigest()
        for doc in doc_data
    ]

    vecstore = _get_vector_store(user_id)
    print("trying to retrieve existing data...")
    prev_docs = vecstore.get(ids)
    if prev_docs:
        print("existing data found skipping save command")
        return vecstore
    print("user profile data saved in the vector store")
    vecstore.add_documents(doc_data, ids=ids)
    return vecstore


def _get_user_chunked_profile_data(user_id: str):
    vecstore = _get_vector_store(f"{user_id}-chunked")
    prev_docs = vecstore.get()
    if prev_docs.get("documents", None) and len(prev_docs.get("documents", [])) > 0:
        print("prev data found aborting now")
        return vecstore

    docpath = os.path.abspath("./agent/assets/test-data--profile.pdf")
    doc_data = PyPDFLoader(docpath).load()

    print("splitting the profile data into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks: list[str] = []
    for doc in doc_data:
        chunks.extend(text_splitter.split_text(doc.page_content))
    print("storing profile data chunks")
    for c in chunks:
        vecstore.add_texts([c], [{"source": "user_profile"}])

    return vecstore


def _format_base_prompt(user_id: str, job_description: str) -> Any:
    # TODO: fetch the user info
    # prev_history = _get_user_history(user_id)

    # profile_data = _get_user_profile_data(user_id)
    # docs = profile_data.similarity_search("Does Sifatul has experience in Python?")
    # for doc in docs:
    #     print(f"* {doc.page_content}")
    # retriever = profile_data.as_retriever(
    #     search_type="mmr",
    #     search_kwargs={"k": 6, "lambda_mult": 0.25},
    # )
    # docs = retriever.invoke("Does Sifatul has experience in Python?")
    # print("documents found:", len(docs))

    profile_data_store = _get_user_chunked_profile_data(user_id)
    results = profile_data_store.similarity_search("skills")
    for r in results:
        print("*", r.page_content)
