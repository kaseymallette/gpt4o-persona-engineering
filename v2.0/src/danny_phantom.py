#!/usr/bin/env python3
"""Run a conversation with Danny Phantom."""

import sys
from voice_loader import run_voice

GREETING = "Hey, Danny Phantom here. What's up, trouble? I know you're up to something...you always are."

if __name__ == "__main__":
    resume = "--new" not in sys.argv
    run_voice("danny_phantom", resume=resume, greeting=GREETING)
