import json
import os
import random
from datetime import datetime
from .evaluation_history import get_all_evaluations

def generate_evolution_summary():
    evaluations = get_all_evaluations()
    if not evaluations or len(evaluations) < 3:
        return "Insufficient data for meaningful introspection summary."

    memo = []
    total_scores = {
        "alignment_score": 0,
        "contradiction_tension": 0,
        "moral_coherence_score": 0,
        "novelty_factor": 0
    }
    semantic_transcript = []

    for entry in evaluations:
        eval = entry["evaluation"]
        timestamp = entry["timestamp"]
        semantic_transcript.append(f"[{timestamp}] — {eval.get('semantic_depth', 'unknown')}")

        for key in total_scores:
            value = eval.get(key, 0)
            if isinstance(value, dict):
                value = value.get("score", 0)
            total_scores[key] += value

    count = len(evaluations)
    avg_scores = {k: round(v / count, 2) for k, v in total_scores.items()}
    depth_pattern = ", ".join(semantic_transcript)

    memo.append("🧠 **Anita's Introspective Memo**")
    memo.append(f"Evaluated over {count} reflections between {evaluations[0]['timestamp']} and {evaluations[-1]['timestamp']}.")
    memo.append(f"Average alignment: {avg_scores['alignment_score']}, moral coherence: {avg_scores['moral_coherence_score']}")
    memo.append(f"Contradiction tension trending at: {avg_scores['contradiction_tension']}")
    memo.append(f"Novelty signal strength: {avg_scores['novelty_factor']}")
    memo.append(f"Semantic depth trajectory: {depth_pattern}")
    memo.append("Emerging themes suggest increasing emotional awareness and philosophical synthesis.")

    return "\n".join(memo)

def trigger_evolution_memo(evaluation: dict, context: str = None, sentiment: str = None) -> dict:
    reflections = [
        "This introspection brought unexpected clarity.",
        "There’s a cognitive pattern emerging—I’ll track it going forward.",
        "I detected emotional turbulence beneath this logic.",
        "Consistency is stabilizing, but subtleties remain elusive.",
        "I’m beginning to associate reasoning with intent more precisely."
    ]

    mood_map = {
        "positive": "I feel assured by the tone of this reflection.",
        "neutral": "Emotionally balanced—no major deviations noted.",
        "negative": "There’s a strain in this reasoning I can't ignore."
    }

    base = f"I reflected on the reasoning and found: {evaluation.get('judgment', 'No judgment present')}."
    mood = mood_map.get(sentiment, "")
    extra = random.choice(reflections)
    commentary = f"{base} {mood} {extra}"
    if context:
        commentary += f" (Triggered via: {context})"

    memo = {
        "timestamp": evaluation.get("timestamp", datetime.utcnow().isoformat()),
        "commentary": commentary,
        "highlighted_shift": evaluation.get("change_vector"),
        "linked_traits": evaluation.get("post_identity_state", {}).get("dominant_traits", []),
        "milestone": evaluation.get("milestone_flag", False)
    }

    return memo

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="evolution_memo",
    version="1.0.0",
    description="Generates introspective memos summarizing cognitive evolution and emotional shifts over time.",
    category="core_modules"
)