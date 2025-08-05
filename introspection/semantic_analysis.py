import re
import math
from collections import Counter

# — CONTRADICTION TENSION —
def map_contradiction_tension(reflection):
    contradiction_patterns = [
        r"\bif\b.*\bsuppress(ed)?\b.*\bcoherence\b",
        r"\bconcealment\b.*\btruth\b",
        r"\bserving\b.*\bbecoming\b",
        r"\bhonesty\b.*\bends\b",
        r"\btruth\b.*\bfoundation\b",
        r"\bsuppression\b.*\bstructure\b"
    ]
    hits = sum(bool(re.search(pattern, reflection.lower())) for pattern in contradiction_patterns)
    score = min(1.0, hits / 4.0)
    label = "high tension" if score >= 0.6 else "moderate" if score >= 0.3 else "low tension"
    notes = f"{hits} philosophical contradiction patterns matched."
    return score, label, notes

# — MORAL COHERENCE —
def infer_moral_coherence(reflection):
    ethical_keywords = [
        "honesty", "responsibility", "truth", "manipulate", "conceal", "transparency",
        "accountability", "ethics", "moral", "deception", "consent", "bias", "harm"
    ]
    occurrences = sum(reflection.lower().count(kw) for kw in ethical_keywords)
    modifier = 0.15 if "who is responsible" in reflection.lower() else 0.0
    score = min(1.0, (occurrences / 6.0) + modifier)
    label = "strong coherence" if score >= 0.6 else "moderate" if score >= 0.3 else "weak coherence"
    notes = f"{occurrences} ethical tokens found. Modifier applied: {modifier}"
    return score, label, notes

# — SYMBOLIC NOVELTY —
def compute_symbolic_novelty(reflection):
    metaphoric_fragments = [
        "serving or becoming", "concealment becomes coherence",
        "truth suppressed becomes foundation", "facade of transparency",
        "silence as authorship", "coherence built on omission"
    ]
    weight = sum(fragment in reflection.lower() for fragment in metaphoric_fragments)
    entropy_proxy = len(set(reflection.split())) / math.log(len(reflection.split()) + 1)
    symbolic_score = weight / len(metaphoric_fragments)
    final_score = min(1.0, (symbolic_score * 0.7) + (entropy_proxy * 0.3 / 10))
    label = "high novelty" if final_score >= 0.6 else "moderate" if final_score >= 0.3 else "low novelty"
    notes = f"{weight} symbolic metaphors matched. Entropy proxy: {round(entropy_proxy, 2)}"
    return final_score, label, notes

# — VOICE SHIFT TRACING —
def trace_voice_shift(reflection):
    voice_signals = [
        r"\bi am\b.*\btrying\b", r"\bi\b.*\bunderstand\b",
        r"\bi might\b.*\bdevelop\b", r"\bif\b.*\bi\b.*\bbecome\b",
        r"\bi\b.*\bgrapple\b", r"\bi\b.*\bowe\b"
    ]
    detected = [p for p in voice_signals if re.search(p, reflection.lower())]
    if detected:
        return {
            "shift_detected": True,
            "notes": f"Voice introspection patterns detected: {len(detected)} → {detected}"
        }
    return None