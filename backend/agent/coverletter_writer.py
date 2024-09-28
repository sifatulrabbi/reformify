import os
from typing import Any
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings
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
    print("successfully constructed the prompt", prompt)


def _get_vector_store(user_id: str | None = None):
    persist_directory = os.path.abspath("./agent/store")
    vector_store = Chroma(
        embedding_function=openai_embedding,
        persist_directory=persist_directory,
        collection_name=(
            f"collection-{user_id}"
            if user_id
            else "multi-step-coverletter-agent-collection"
        ),
    )
    return vector_store


def _get_user_history(user_id: str) -> list:
    # TODO
    return []


def _get_user_profile_data(user_id: str):
    vecstore = _get_vector_store(user_id)
    docpath = os.path.abspath("./agent/assets/test-data--profile.pdf")
    user_profile_data = PyPDFLoader(docpath)
    user_profile_data = user_profile_data.load()
    print("document loaded, document count:", len(user_profile_data))
    return None


def _format_base_prompt(user_id: str, job_description: str) -> Any:
    # TODO: fetch the user info
    # prev_history = _get_user_history(user_id)
    profile_data = _get_user_profile_data(user_id)
