import json
import os
from openai import OpenAI
import tiktoken

# ------------------------------
# SETUP DESKTOP SAVE LOCATION
# ------------------------------
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  #this line is not needed if your desktop is in onedrive only next line is enough.
onedrive_desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")   #This creates a path to your desktop folder."~" means “home director.On Windows → C:\Users\YourName On Mac/Linux → /home/YourName
if os.path.exists(onedrive_desktop_path):
    desktop_path = onedrive_desktop_path  # if the OneDrive desktop folder exists, then we use that instead of the normal desktop.

SESSION_FOLDER = os.path.join(desktop_path, "chat_sessions")   #   C:\Users\<userName>\Desktop\chat_sessions (creates a path )
os.makedirs(SESSION_FOLDER, exist_ok=True)  #Creates a folder at the given path. If the folder already exists, don’t throw an error so we use exist_ok=True.

# ------------------------------
# FILE HANDLING FUNCTIONS
# ------------------------------
def get_next_session_filename():
    """Generate the next numbered session filename."""
    existing_files = [f for f in os.listdir(SESSION_FOLDER) if f.startswith("session_conv_") and f.endswith(".json")]
    # f for f in if is to build list, os.listdir(SESSION_FOLDER) → returns all filenames in the folder SESSION_FOLDER, if f.startswith("session_conv_") → keeps only files whose names start with"session_conv_", and also end with ".json".
    if not existing_files:
        return os.path.join(SESSION_FOLDER, "session_conv_1.json")
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in existing_files]
    #f.split("_") → splits filename by underscore _. Example: "session_conv_12.json" → ["session", "conv", "12.json"]
    # [-1] → takes the last part: "12.json"
    #.split(".")[0] → splits by . and takes first part: "12"
    # int(...) → converts "12" to number 
    next_num = max(numbers) + 1 #finds the largest session number in the list.
    return os.path.join(SESSION_FOLDER, f"session_conv_{next_num}.json")  #returns path string

def list_sessions():
    """List all saved sessions."""
    files = sorted([f for f in os.listdir(SESSION_FOLDER) if f.startswith("session_conv_") and f.endswith(".json")],
                   key=lambda x: int(x.split("_")[-1].split(".")[0])) # Defines how to sort,key tells sorted() how to sort the items.
    return files

def load_session(filename):
    """Load a specific session file."""
    filepath = os.path.join(SESSION_FOLDER, filename)  #specific file name you want to load
    with open(filepath, "r", encoding="utf-8") as f: #encoding="utf-8 Ensures correct reading of special characters like emojis or non-English letters. as f: → Gives us a file object named f that we can read from. 
        try:
            data = json.load(f) #Reads the JSON file and converts it into a Python object
            print(f"Session '{filename}' loaded successfully.")  #Session 'session_conv_3.json' loaded successfully.
            return data
        except json.JSONDecodeError:
            print("Corrupted session file. Starting fresh.")  #if json file is not valid.
            return []

def save_session(messages, filepath):
    """Save current conversation to the given file path."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4) #Converts the Python object (messages) into JSON format and writes it directly into the file object f. Adds 4 spaces before each nested level.
    print(f"Session saved successfully at {filepath}")   

# ------------------------------
# OPENAI CHATBOT CONFIG
# ------------------------------
# fetch openai API Key from environment variable
# You need to set the environment variable OPENAI_API_KEY in your system.
# You can do this in your terminal or command prompt before running the script.
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

# ------------------------------
# TOKEN HANDLING FUNCTIONS
# ------------------------------
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
def chat_loop(messages, session_file):
    """Main chat interaction loop."""
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            save_session(messages, session_file)
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

        

        print(f"AI: {reply}")
        print(f"Total tokens used: {total_tokens_used(messages)}")

        save_session(messages, session_file)

# ------------------------------
# MAIN ENTRY
# ------------------------------
def main():
    print("\n=== Conversation Manager ===")
    print("1. Start a new session")
    print("2. Load existing session")
    choice = input("Choose an option (1 or 2): ").strip()  #strip removes any spaces or newline characters from the start and end of the input.

    if choice == "1":
        session_file = get_next_session_filename()
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        print(f"Starting a new session: {os.path.basename(session_file)}") #extracts just the filename (no folder path).

    elif choice == "2":
        sessions = list_sessions()
        if not sessions:
            print("No saved sessions found. Starting a new one.")
            session_file = get_next_session_filename()
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        else:
            print("\nAvailable sessions:")
            for idx, fname in enumerate(sessions, start=1): #Built-in Python function that takes a sequence,enumerate starts counting at 0.
                print(f"{idx}. {fname}")
            try:
                file_choice = int(input("Enter the number of the session to load: ")) #asks for input and converts it to an integer.
                selected_file = sessions[file_choice - 1]  #adjusts because list indexes start at 0, but menu numbers start at 1.
                session_file = os.path.join(SESSION_FOLDER, selected_file)
                messages = load_session(selected_file) #loads the JSON data from file into messages
                if not messages:
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]  #If the file is empty starts with a fresh system prompt.
            except (ValueError, IndexError):
                print("Invalid choice. Starting a new session.") 
                session_file = get_next_session_filename()       #Falls back to creating a new session.
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]  
    else:
        print("Invalid choice. Starting a new session by default.")         #If User Chooses Neither 1 Nor 2
        session_file = get_next_session_filename()
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_loop(messages, session_file)

if __name__ == "__main__":    
    main()
