import os
from typing import Any
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.document_loaders.pdf import PyPDFLoader
from pydantic import BaseModel

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")


llm = OpenAI(api_key=OPENAI_API_KEY, verbose=True)
res = llm.invoke("How are you?")
print(res)

"""
outline of what the agent would do
1. at first it would take in
    - user info
    - previous cover letters and job descriptions (only the successful one)
2. take in the target job description
3. produce a cover letter by type (type = "upwork_proposal", "application")
"""


class Data(BaseModel):
    successful_letters: list


multi_step_agent = None


def generate_coverletter(user_id: str, job_description: str):
    # TODO: fetch the user info
    prev_history = _get_user_history(user_id)
    prompt = _format_base_prompt(job_description)
    res = multi_step_agent.invoke(prompt)


def _get_user_history(user_id: str) -> list:
    pass


def _format_base_prompt(job_description: str) -> Any:
    # TEST: needed
    user_profile_data = PyPDFLoader(os.path.abspath("./assets/test-data--profile.pdf"))
