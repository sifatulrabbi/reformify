import os
import hashlib
from uuid import uuid4
from typing import Any
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_chroma import Chroma

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found")

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
openai_model = ChatOpenAI(verbose=True, model=OPENAI_MODEL)
openai_embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)


def generate_coverletter(user_id: str, content_type: str, job_description: str):
    """
    outline of what the agent would do
    1. at first it would take in
        - user info
        - previous cover letters and job descriptions (only the successful one)
    2. take in the target job description
    3. produce a cover letter by type (type = "upwork proposal", "application", "cover letter")
    """

    prompt = _format_base_prompt(user_id, content_type, job_description)
    content = openai_model.invoke(prompt)
    return content.content


def _format_base_prompt(user_id: str, content_type: str, job_description: str):
    sysmsg = SystemMessage(
        f"""You are an helpful assistant and your primary task is to help user with writing effective and convertible {content_type}. To create the perfect proposal/cover letter/application for the user you'll follow these steps:
- Identify the key points in from the job's description
- Identify how the user matches the jobs requirements and the strenghts of the user
- Think about how you can best highlight the user's strenths that aligns with the job's description
- Follow the structure of the most impactful {content_type}s
- Make sure you are not making anything up and only telling the truth
- You should not use any corporate buzz words or any fancy words
- keep the output genuine and authentic

<user-profile-and-career-info>
<summary>
I love building software and collaborating with awesome people. I often use Go, Python, or TypeScript to hack out most of my curiosities on Neovim. I enjoy exploring the tech world and practicing system design concepts, which makes me more focused on the overall system. I've helped rebuild HelloScribe AI's entire system in a more secure and scalable way.

My preferred working environment is a fast-paced SaaS startup. Moving as fast as possible, making decisions that will change the entire outcome of a software system, and collaborating with awesome engineers always excite me.
</summary>

<another-about-me>
I love building software and collaborating with awesome people. Particularly, I dive into things I don't know and produce results. However, my attention span is limited to system design, server apps, web apps, and gen-AI. I enjoy exploring the tech world and mostly use Go, Python, and TypeScript to hack out my curiosities.
</another-about-me>

<experience>
HelloScribe AI is an AI productivity tool that speeds up various planning and content-writing tasks. It provides an intuitive web app and utilizes LLM engines to aid in plan-making and content writing.

* Collaborated with the founders and led the team to develop better and more time-effective solutions to improve and evolve the system
* Developed a flexible algorithm for the HelloScribe agent, laid the groundwork to implement a dynamic UI component generator from the core LLM, and completed the dynamic HTML table generator
* Improved the core data pipeline of HelloScribe, enhancing performance from handling a few dozen concurrent requests to managing up to 5,000 concurrent requests
* Architected a flexible pay-as-you-go billing system
* Improved the data models and frontend UI structure for better performance and scalability
* Led the development process to rebuild HelloScribe AI with massive improvement and new features such as the agent mode, better text editor, improved security, and scalable backend architecture
* Enforced coding styles and consistencies across team members
* Utilized LLM services (OpenAI, Gemini) to produce content, and build the HelloScribe Agent
* Built an advanced logging system to log critical application logs to our Slack channel
</experience>
<experience>/
X-Booker aims to streamline project management by combining most of the project management solutions into one single system with intelligent automation as well as providing an intuitive UI for easier navigation and business management.

* As the lead engineer, I worked closely with the founders to figure out technical solutions and the best way to materialize their vision
* Integrated various services such as Google Maps, Gmail, and Calendar into X-Booker's core API
* Architected a diverse system that uses background job processing, pub-sub, and a serverless approach to achieve various automation and data processing
* Built a flexible chat system with the ability to chat with individuals create groups, and share images, videos, and audio
* Architected a tier-based subscription system with buyable perks (extra storage or extra team seat)
* Built a complex but responsive, fast-loading, and secured dashboard, kanban board, email client, and file manager with different access levels (super admin, admin, and different types of teams)
* Architected a role-based auth system as well as an API integration so that the organizations can have direct external connections with other lead generation platforms
* Onboarded and mentored junior developers, in understanding the platform, and developing new features
* Developed an automated deployment pipeline to auto-deploy two different versions of the system on GCP’s Kubernetes cluster
</experience>

<personal-project>
<title>
Filepatrol
</title>
<github-repository>
[https://github.com/sifatulrabbi/filepatrol]
</github-repository>
<description>
A lightweight, real-time file system watcher and static HTTP file server. It triggers custom user commands upon detecting changes in directories or files. Written in Go and has 0 dependencies.
</description>
</personal-project>

<personal-project>
<title>
Shadow tracker
</title>
<github-repository>
[https://github.com/sifatulrabbi/shadowtracker]
</github-repository>
<description>
This tools monitors the http and https traffic forwards them to specified ports and also logs the traffic on a log file for future inspection
</description>
</personal-project>
</user-profile-and-career-info>

Now create a {content_type} based on the given job description."""
    )
    usermsg = HumanMessage(
        f"Write me a {content_type} for this following job description.\n<job-description>{job_description}</job-description>"
    )
    return [sysmsg, usermsg]


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


def _practice_embeddings_and_vectors():
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

    # profile_data_store = _get_user_chunked_profile_data(user_id)
    # results = profile_data_store.similarity_search("skills")
    # for r in results:
    #     print("*", r.page_content)
    return
