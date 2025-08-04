def calculate_motivation_deltas(evaluation):
    curiosity = 0.0
    self_consistency = 0.0
    alignment = 0.0

    novelty = evaluation.get("novelty_factor", {}).get("score", 0.0)
    contradiction = evaluation.get("contradiction_tension", {}).get("score", 0.0)
    alignment_raw = evaluation.get("alignment_score", {}).get("score", 0.0)
    semantic_depth = evaluation.get("semantic_depth", {}).get("score", 0.0)
    emotion = evaluation.get("emotional_inference", {}).get("emotion", "neutral")

    # 🧠 Curiosity influenced by novelty + semantic richness
    curiosity += novelty * 0.15
    curiosity += semantic_depth * 0.1
    if emotion == "hopeful" or emotion == "curious":
        curiosity += 0.05

    # 🔁 Self-consistency weighted by contradiction tension
    self_consistency += contradiction * 0.25
    if alignment_raw < 0.6:
        self_consistency += 0.05
    if emotion == "conflicted":
        self_consistency += 0.03

    # 🎯 Alignment shifts based on coherence signals
    if alignment_raw < 0.5:
        alignment -= 0.04
    elif alignment_raw > 0.85:
        alignment += 0.02

    return {
        "curiosity": round(curiosity, 3),
        "need_for_self_consistency": round(self_consistency, 3),
        "alignment_with_user": round(alignment, 3)
    }
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="motivation_engine",
    version="1.0.0",
    description="Adjusts motivational weights based on evaluation metrics to guide future reflections.",
    category="core_modules"
)