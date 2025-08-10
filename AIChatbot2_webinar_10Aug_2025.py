import os
import openai import OpenAI
import tiktoken

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

client = OpenAI("gpt-3.5-turbo", api_key=api_key)

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    return len(tokens)

def chat_with_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to the AI Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break
        
        token_count = count_tokens(user_input)
        print(f"Token count for your input: {token_count}")
        
        ai_response = chat_with_ai(user_input)
        print(f"AI: {ai_response}")

if __name__ == "__main__":
    main()
# Ensure the script is run as the main module
# and not imported as a module in another script.
# This allows the chatbot to function independently.
# The script initializes the OpenAI client, counts tokens in user input,
# and interacts with the AI model to provide responses.
# The main function handles user input and AI responses in a loop,
# allowing for continuous conversation until the user decides to exit.
# The script is designed to be run in a terminal or command line interface. 
# It is a simple chatbot implementation using OpenAI's GPT-3.5 Turbo model.
# The chatbot can be extended with more features such as logging conversations,
# handling different user commands, or integrating with a web interface.
# The code is structured to be clear and maintainable,
# making it easy to add new functionalities in the future.
# The script uses the OpenAI Python client library to interact with the GPT-3.5 Turbo model.        
# It also uses the tiktoken library to count tokens in the user's input,
# which is important for understanding the cost and limits of API usage.    
# The chatbot is designed to be user-friendly and responsive,
# providing immediate feedback on user input and AI responses.                      
# The script is a good starting point for anyone looking to build a chatbot
# using OpenAI's API, and can be customized for various applications.
# The chatbot can be used for various purposes such as customer support,    
# educational tools, or just for fun conversations.
# The code is written in Python and requires the OpenAI and tiktoken libraries.
# Make sure to install these libraries using pip if you haven't done so:    
# pip install openai tiktoken
# The script is designed to be run in a Python environment with access to the internet. 
# Ensure you have set the OPENAI_API_KEY environment variable before running the script.
# This script is a simple implementation of a chatbot using OpenAI's GPT-3.5 Turbo model.
# It can be extended with more features such as logging conversations,  
# handling different user commands, or integrating with a web interface.
# The chatbot can be used for various purposes such as customer support,
# educational tools, or just for fun conversations.

# The code is structured to be clear and maintainable,
# making it easy to add new functionalities in the future.          
# The script is a good starting point for anyone looking to build a chatbot
# using OpenAI's API, and can be customized for various applications.       
# The chatbot can be used for various purposes such as customer support,
# educational tools, or just for fun conversations.