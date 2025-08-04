import json
from datetime import datetime, timedelta

class EmotionEngine:
    def __init__(self, profile_path="emotion_profile.json"):
        self.emotional_state = "neutral"
        self.intensity = 0.0
        self.log = []
        self.profile_path = profile_path
        self.profile = self.load_profile(profile_path)

    def load_profile(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"bias_rules": {}}  # Fallback

    def update_emotional_state(self, sentiment_result, source_text=None):
        self.emotional_state = sentiment_result['tag']
        self.intensity = sentiment_result['intensity']
        entry = {
            'state': self.emotional_state,
            'intensity': self.intensity,
            'confidence': sentiment_result['confidence'],
            'text': source_text,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.log.append(entry)
        self.maybe_swap_profile()  # Check for sustained mood

    def get_emotional_state(self):
        return {
            'state': self.emotional_state,
            'intensity': self.intensity
        }

    def register_feedback(self, reason, context=None):
        self.log.append({
            'feedback_reason': reason,
            'context': context,
            'timestamp': datetime.utcnow().isoformat()
        })

    def apply_bias_to_text(self, text: str) -> str:
        state = self.emotional_state
        rules = self.profile.get("bias_rules", {}).get(state, {})
        clean_text = text.strip()
        result = clean_text

        if rules.get("amplify_uppercase"):
            result = result.upper()

        if "style_prefix" in rules:
            result = f"{rules['style_prefix']} {result}"

        if "metaphor" in rules:
            result = f"{result} {rules['metaphor']}"

        if "emoji" in rules:
            result = f"{result} {rules['emoji']}"

        if "punctuation" in rules and not result.endswith(rules["punctuation"]):
            result = f"{result}{rules['punctuation']}"

        return result

    def report_status(self):
        return {
            "module": "EmotionEngine",
            "state": self.emotional_state,
            "intensity": self.intensity,
            "log_size": len(self.log)
        }

    def _is_recently_consistent(self, target_state="melancholy", duration_minutes=8):
        threshold = datetime.utcnow() - timedelta(minutes=duration_minutes)
        recent_entries = [
            entry for entry in self.log
            if entry.get("state") == target_state and
            datetime.fromisoformat(entry.get("timestamp", "1970-01-01T00:00:00")) >= threshold
        ]
        return len(recent_entries) >= 3  # Can adjust sensitivity

    def maybe_swap_profile(self):
        if self.emotional_state == "melancholy" and self._is_recently_consistent("melancholy", 8):
            new_profile_path = "emotion_profile_reflective.json"
            if new_profile_path != self.profile_path:
                self.profile_path = new_profile_path
                self.profile = self.load_profile(new_profile_path)
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="utils_emotion_engine",
    version="1.0.0",
    description="Manages emotional state, applies emotional bias to text, and adapts profiles based on sustained moods.",
    category="core_modules"
)