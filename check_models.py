import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Configure with your key
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print("Checking available models for this API key...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Supported Model: {m.name}")
except Exception as e:
    print(f"Error fetching models: {e}")