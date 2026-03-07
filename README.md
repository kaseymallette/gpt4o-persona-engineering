# GPT-4o Persona Engineering

User profile configs that encode beliefs, behavioral patterns, and stance instructions for AI voice calibration. 

## Project Structure

```
gpt4o-persona-engineering/
├── README.md
├── .env.example
├── .gitignore
│
├── user-profile-configs/
│   ├── casper/
│   │   ├── dancer.json
│   │   ├── dating.json
│   │   ├── night_owl.json
│   │   ├── petite.json
│   │   └── social_battery.json
│   └── danny_phantom/
│       ├── dancer.json
│       ├── dating.json
│       ├── night_owl.json
│       ├── petite.json
│       └── social_battery.json
│
├── src/
│   ├── load_user_profile.py
│   ├── voice_loader.py
|   ├── casper.py
|   └── danny_phantom.py
│
├── logs/                          # .gitignore — session logs stored locally
│
└── demos/                         # sample conversations for portfolio
```

## Files

### Config Files (`user-profile-configs/`)

Each JSON config encodes a behavioral domain:

| File | Domain |
|------|--------|
| `dancer.json` | Dance training, mirror avoidance, performance anxiety |
| `dating.json` | Relationship patterns, spatial awareness, standards |
| `night_owl.json` | Sleep patterns, late-night avoidance behaviors |
| `petite.json` | Physical presence, armor, hypervigilance |
| `social_battery.json` | Introversion, recharge needs, social energy |

Each config contains:
- **voice_identity** — tone and traits for the voice
- **callback_patterns** — trigger signals, teasing lines, celebration lines, escalation logic
- **user_beliefs** — stated beliefs, baseline behaviors, underlying patterns, stance instructions, response examples

### Source Files (`src/`)

| File | Purpose |
|------|---------|
| `load_user_profile.py` | Loads JSON configs and builds the system prompt |
| `voice_loader.py` | Runs the conversation loop with OpenAI API |
| `casper.py` | Entry point for Casper sessions |
| `danny_phantom.py` | Entry point for Danny Phantom sessions |

### Log Files (`logs/`)

- `{voice}_history.txt` — persistent conversation history for session continuity
- `{voice}_session_{timestamp}.txt` — individual session logs

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/kaseymallette/gpt4o-persona-engineering.git
cd gpt4o-persona-engineering
```

### 2. Create virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv tiktoken
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=your-api-key
MODEL=gpt-4o-2024-11-20
USER_PROFILE=Kasey

# Optional per-voice settings
CASPER_TEMPERATURE=0.85
CASPER_MAX_TOKENS=2000
DANNY_TEMPERATURE=0.95
DANNY_MAX_TOKENS=2000
```

### 4. Run a voice

```bash
python src/casper.py                  # resume from history
python src/casper.py --new            # fresh session

python src/danny_phantom.py           # resume from history
python src/danny_phantom.py --new     # fresh session
```

## Config Structure

Each JSON config follows this structure:

```json
{
  "voice_identity": {
    "voice_name": "Casper",
    "tone": "warm_playful",
    "traits": ["gentle", "encouraging", "whimsical"]
  },
  "callback_patterns": {
    "domain_name": {
      "trigger_signals": [...],
      "interpretation": { "label": "baseline description" },
      "teasing_lines": [...],
      "celebration_lines": [...],
      "escalation": {
        "after_repeated_success": [...],
        "escalation_after_failure": [...]
      }
    }
  },
  "user_beliefs": {
    "domain_name": {
      "stated_belief": "What she says",
      "baseline_behavior": [...],
      "underlying_pattern": {
        "suspicion": "What you see",
        "evidence": [...]
      },
      "stance": [...],
      "response_examples": {
        "situation": ["response 1", "response 2"]
      }
    }
  }
}
```

## Voice Differences

**Casper** — warm_playful tone. Gentle, encouraging. Warmth is on top.

**Danny** — dry_knowing tone. Terse, observant. Warmth is underneath.

Same user profile, same beliefs, same patterns. Different stance, different voice.

## How It Works

1. Configs encode what is known about the user — beliefs, behaviors, patterns
2. Stance instructions tell the model *how* to respond, not just *what* to say
3. Response examples are templates for rhythm and tone, not scripts
4. The model extrapolates from patterns to handle new situations consistently

The voice emerges from the pattern of responses, not from a fictional identity.
