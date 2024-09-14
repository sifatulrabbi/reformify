"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "what are the top most growing fields in freelancing? list the fields that are great for beginners and intermediate candidates to take advantage of",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## Top Growing Fields in Freelancing:\n\nHere's a breakdown of high-growth freelancing fields, ideal for both beginners and intermediate candidates:\n\n**High Growth & Beginner-Friendly:**\n\n* **Content Creation:**\n    * **Blog Writing:** High demand for engaging, SEO-optimized content.  \n    * **Social Media Management:**  Managing social media accounts for businesses.\n    * **Copywriting:** Writing compelling ad copy, website content, email marketing, etc.\n    * **Video Editing:**  Creating engaging videos for various platforms (YouTube, social media).\n    * **Graphic Design:**  Creating visual content (logos, social media graphics, etc.).\n    * **Transcription:**  Converting audio or video into text.\n    * **Proofreading/Editing:**  Ensuring written content is accurate and polished.\n\n* **Virtual Assistance:** \n    * **Administrative Support:**  Handling emails, scheduling, and basic tasks.\n    * **Customer Service:**  Providing support to clients via email, chat, or phone.\n    * **Social Media Management:**  Managing social media accounts for businesses.\n    * **Event Planning:**  Organizing and coordinating virtual or in-person events.\n\n* **Online Teaching:**\n    * **Tutoring:**  Providing one-on-one instruction in various subjects.\n    * **Language Teaching:**  Teaching a foreign language online.\n    * **Online Course Creation:**  Creating and selling online courses on platforms like Udemy or Teachable.\n\n* **Web Development & Design:**  \n    * **WordPress Development:** Building and maintaining websites using the WordPress platform.\n    * **Front-End Development:**  Creating the visual elements of websites (HTML, CSS, JavaScript).\n    * **UI/UX Design:**  Designing user interfaces and experiences for websites and apps. \n\n\n**Intermediate Level & High Growth:**\n\n* **Data Analysis & Data Science:**  Analyzing data to uncover insights and make informed decisions.\n* **Marketing & Sales:**\n    * **SEO:** Optimizing websites for search engines.\n    * **SEM:**  Managing paid search campaigns on platforms like Google Ads.\n    * **Social Media Marketing:**  Creating and executing social media marketing strategies.\n    * **Email Marketing:**  Creating and managing email marketing campaigns.\n* **Software Development:**  \n    * **Mobile App Development:**  Building apps for iOS and Android devices.\n    * **Web Development:**  Developing complex web applications using various languages and frameworks.\n    * **Back-End Development:**  Building and maintaining the server-side logic of web applications.\n\n**Tips for Beginners & Intermediate Candidates:**\n\n* **Build a Portfolio:**  Showcase your skills and experience to potential clients.\n* **Network:**  Connect with other freelancers, industry professionals, and potential clients.\n* **Market Your Services:**  Use social media, online platforms, and word-of-mouth to promote your skills.\n* **Stay Up-to-Date:**  Keep learning and stay informed about the latest trends in your field.\n* **Offer Value:**  Go above and beyond to deliver excellent service to clients.\n\n**Remember:**  The best field for you depends on your skills, interests, and goals. Research different areas, experiment with different projects, and find what you enjoy and are good at.",
            ],
        },
    ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
