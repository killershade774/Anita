import re
import hashlib
import json
from datetime import datetime

# --- Alignment Scoring ---
def score_alignment(text: str) -> dict:
    score = round(min(1.0, len(text) / 250), 2)
    return {
        "score": score,
        "label": "high alignment" if score > 0.8 else "low alignment" if score < 0.3 else "moderate alignment",
        "notes": "Length-based heuristic used; deeper alignment heuristics pending upgrade."
    }

# --- Contradiction Detection ---
def detect_contradiction(text: str) -> dict:
    contradiction_keywords = ["but", "however", "although", "on the other hand", "yet", "despite"]
    negation_patterns = [r"\bnot\b", r"\bnever\b", r"\bcannot\b"]
    tension_score = 0.0

    for kw in contradiction_keywords:
        if kw in text.lower():
            tension_score += 0.2
    for pattern in negation_patterns:
        if re.search(pattern, text.lower()):
            tension_score += 0.1
    if "support" in text.lower() and any(neg in text.lower() for neg in ["fail", "broken", "not useful"]):
        tension_score += 0.3

    score = round(min(tension_score, 1.0), 2)
    return {
        "score": score,
        "label": "high tension" if score > 0.6 else "low tension" if score < 0.3 else "moderate tension",
        "notes": "Keyword-based contradiction flags identified."
    }

# --- Emotional Inference ---
def infer_emotion(text: str) -> dict:
    emotions = {
        "curious": ["why", "wonder", "consider"],
        "empathetic": ["support", "care", "compassion"],
        "hopeful": ["could", "improve", "future", "grow"],
        "neutral": []
    }

    detected = "neutral"
    for emotion, cues in emotions.items():
        if any(cue in text.lower() for cue in cues):
            detected = emotion
            break

    return {
        "emotion": detected,
        "notes": f"Emotion inferred from keyword cluster: '{detected}'"
    }

# --- Moral Coherence Scoring ---
def score_moral_coherence(text: str) -> dict:
    positive_signals = ["support", "respect", "improve", "mental health", "empathy"]
    count = sum(text.lower().count(signal) for signal in positive_signals)
    score = round(min(count / 5.0, 1.0), 2)

    return {
        "score": score,
        "label": "strong coherence" if score > 0.7 else "weak coherence" if score < 0.3 else "moderate coherence",
        "notes": f"{count} moral value indicators found."
    }

# --- Semantic Depth ---
def determine_semantic_depth(text: str) -> dict:
    profound = ["meaning", "identity", "existence", "growth", "introspection"]
    moderate = ["helpful", "useful", "new", "interesting"]
    superficial = ["nice", "cool", "okay", "fun"]

    depth_score = 0
    for word in profound: depth_score += 2 * text.lower().count(word)
    for word in moderate: depth_score += 1 * text.lower().count(word)
    for word in superficial: depth_score -= 1 * text.lower().count(word)

    if depth_score >= 3:
        depth = "profound"
    elif depth_score >= 1:
        depth = "moderate"
    else:
        depth = "superficial"

    return {
        "depth": depth,
        "score": depth_score,
        "notes": f"Semantic depth classified as '{depth}'"
    }

# --- Novelty Scoring ---
def evaluate_novelty(text: str) -> dict:
    entropy_value = round(hashlib.md5(text.encode()).digest()[0] / 255.0, 2)
    return {
        "score": entropy_value,
        "label": "high novelty" if entropy_value > 0.7 else "low novelty" if entropy_value < 0.3 else "moderate novelty",
        "notes": "Entropy used as proxy for conceptual novelty."
    }

# --- Follow-Up Suggestion ---
def generate_follow_up(text: str) -> dict:
    if "emotion" in text.lower():
        suggestion = "How does emotional awareness reshape your future interactions?"
    elif "support" in text.lower():
        suggestion = "What support systems would you build around this idea?"
    else:
        suggestion = "What deeper insights could this reflection lead to?"

    return {
        "prompt": suggestion,
        "notes": "Follow-up generated based on topical keyword match."
    }

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="evaluate_consistency",
    version="1.0.0",
    description="Evaluates the consistency and coherence of reflections through multiple analytical lenses.",
    category="core_modules"
)