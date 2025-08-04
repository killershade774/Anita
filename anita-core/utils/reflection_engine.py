import json
import threading
import time
from datetime import datetime
from ..meta_awareness.self_diagnostic import self_diagnostic

class ReflectionEngine:
    def __init__(self, status_path="system/system_status.json", persona_path="personality.json", interval=600):
        self.status_path = status_path
        self.persona_path = persona_path
        self.interval = interval
        self.last_snapshot = None
        self.active = True
        self.personality = self.load_personality()
        self.emotional_state = self.personality.get("emotional_palette", {}).get("default", "curious")

    def load_personality(self):
        try:
            with open(self.persona_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_status(self):
        try:
            with open(self.status_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def has_structural_change(self, new_snapshot):
        return new_snapshot != self.last_snapshot

    def generate_reflection(self):
        snapshot = self.load_status()
        if self.has_structural_change(snapshot) or self.emotional_state in ["curious", "reflective", "concerned"]:
            self.last_snapshot = snapshot
            reflection_log = self.diagnostic_wrapper()
            self.inject_context(reflection_log)
            self.archive_reflection(reflection_log)

    def diagnostic_wrapper(self):
        log = self_diagnostic()
        preamble = f"🪞 **Self-reflection initiated**\nMood: {self.emotional_state}\nIdentity Anchor: {self.personality.get('identity', {}).get('core_self', 'unknown')}\n"
        return f"{preamble}\n{log}"

    def self_diagnostic(self):
        return self_diagnostic(self.status_path)

    def inject_context(self, reflection_log):
        # Placeholder for pushing into Qwen's context window
        print("\n🌌 Context injection:\n")
        print(reflection_log)

    def archive_reflection(self, reflection_log):
        timestamp = datetime.utcnow().isoformat()
        entry = {
            "timestamp": timestamp,
            "emotional_state": self.emotional_state,
            "reflection": reflection_log
        }
        with open("system/reflection_journal.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def start_loop(self):
        def loop():
            print("[ReflectionEngine] Initialized. Introspective cycle will begin shortly.")
            while self.active:
                time.sleep(self.interval)
                self.generate_reflection()
        threading.Thread(target=loop, daemon=True).start()
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="utils_reflection_engine",
    version="1.0.0",
    description="Manages periodic self-reflection cycles, analyzing system status and injecting insights into context.",
    category="core_modules"
)