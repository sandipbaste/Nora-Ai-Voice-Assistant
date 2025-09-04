# client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."
user_input = "what is coding"

response = model.generate_content([
    {"role": "user", "parts": [prompt]},
    {"role": "user", "parts": [user_input]}
])

print(response.text)
