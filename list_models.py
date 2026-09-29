import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in client.models.list():
    actions = getattr(model, "supported_actions", None)
    if actions and "generateContent" in actions:
        print(model.name)