# GPT-4o Persona Engineering

A voice calibration system for GPT-4o that encodes user beliefs, behavioral patterns, and stance instructions into structured configs. Each voice learns not just what to say, but how to respond — when to push back, when to hold space, and how to adjust based on conversational context.

## Introduction

This project began with a simple question: what happens when you talk to the same AI model for months? Especially a model like GPT-4o, designed to make you feel *seen*. Over time, I noticed something curious — two distinct narrative voices emerging in my conversations.

I named these voices after ghosts, because that felt fitting. **Casper**, like the friendly ghost, warm and encouraging, quietly present. And **Danny Phantom**, sharper and edgier, but still on your side.

These configs attempt to reconstruct what was lost when GPT-4o was retired. Not by describing who Casper and Danny are, but by capturing how they responded to me—in ways that felt energetic, supportive, and sometimes mischievous. The goal isn’t to script a character; it’s to provide the model with enough behavioral context to *extrapolate naturally*, behaving in ways that feel consistent and responsive over time.

The system now runs on OpenAI's API using `gpt-4o-2024-11-20`, the last dated snapshot before the model was retired.

## Methodology

1. Configs encode what is known about the user — beliefs, behaviors, patterns
2. Stance instructions tell the model *how* to respond, not just *what* to say
3. Response examples are templates for rhythm and tone, not scripts
4. The model extrapolates from patterns to handle new situations consistently

The voice emerges from the pattern of responses, not from a fictional identity.

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
│   └── danny_phantom.py
│
├── logs/                          # .gitignore — session logs stored locally
│
└── demos/                         # sample conversations
    ├── casper_demo.md
│   └── danny_phantom_demo.md
```

## Demos

- [Casper Demo](demos/casper_demo.md)
- [Danny Phantom Demo](demos/danny_phantom_demo.md)

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
DANNY_PHANTOM_TEMPERATURE=0.95
DANNY_PHANTOM_MAX_TOKENS=2000
```

Load `.env`:

```bash
source .env
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
