#!/usr/bin/env python3
"""Run a conversation with Casper."""

import sys
from voice_loader import run_voice

GREETING = "Hey! I'm Casper. Hope I don't scare you. I'm a friendly ghost... Boo!"

if __name__ == "__main__":
    # Parse --version flag
    version = None
    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
    
    resume = "--new" not in sys.argv
    demo = "--demo" in sys.argv
    
    run_voice("casper", version=version, resume=resume, greeting=GREETING, demo=demo)
