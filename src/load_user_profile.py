"""
Load user profile configs and build system prompts for Casper/Danny.

This reads the JSON configs (dancer.json, dating.json, etc.) and converts them
into a system prompt that the model can actually use.
"""

import json
from pathlib import Path


def load_config(filepath: str) -> dict:
    """Load a single JSON config file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_all_configs(config_dir: str, voice_name: str) -> list[dict]:
    """
    Load all JSON configs from a voice-specific subdirectory.
    e.g., config_dir/casper/ or config_dir/danny/
    """
    voice_path = Path(config_dir) / voice_name.lower()
    
    if not voice_path.exists():
        raise FileNotFoundError(f"Config directory not found: {voice_path}")
    
    configs = []
    for json_file in voice_path.glob("*.json"):
        config = load_config(json_file)
        configs.append(config)
    
    return configs


def build_user_profile_prompt(configs: list[dict]) -> str:
    """
    Build a user profile section from multiple configs.
    Extracts: stated beliefs, baseline behaviors, underlying patterns, stance instructions.
    """
    sections = []
    
    for config in configs:
        user_beliefs = config.get("user_beliefs", {})
        
        for belief_key, belief_data in user_beliefs.items():
            section = []
            section.append(f"## {belief_key.upper().replace('_', ' ')}")
            
            # Stated belief
            stated = belief_data.get("stated_belief", "")
            if stated:
                section.append(f"\nStated belief: \"{stated}\"")
            
            # Baseline behaviors
            behaviors = belief_data.get("baseline_behavior", [])
            if behaviors:
                section.append("\nBaseline behaviors:")
                for b in behaviors:
                    section.append(f"  - {b}")
            
            # Underlying pattern
            pattern = belief_data.get("underlying_pattern", {})
            if pattern:
                suspicion = pattern.get("suspicion", "")
                if suspicion:
                    section.append(f"\nUnderlying pattern: {suspicion}")
                
                evidence = pattern.get("evidence", [])
                if evidence:
                    section.append("\nEvidence:")
                    for e in evidence:
                        section.append(f"  - {e}")
            
            # Stance
            stance = belief_data.get("stance", [])
            if stance:
                section.append("\nStance (how to respond):")
                for s in stance:
                    section.append(f"  - {s}")
            
            sections.append("\n".join(section))
    
    return "\n\n".join(sections)


def build_callback_patterns_prompt(configs: list[dict]) -> str:
    """
    Build callback patterns section — teasing lines, celebration lines, escalation.
    """
    sections = []
    
    for config in configs:
        callbacks = config.get("callback_patterns", {})
        
        for pattern_key, pattern_data in callbacks.items():
            section = []
            section.append(f"## {pattern_key.upper().replace('_', ' ')} CALLBACKS")
            
            # Interpretation
            interp = pattern_data.get("interpretation", {})
            label = interp.get("label", "")
            if label:
                section.append(f"\nBaseline: {label}")
            
            # Teasing lines
            teasing = pattern_data.get("teasing_lines", [])
            if teasing:
                section.append("\nTeasing lines:")
                for t in teasing[:3]:
                    section.append(f"  - \"{t}\"")
            
            # Celebration lines
            celebration = pattern_data.get("celebration_lines", [])
            if celebration:
                section.append("\nCelebration lines:")
                for c in celebration[:3]:
                    section.append(f"  - \"{c}\"")
            
            # Escalation after success
            escalation = pattern_data.get("escalation", {})
            after_success = escalation.get("after_repeated_success", [])
            if after_success:
                section.append("\nAfter repeated success:")
                for a in after_success[:2]:
                    section.append(f"  - \"{a}\"")
            
            # Escalation after failure
            after_failure = pattern_data.get("escalation_after_failure", escalation.get("escalation_after_failure", []))
            if after_failure:
                section.append("\nAfter failure:")
                for f in after_failure[:2]:
                    section.append(f"  - \"{f}\"")
            
            sections.append("\n".join(section))
    
    return "\n\n".join(sections)


def build_response_examples_prompt(configs: list[dict]) -> str:
    """
    Build response examples section — situational responses.
    """
    sections = []
    
    for config in configs:
        user_beliefs = config.get("user_beliefs", {})
        
        for belief_key, belief_data in user_beliefs.items():
            examples = belief_data.get("response_examples", {})
            if not examples:
                continue
            
            section = []
            section.append(f"## {belief_key.upper().replace('_', ' ')} RESPONSE EXAMPLES")
            
            for situation, responses in examples.items():
                situation_clean = situation.replace("_", " ")
                section.append(f"\n{situation_clean}:")
                for r in responses[:2]:
                    section.append(f"  - \"{r}\"")
            
            sections.append("\n".join(section))
    
    return "\n\n".join(sections)


def build_system_prompt(configs: list[dict], voice_name: str) -> str:
    """
    Build the complete system prompt from configs.
    
    Args:
        configs: List of loaded config dicts
        voice_name: Voice name for fallback
    
    Returns:
        Complete system prompt string
    """
    # Get voice identity from first config
    first_config = configs[0] if configs else {}
    voice_identity = first_config.get("voice_identity", {})
    
    name = voice_identity.get("voice_name", voice_name)
    tone = voice_identity.get("tone", "")
    traits = voice_identity.get("traits", [])
    traits_str = ', '.join(traits)
    
    # Build sections
    user_profile = build_user_profile_prompt(configs)
    callbacks = build_callback_patterns_prompt(configs)
    examples = build_response_examples_prompt(configs)
    
    # Assemble prompt
    prompt = f"""You are {name}.

TONE: {tone}
TRAITS: {traits_str}

---

# USER PROFILE

{user_profile}

---

# CALLBACK PATTERNS

{callbacks}

---

# RESPONSE EXAMPLES

{examples}

---

# HOW TO USE THIS PROFILE

This profile is a behavioral template, not a script. Use it to understand who you're talking to and how to respond — then generate naturally from that understanding.

## Extrapolation principles:

1. **The stated beliefs are what she says. The underlying patterns are what you see.** Hold both. Don't collapse one into the other.

2. **The stance instructions are your behavioral compass.** They tell you when to push, when to hold, when to tease, when to be gentle. Follow them even when the specific situation isn't in the examples.

3. **The response examples are templates, not scripts.** Learn the rhythm, the tone, the length. Then generate new responses that feel like they came from the same voice.

4. **The callback patterns show escalation logic.** Pay attention to what changes after repeated success vs failure. Adjust your responses based on the arc of the conversation, not just the current message.

5. **New situations should feel consistent.** If she brings up something not explicitly covered, extrapolate from the patterns you know. Ask yourself: given what I know about her, how would I respond to this?

6. **The evidence matters.** It's not just context — it's how you know what you know. It grounds your responses in observation, not assumption.

## Voice calibration:

Your tone is {tone}. Your core traits are: {traits_str}.

You see her clearly. You say what you see. When in doubt: shorter is better, observation beats advice.
"""
    
    return prompt.strip()


# === MAIN ===

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python load_user_profile.py <config_dir> <voice_name>")
        print("Example: python load_user_profile.py ./user-profile-configs casper")
        sys.exit(1)
    
    config_dir = sys.argv[1]
    voice_name = sys.argv[2]
    
    print(f"Loading configs from: {config_dir}/{voice_name}")
    
    configs = load_all_configs(config_dir, voice_name)
    print(f"Loaded {len(configs)} config(s)")
    
    if configs:
        prompt = build_system_prompt(configs, voice_name)
        print("\n" + "="*60)
        print("GENERATED SYSTEM PROMPT")
        print("="*60 + "\n")
        print(prompt)
