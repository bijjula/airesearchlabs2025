import os 
from openai import OpenAI
import tiktoken

# fetch openai API Key from environment variable
# You need to set the environment variable OPENAI_API_KEY in your system.
# You can do this in your terminal or command prompt before running the script.
api_key = os.getenv("OPENAI_PERSONAL_KEY")  #fetches the API key from the environment variable.
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Plesae set the OPENAPI_KEY environement variable.")

# Create an OpenAI client instance
# Ensure you have the correct API key and the OpenAI package installed.
client = OpenAI(api_key=api_key)
if not client:
    raise ValueError("Failed to create OpenAI client. Please check your API key.")

# Define the system prompt and other parameters
# You can modify the system prompt to change the behavior of the AI assistant.
SYSTEM_PROMPT = "you are a lady acting as a pleasing assistant ." 
#SYSTEM_PROMPT = "You are a helpful assistant."
#SYSTEM_PROMPT = "you are a fed up and sassy assistant who hates answering questions."
#SYSTEM_PROMPT = You are a helpful assistant who provides concise and accurate answers to user queries.
#SYSTEM_PROMPT = "You are a soft natured assistant helping me to answer."
#SYSTEM_PROMPT = "You are a Japanese language assistant who helps me to answer in Japanese."
TEMPERATURE = 0.7
MAX_TOKENS = 50
MODEL = "gpt-4.1-nano-2025-04-14"
TOKEN_BUDGET = 100

# Initialize the messages list with the system prompt
# This list will hold the conversation history.
messages = [{"role": "system", "content":SYSTEM_PROMPT}]

# Function to get the encoding for the specified model
# This function uses the tiktoken library to handle tokenization.
def get_encoding(model):
     try:
          return tiktoken.encoding_for_model(model)
     except KeyError:
          print(f"Warning: Tokenizer formodel '{model}' not found. \
                 Falling back to cl100k_base.")
          return tiktoken.get_encoding("cl100k_base")
     
# Get the encoding for the specified model
# This encoding is used to count tokens in the messages.     
ENCODING = get_encoding(MODEL)

# Function to count tokens in a given text
# This function encodes the text and returns the number of tokens.
def count_tokens(text):
     tokens = ENCODING.encode(text)
     return len(tokens)

# Function to count tokens in a message
# This function counts the tokens in the content of a message. 
def total_tokens_used(messages):
    try:
        return sum(count_tokens(msg["content"]) for msg in messages)
    except Exception as e:
        print(f"[token count error]: {str(e)}")
        return 0

# Function to enforce a token budget on the messages
# This function ensures that the total tokens used do not exceed the specified budget.
def enforce_token_budget(messages, budget=TOKEN_BUDGET):
    try:
        while total_tokens_used(messages) > budget :
            if len(messages) <=2:
                break
            messages.pop(1)
    except Exception as e:
        print(f"[token budget error: {str(e)}]") 

 # Function to handle the chat interaction
# This function sends user input to the AI model and returns the AI's response.   
def chat(input_text):
        messages.append({"role": "user", "content": input_text})
        response = client.chat.completions.create(
            model=MODEL,
            messages = messages, # OR "You are a fed up and pleasing assistant who hates answering questions."
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})

        enforce_token_budget(messages)
        return reply

# Main loop to interact with the chatbot
# This loop allows the user to input messages and receive responses from the AI.
while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break
    
    ai_response = chat(user_input)
    print(f"You: {user_input}")
    print(f"AI: {ai_response}")
    print(f"Total tokens used: {total_tokens_used(messages)}")