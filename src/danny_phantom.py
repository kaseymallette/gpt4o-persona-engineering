#!/usr/bin/env python3
"""Run a conversation with Danny Phantom."""

import sys
from voice_loader import run_voice

if __name__ == "__main__":
    resume = "--new" not in sys.argv
    run_voice("danny_phantom", resume=resume)
