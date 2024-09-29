if __name__ != "__main__":
    print("this test should be run directly")
    exit(1)

import os
import sys
from icecream import ic

parent_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(parent_dir)


# from agent.coverletter_writer import generate_coverletter
from agent.multi_step_agent import MultiStepAgent


user_id = "test-user-1"
job_description = """Fullstack Developer (AI-Driven SaaS Platform)

We are seeking a skilled Fullstack Developer to join our dynamic team and contribute to the ongoing development of our SaaS platform, which is heavily focused on streamlining RFP responses with integrated AI solutions. This role involves building and enhancing features for a cutting-edge platform that leverages advanced AI models (LLM).

We are looking for a developer who has a solid understanding of available AI tools and models, and who can seamlessly integrate them via APIs into the platform. While you don’t need to be an AI engineer developing models, you must be comfortable working with AI technologies and have the ability to implement them effectively within a fullstack environment.

Key Responsibilities:

- Design and develop new features for the RFP Response Platform
- Integrate AI models and tools via APIs into the platform
- Collaborate with our development team to implement AI-driven features
- Ensure smooth operation between frontend and backend components
- Troubleshoot and optimize AI integrations for better performance

Key Requirements:

- Strong proficiency in both frontend and backend development
- Experience with API integration, especially with AI tools and models
- Familiarity with LLMs and AI technologies, with the ability to effectively integrate them into a product
- Ability to work in a fast-paced, evolving environment

This is a unique opportunity for someone passionate about full stack development and interested in shaping the future of AI-driven SaaS platforms."""

# result = generate_coverletter(user_id, "Upwork Proposal", job_description)

agent = MultiStepAgent()
result = agent.execute(job_description)
print("=" * 80)
ic(result)
print("=" * 80)