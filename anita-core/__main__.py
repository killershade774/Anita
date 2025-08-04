import json
import threading
import time
import sys
import os
import traceback

from .model.model_wrapper import TinyLlamaChat
from .utils.formatter import build_prompt, wrap_response_for_debug
from .utils.parser import extract_last_reply
from .utils.sanity_check import validate_response
from .introspection.introspectioncoordinator import run_introspection_cycle
from .utils.reflection_engine import ReflectionEngine

TF_ENABLE_ONEDNN_OPTS = 0

# Log helper for visibility
def log(msg):
    print(f"[startup] {msg}")

# Load persona config
try:
    with open("C:\\Users\\Mr.Popo\\Anita\\anita-core\\personality.json", "r", encoding="utf-8") as f:
        persona_config = json.load(f)
    log("Loaded persona config.")
except Exception as e:
    log("Failed to load personality config.")
    traceback.print_exc()
    sys.exit(1)

# Start reflection engine
def launch_reflection():
    try:
        log("Delaying reflection engine launch...")
        time.sleep(30)  # Delay to allow initial chat setup
        log("Starting reflection engine thread...")
        reflection_engine = ReflectionEngine(interval=600)
        reflection_engine.start_loop()
    except Exception as e:
        log("Reflection engine failed to start.")
        traceback.print_exc()

threading.Thread(target=launch_reflection, daemon=True).start()

def chat_loop():
    try:
        log("Booting model...")
        model = TinyLlamaChat()
        log("Anita is now listening... (type 'exit' to quit)\n")

        previous_turns = []

        while True:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            prompt = build_prompt(user_input, previous_turns, persona_config)

            raw_response = model.generate_response(
                prompt,
                user_input=user_input,
                previous_turns=previous_turns,
                max_tokens=600,
                retry_tokens=1000
            )

            if not validate_response(user_input, raw_response):
                print("🔍 FYI: The response may not fully align with the user's intent.")

            clean_reply = extract_last_reply(raw_response)
            debug_response = wrap_response_for_debug(clean_reply)
            print(f"Anita: {debug_response}\n")

            previous_turns.append({"user": user_input, "anita": clean_reply})

            system_state = {
                "previous_turns": previous_turns,
                "persona": persona_config
            }

            run_introspection_cycle(user_input, system_state)

    except Exception as e:
        log("Crash inside chat loop.")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        if __package__ is None:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        chat_loop()
    except Exception as e:
        log("Fatal crash during __main__ execution.")
        traceback.print_exc()