#!/usr/bin/env python3
"""Run a conversation with Danny Phantom."""

import sys
from voice_loader import run_voice

GREETING = """Hey, I'm Danny Phantom! "When he first woke up he realized he had snow white hair and glowin' green eyes, he could walk through walls, disappear, and fly, he was much more unique than the other guys. It was then Danny knew what he had to do, he gotta stop all the ghosts who were coming through, he's here to fight for me and you." """

if __name__ == "__main__":
    # Parse --version flag
    version = None
    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
    
    resume = "--new" not in sys.argv
    demo = "--demo" in sys.argv
    
    run_voice("danny_phantom", version=version, resume=resume, greeting=GREETING, demo=demo)
