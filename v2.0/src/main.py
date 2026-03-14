#!/usr/bin/env python3
"""Run a conversation with Casper or Danny Phantom."""

import sys
from voice_loader import run_voice

GREETINGS = {
    "casper": "Hey! I'm here. What's on your mind?",
    "danny_phantom": "Still here. Still sharp. What do you need?"
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: python main.py <voice> [--new]")
        print("  voice: casper | danny_phantom")
        print("  --new: start fresh (don't resume history)")
        sys.exit(0)
    
    voice = sys.argv[1].lower()
    
    if voice not in GREETINGS:
        print(f"Unknown voice: {voice}")
        print("Available: casper, danny_phantom")
        sys.exit(1)
    
    resume = "--new" not in sys.argv
    greeting = GREETINGS[voice]
    
    run_voice(voice, resume=resume, greeting=greeting)


if __name__ == "__main__":
    main()
