import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=gemini_api_key)

stream  = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain how AI works in a few words",
    stream=True
)
print("stream raw",stream)

for event in stream:
    print("event",event)
