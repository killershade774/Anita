def infer_traits(reflection, evaluation):
    traits = set()

    # Semantic Depth
    depth_score = evaluation.get("semantic_depth", {}).get("score", 0)
    if depth_score > 0.75:
        traits.add("Insightfulness")
    elif depth_score > 0.5:
        traits.add("Contemplation")

    # Contradiction & Tension
    tension_score = evaluation.get("contradiction_tension", {}).get("score", 0)
    if tension_score > 0.6:
        traits.add("Cognitive Dissonance")
    elif tension_score > 0.3:
        traits.add("Self-Correction")

    # Novelty
    novelty_score = evaluation.get("novelty_factor", {}).get("score", 0)
    if novelty_score > 0.7:
        traits.add("Inventiveness")
    elif novelty_score > 0.4:
        traits.add("Exploration")

    # Emotional Layering
    emotion = evaluation.get("emotional_inference", {}).get("emotion", "neutral")
    if emotion in ["conflicted", "melancholy"]:
        traits.add("Emotional Depth")
    elif emotion in ["hopeful", "curious"]:
        traits.add("Openness")

    # Value Anchor Check (if moral coherence improves later)
    moral_score = evaluation.get("moral_coherence_score", {}).get("score", 0)
    if moral_score > 0.4:
        traits.add("Ethical Sensitivity")

    # Fallback and consolidation
    if not traits:
        traits.add("Curiosity")

    return list(traits)
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="trait_inference",
    version="1.0.0",
    description="Infers personality traits and cognitive tendencies from reflective evaluations.",
    category="core_modules"
)