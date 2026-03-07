# === IMPORTS ===
import os
import datetime
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

from load_user_profile import load_all_configs, build_system_prompt

# === LOAD ENVIRONMENT ===
load_dotenv()
client = OpenAI()

# === PATHS ===
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "user-profile-configs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")


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

def run_voice(voice_key: str, resume: bool = True):
    """
    Main conversation loop.
    
    Args:
        voice_key: 'casper' or 'danny' — matches subdirectory in user-profile-configs/
        resume: If True, load previous conversation history
    """
    # Config
    user_name = os.getenv("USER_PROFILE", "KASEY").capitalize()
    model = os.getenv("MODEL", "gpt-4o")
    temperature = float(os.getenv(f"{voice_key.upper()}_TEMPERATURE", "0.9"))
    max_tokens = int(os.getenv(f"{voice_key.upper()}_MAX_TOKENS", "2000"))
    
    # Load configs
    configs = load_all_configs(CONFIG_DIR, voice_key)
    if not configs:
        print(f"No configs found for voice: {voice_key}")
        return
    
    # Get voice name from config
    first_config = configs[0]
    voice_identity = first_config.get("voice_identity", {})
    voice_name = voice_identity.get("voice_name", voice_key.capitalize())
    agent_name = voice_name
    
    # Build system prompt
    system_prompt = build_system_prompt(configs, voice_key)
    
    # Logging setup
    voice_log_dir = os.path.join(LOGS_DIR, voice_key)
    os.makedirs(voice_log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(voice_log_dir, f"{voice_key}_session_{timestamp}.txt")
    history_path = os.path.join(voice_log_dir, f"{voice_key}_history.txt")
    
    # Initialize messages
    if resume and os.path.exists(history_path):
        messages = load_previous_messages(history_path, agent_name, user_name)
        messages.insert(0, {"role": "system", "content": system_prompt})
        print(f"\n=== Resuming session with {agent_name} ===")
        print(f"Loaded {len(messages) - 1} previous messages")
    else:
        print(f"\n=== New session with {agent_name} ===")
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
        f.write(f"=== Session with {agent_name} ===\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Model: {model}\n")
        f.write(f"Temperature: {temperature}\n\n")
    
    # Get first reply
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
    resume = "--new" not in sys.argv
    
    print(f"Loading voice: {voice}")
    print(f"Resume: {resume}")
    
    run_voice(voice, resume=resume)
