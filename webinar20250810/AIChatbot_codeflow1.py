import os
from openai import OpenAI

#TOGETHER_API_KEY - if it require to be free.
#restart the machine, to take effect or restart application
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY in environemnt variables")

client = OpenAI(api_key=api_key)
if not client:
    raise ValueError("Failed to create OpenAI client. Please check your API Key")

def chat():
    response = client.chat.completions.create(
        model = "gpt-4.1-nano-2025-04-14", #"meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
        messages = [
            {"role":"system","content":"You are a soft nature assistant"},
            {"role":"user","content":"Hi, How are you?"}
        ],
        temperature = 0.7,
        max_tokens = 100
    )
    reply = response.choices[0].message.content.strip()
    return reply

print(chat())

## step2 - Lets improvise it with function arguments and global variables.