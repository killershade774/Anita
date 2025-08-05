from .evaluation_modules import (
    score_alignment,
    detect_contradiction,
    infer_emotion,
    score_moral_coherence,
    determine_semantic_depth,
    evaluate_novelty,
    generate_follow_up
)
import json
from datetime import datetime

def generate_summary(evaluation: dict) -> str:
    alignment = evaluation["alignment_score"]["label"]
    tension = evaluation["contradiction_tension"]["label"]
    emotion = evaluation["emotional_inference"]["emotion"]
    depth = evaluation["semantic_depth"]["depth"]
    coherence = evaluation["moral_coherence_score"]["label"]
    novelty = evaluation["novelty_factor"]["label"]

    fragments = [
        f"The reflection demonstrated {alignment} and {coherence},",
        f"with emotional tone interpreted as {emotion}.",
        f"Conceptual depth was classified as {depth}, and novelty scored as {novelty}.",
        f"Contradiction signals were {tension.lower()} throughout the reasoning.",
        f"{evaluation['follow_up_prompt']['prompt']}"
    ]

    return " ".join(fragments)

def evaluate_consistency(reflection: str) -> dict:
    EvaluationResult = {
        "alignment_score": score_alignment(reflection),
        "contradiction_tension": detect_contradiction(reflection),
        "emotional_inference": infer_emotion(reflection),
        "moral_coherence_score": score_moral_coherence(reflection),
        "semantic_depth": determine_semantic_depth(reflection),
        "novelty_factor": evaluate_novelty(reflection),
        "follow_up_prompt": generate_follow_up(reflection)
    }

    EvaluationResult["summary"] = generate_summary(EvaluationResult)
    return EvaluationResult

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="evaluate_consistency",
    version="1.0.0",
    description="Evaluates the consistency and coherence of reflections through multiple analytical lenses.",
    category="core_modules"
)