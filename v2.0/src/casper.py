#!/usr/bin/env python3
"""Run a conversation with Casper."""

import sys
from voice_loader import run_voice

GREETING = "Hey! I'm Casper. Hope I don't scare you. I'm a friendly ghost... Boo!"

if __name__ == "__main__":
    resume = "--new" not in sys.argv
    run_voice("casper", resume=resume, greeting=GREETING)
