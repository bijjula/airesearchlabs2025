get_next_session_filename
list_sessions
load_session
save_session

#------------------------------
# FILE HANDLING FUNCTIONS
# ------------------------------

def list_sessions():
    """List all saved sessions."""
    files = sorted([f for f in os.listdir(SESSION_FOLDER) if f.startswith("session_conv_") and f.endswith(".json")],
                   key=lambda x: int(x.split("_")[-1].split(".")[0])) # Defines how to sort,key tells sorted() how to sort the items.
    return files

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



#------------------------------
# FILE HANDLING FUNCTIONS
# ------------------------------
def list_sessions():
    files = sorted([f for f in os.listdir(SESSION_FOLDER) if f.startswith("session_conv_") and f.endswith(".json")],
                   key=lambda x: int(x.split("_")[-1].split(".")[0])) 
    return files

def get_next_session_filename():
    existing_files = [f for f in os.listdir(SESSION_FOLDER) if f.startswith("session_conv_") and f.endswith(".json")]
    if not existing_files:
        return os.path.join(SESSION_FOLDER, "session_conv_1.json")
    numbers = [int(f.split("_")[-1].split(".")[0]) for f in existing_files]
    next_num = max(numbers) + 1 
    return os.path.join(SESSION_FOLDER, f"session_conv_{next_num}.json")  

def load_session(filename):
    filepath = os.path.join(SESSION_FOLDER, filename) 
    with open(filepath, "r", encoding="utf-8") as f: 
        try:
            data = json.load(f) 
            print(f"Session '{filename}' loaded successfully.") 
            return data
        except json.JSONDecodeError:
            print("Corrupted session file. Starting fresh.")  #if json file is not valid.
            return []
        
def save_session(messages, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4) #Converts the Python object (messages) into JSON format and writes it directly into the file object f. Adds 4 spaces before each nested level.
    print(f"Session saved successfully at {filepath}")  