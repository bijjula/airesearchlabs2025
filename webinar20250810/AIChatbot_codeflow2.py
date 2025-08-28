## step2 - Lets improvise it with function arguments and global variables.
# user_input as one variable, and pass this to chat() and assign in the arguments.
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY in environemnt variables")

client = OpenAI(api_key=api_key)
if not client:
    raise ValueError("Failed to create OpenAI client. Please check your API Key")

MODEL = "gpt-4.1-nano-2025-04-14"
TEMPERATURE = 0.7 # randomness
MAX_TOKENS = 100 # number of tokens considered to return in response
SYSTEM_PROMPT = "You are a japanese teacher helping me to train in converting english words to japanese"
messages = [{"role":"system","content":SYSTEM_PROMPT}] #[0]

def chat(user_input):
    messages.append({"role":"user","content":user_input}) #[1]..
    response = client.chat.completions.create(
        model = MODEL,
        messages = messages,
        temperature = TEMPERATURE,
        max_tokens = MAX_TOKENS
    )
    reply = response.choices[0].message.content.strip()
    messages.append({"role":"assistant","content":reply})
    return reply

while True:
    user_input = input("You:")
    if user_input.strip().lower() in {"quit","exit"}:
        break
    print("Assistant:", chat(user_input))

