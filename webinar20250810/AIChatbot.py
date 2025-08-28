# openai API Key -- you need to go to platform.openai.com, register yourself and generate a API key
# You have save this OpenAI API key in your system environment variable. OEPNAI_API_KEY.

import os
from openai import OpenAI

api_key = os.getenv("OPENAI_PERSONAL_KEY")

print(f"apikey {api_key}")
if not api_key:
    raise ValueError("Please set the environment variable OEPNAI_API_KEY")

client = OpenAI(api_key = api_key)
if not client:
    raise ValueError("Something wrong with the model instance creation. Check the import packages and API key.")

response = client.chat.completions.create(
    model = "gpt-4.1-nano-2025-04-14",
    messages = [
        {"role":"system","content":"You are a soft natured assistant helping me to answer."},
        {"role":"user", "content":"hi, how are you"}
    ],
    temperature = 0.7,
    max_tokens = 100
)
response.choices[0].message.content.strip()

print(response)