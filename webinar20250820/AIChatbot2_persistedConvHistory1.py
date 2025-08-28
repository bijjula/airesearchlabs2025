import json
import os
from openai import OpenAI
import tiktoken

# ------------------------------
# SETUP DESKTOP SAVE LOCATION
# ------------------------------
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
onedrive_desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
if os.path.exists(onedrive_desktop_path):
    desktop_path = onedrive_desktop_path

SESSION_FILE = os.path.join(desktop_path, "session_conv.json")

# ------------------------------
# CONVERSATION SAVE/LOAD
# ------------------------------
def load_session():
    """Load previous conversation if file exists."""
    if not os.path.exists(SESSION_FILE):
        print("No previous session found.")
        return []
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            print("Previous session loaded successfully.")
            return data
        except json.JSONDecodeError:
            print("Corrupted session file. Starting fresh.")
            return []

def save_session(messages):
    """Save current conversation to file."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)
    print(f"Session saved successfully at {SESSION_FILE}")

def start_new_session():
    """Start with a fresh conversation."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    print("Starting a new conversation session.")
    return []

def menu():
    """Display menu and return user's choice."""
    print("\n=== Conversation Manager ===")
    print("1. Start a new session")
    print("2. Load existing session")
    choice = input("Choose an option (1 or 2): ").strip()
    return choice

# ------------------------------
# OPENAI CHATBOT CONFIG
# ------------------------------
#api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("OPENAI_PERSONAL_KEY")  #fetches the API key from the environment variable.
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)
if not client:
    raise ValueError("Failed to create OpenAI client. Please check your API key.")

SYSTEM_PROMPT = "You are a lady acting as a pleasing assistant."
TEMPERATURE = 0.7
MAX_TOKENS = 50
MODEL = "gpt-4.1-nano-2025-04-14"
TOKEN_BUDGET = 100

def get_encoding(model):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Warning: Tokenizer for model '{model}' not found. Falling back to cl100k_base.")
        return tiktoken.get_encoding("cl100k_base")

ENCODING = get_encoding(MODEL)

def count_tokens(text):
    return len(ENCODING.encode(text))

def total_tokens_used(messages):
    try:
        return sum(count_tokens(msg["content"]) for msg in messages)
    except Exception as e:
        print(f"[token count error]: {str(e)}")
        return 0

def enforce_token_budget(messages, budget=TOKEN_BUDGET):
    try:
        while total_tokens_used(messages) > budget:
            if len(messages) <= 2:
                break
            messages.pop(1)  # remove oldest user/assistant message
    except Exception as e:
        print(f"[token budget error: {str(e)}]")

# ------------------------------
# CHAT LOOP
# ------------------------------
def chat_loop(messages):
    """Main chat interaction loop."""
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            save_session(messages)
            print("Exiting... Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        reply = response.choices[0].message.content.strip()

        messages.append({"role": "assistant", "content": reply})

        enforce_token_budget(messages)

        print(f"AI: {reply}")
        print(f"Total tokens used: {total_tokens_used(messages)}")

        save_session(messages)

# ------------------------------
# MAIN ENTRY
# ------------------------------
def main():
    choice = menu()
    if choice == "1":
        messages = start_new_session()
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    elif choice == "2":
        messages = load_session()
        if not messages:
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
    else:
        print("Invalid choice. Starting a new session by default.")
        messages = start_new_session()
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

    chat_loop(messages)

if __name__ == "__main__":
    main()


    
