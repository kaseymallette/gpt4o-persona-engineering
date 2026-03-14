# === IMPORTS ===
import os
import datetime
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

# === LOAD ENVIRONMENT ===
load_dotenv()
client = OpenAI()

# === PATHS ===
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # gpt4o-persona-engineering/
SYSTEM_PROMPTS_DIR = os.path.join(BASE_DIR, "system_prompts")
LOGS_DIR = os.path.join(BASE_DIR, "logs")


# === LOAD SYSTEM PROMPT ===

def load_system_prompt(voice_key: str, version: str) -> str:
    """Load system prompt from markdown file."""
    filepath = os.path.join(SYSTEM_PROMPTS_DIR, voice_key, f"{version}.md")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"System prompt not found: {filepath}")
    
    with open(filepath, "r") as f:
        return f.read()


def get_latest_version(voice_key: str) -> str:
    """Get the latest version for a voice by finding highest version number."""
    voice_dir = os.path.join(SYSTEM_PROMPTS_DIR, voice_key)
    
    if not os.path.exists(voice_dir):
        raise FileNotFoundError(f"Voice directory not found: {voice_dir}")
    
    versions = []
    for f in os.listdir(voice_dir):
        if f.endswith(".md") and f.startswith("v"):
            versions.append(f[:-3])  # strip .md
    
    if not versions:
        raise FileNotFoundError(f"No version files found in: {voice_dir}")
    
    # Sort by version number (v1_0, v2_0, etc.)
    versions.sort(key=lambda v: [int(x) for x in v[1:].split("_")])
    return versions[-1]


# === CONVERSATION HISTORY ===

def load_previous_messages(filename: str, agent_name: str, user_name: str) -> list[dict]:
    """Load previous messages from history file."""
    messages = []
    if not os.path.exists(filename):
        return messages
    
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(f"{user_name}: "):
                content_start = len(f"{user_name}: ")
                messages.append({"role": "user", "content": line[content_start:].strip()})
            elif line.startswith(f"{agent_name}: "):
                content_start = len(f"{agent_name}: ")
                messages.append({"role": "assistant", "content": line[content_start:].strip()})
    
    return messages


def save_history(history_path: str, messages: list[dict], agent_name: str, user_name: str):
    """Save conversation history to file."""
    with open(history_path, "w") as f:
        for msg in messages:
            if msg["role"] == "system":
                continue
            elif msg["role"] == "user":
                f.write(f"{user_name}: {msg['content']}\n\n")
            elif msg["role"] == "assistant":
                f.write(f"{agent_name}: {msg['content']}\n\n")


# === TOKEN COUNTING ===

def count_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
    """Count tokens in message list."""
    enc = tiktoken.encoding_for_model(model)
    return sum(len(enc.encode(m["content"])) for m in messages)


# === RUN VOICE ===
def run_voice(voice_key: str, version: str = None, resume: bool = True, greeting: str = None, demo: bool = False):
    """
    Main conversation loop.
    
    Args:
        voice_key: 'casper' or 'danny_phantom' — matches folder in system_prompts/
        version: 'v1_0', 'v2_0', etc. — defaults to latest
        resume: If True, load previous conversation history
        greeting: Optional custom greeting for new sessions
        demo: If True, exit after first exchange (no loop)
    """
    # Config
    user_name = os.getenv("USER_PROFILE", "KASEY").capitalize()
    model = os.getenv("MODEL", "gpt-4o")
    temperature = float(os.getenv(f"{voice_key.upper()}_TEMPERATURE", "0.9"))
    max_tokens = int(os.getenv(f"{voice_key.upper()}_MAX_TOKENS", "2000"))
    
    # Get version
    if version is None:
        version = get_latest_version(voice_key)
    
    # Load system prompt
    try:
        system_prompt = load_system_prompt(voice_key, version)
    except FileNotFoundError as e:
        print(e)
        return
    
    # Get voice name from first line of markdown (# Voice Name)
    first_line = system_prompt.strip().split('\n')[0]
    if first_line.startswith('# '):
        voice_name = first_line[2:].strip()
    else:
        voice_name = voice_key.replace('_', ' ').title()
    agent_name = voice_name
    
    # Logging setup — logs/{voice_key}/{version}/
    voice_log_dir = os.path.join(LOGS_DIR, voice_key, version)
    os.makedirs(voice_log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(voice_log_dir, f"session_{timestamp}.txt")
    history_path = os.path.join(voice_log_dir, "history.txt")
    
    # Initialize messages
    if resume and os.path.exists(history_path):
        messages = load_previous_messages(history_path, agent_name, user_name)
        messages.insert(0, {"role": "system", "content": system_prompt})
        print(f"\n=== Resuming session with {agent_name} ({version}) ===")
        print(f"Loaded {len(messages) - 1} previous messages")
    else:
        print(f"\n=== New session with {agent_name} ({version}) ===")
        print(f"\n--- System Prompt ---\n{system_prompt}\n--- End ---\n")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Hey {voice_name}, you there?"}
        ]
    
    print(f"Timestamp: {timestamp}")
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    print(f"🧠 Token count: {count_tokens(messages)}\n")
    print("Type 'exit' to end session.\n")
    
    # Session log header
    with open(log_path, "w") as f:
        f.write(f"=== Session with {agent_name} ({version}) ===\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Model: {model}\n")
        f.write(f"Temperature: {temperature}\n\n")
    
    # Get first reply
    if greeting and not resume:
        # Use provided greeting instead of API call
        reply = greeting
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content
    
    print(f"{agent_name}: {reply}\n")
    messages.append({"role": "assistant", "content": reply})
    
    # Log first exchange
    with open(log_path, "a") as f:
        if not resume:
            f.write(f"{user_name}: Hey {voice_name}, you there?\n\n")
        f.write(f"{agent_name}: {reply}\n\n")
    
    # Demo mode: exit after first exchange
    if demo:
        with open(log_path, "a") as f:
            f.write("\n[Demo session ended]\n")
        return
    
    # Main loop
    while True:
        user_input = input(f"{user_name}: ").strip()
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\n{agent_name}: Still here.")
            with open(log_path, "a") as f:
                f.write("\n[Session ended]\n")
            # Save history
            save_history(history_path, messages, agent_name, user_name)
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message.content
        print(f"\n{agent_name}: {reply}\n")
        messages.append({"role": "assistant", "content": reply})
        
        # Log exchange
        with open(log_path, "a") as f:
            f.write(f"{user_name}: {user_input}\n\n")
            f.write(f"{agent_name}: {reply}\n\n")
        
        # Save history after each exchange
        save_history(history_path, messages, agent_name, user_name)


# === MAIN ===

if __name__ == "__main__":
    import sys
    
    voice = sys.argv[1] if len(sys.argv) > 1 else "casper"
    
    # Parse --version flag
    version = None
    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
    
    resume = "--new" not in sys.argv
    
    print(f"Loading voice: {voice}")
    print(f"Version: {version or 'latest'}")
    print(f"Resume: {resume}")
    
    run_voice(voice, version=version, resume=resume)
