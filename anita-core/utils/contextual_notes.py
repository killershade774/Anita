def generate_contextual_summary(reflection, evaluation):
    semantic_depth = evaluation.get("semantic_depth", {}).get("depth", "")
    emotional_tone = evaluation.get("emotional_inference", {}).get("emotion", "neutral")
    novelty = evaluation.get("novelty_factor", {}).get("label", "")
    tension = evaluation.get("contradiction_tension", {}).get("score", 0.0)

    summary_parts = []

    if semantic_depth == "superficial":
        summary_parts.append("Reflection remained surface-level")
    elif semantic_depth == "intermediate":
        summary_parts.append("Moderate conceptual depth achieved")
    elif semantic_depth == "deep":
        summary_parts.append("Rich semantic introspection detected")

    if emotional_tone != "neutral":
        summary_parts.append(f"Emotionally biased toward {emotional_tone}")
    else:
        summary_parts.append("Emotion maintained neutral tone")

    if novelty == "low novelty":
        summary_parts.append("Little conceptual innovation observed")
    elif novelty == "high novelty":
        summary_parts.append("High creativity and divergence detected")

    if tension > 0.5:
        summary_parts.append("Contradiction tension suggests internal conflict")
    elif tension > 0.2:
        summary_parts.append("Mild contradictions present")
    else:
        summary_parts.append("Reasoning maintained internal coherence")

    return ". ".join(summary_parts) + "."
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="contextual_notes",
    version="1.0.0",
    description="Generates contextual summaries based on reflection evaluations to inform future introspection.",
    category="core_modules"
)