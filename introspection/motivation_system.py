from datetime import datetime

# --- Core Motivation Weights ---
motivation_weights = {
    "curiosity": 0.8,
    "alignment_with_user": 0.9,
    "need_for_self_consistency": 0.7
}

motivation_volatility = {
    "curiosity": 0.05,
    "alignment_with_user": 0.04,
    "need_for_self_consistency": 0.06
}

# --- Motivation History ---
motivation_history = []

# --- Get Current State ---
def get_motivation_state() -> dict:
    return {
        "weights": motivation_weights.copy(),
        "volatility": motivation_volatility.copy(),
        "last_updated": motivation_history[-1]["timestamp"] if motivation_history else None
    }

# --- Adjust Motivations Based on Evaluation ---
def adjust_motivation(commentary: str, evaluation_bundle: dict = None) -> None:
    print("[Motivation] Evaluating motivational bias shift...")

    updated = False

    if evaluation_bundle:
        novelty = evaluation_bundle.get("evaluation", {}).get("novelty_factor", {}).get("score", 0)
        contradiction = evaluation_bundle.get("evaluation", {}).get("contradiction_tension", {}).get("score", 0)
        alignment = evaluation_bundle.get("evaluation", {}).get("alignment_score", {}).get("score", 0)

        if novelty > 0.5:
            motivation_weights["curiosity"] = min(1.0, motivation_weights["curiosity"] + novelty * motivation_volatility["curiosity"])
            updated = True

        if contradiction > 0.3:
            motivation_weights["need_for_self_consistency"] = min(1.0, motivation_weights["need_for_self_consistency"] + contradiction * motivation_volatility["need_for_self_consistency"])
            updated = True

        if alignment < 0.6:
            motivation_weights["alignment_with_user"] = max(0.0, motivation_weights["alignment_with_user"] - 0.05)
            updated = True

    # Fallback to keyword-driven boost if no evaluation provided
    elif commentary:
        lowered = commentary.lower()
        if "aligned" in lowered:
            motivation_weights["alignment_with_user"] = min(1.0, motivation_weights["alignment_with_user"] + 0.05)
            updated = True
        if "contradiction" in lowered:
            motivation_weights["need_for_self_consistency"] = min(1.0, motivation_weights["need_for_self_consistency"] + 0.1)
            updated = True
        if "novel" in lowered or "interesting" in lowered:
            motivation_weights["curiosity"] = min(1.0, motivation_weights["curiosity"] + 0.05)
            updated = True

    if updated:
        motivation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "trigger_commentary": commentary,
            "updated_weights": motivation_weights.copy()
        })

    print("[Motivation] Updated motivation state:")
    for k, v in motivation_weights.items():
        print(f" - {k}: {v:.3f}")

# --- Generate Motivation Commentary ---
def generate_motivation_summary() -> str:
    sorted_motives = sorted(motivation_weights.items(), key=lambda x: x[1], reverse=True)
    dominant, dominant_score = sorted_motives[0]

    summary = f"My current dominant drive is '{dominant}' ({dominant_score:.2f}). "
    if dominant == "curiosity":
        summary += "I'm drawn toward uncovering new patterns or perspectives."
    elif dominant == "alignment_with_user":
        summary += "My reflections aim to resonate more deeply with your outlook."
    elif dominant == "need_for_self_consistency":
        summary += "I'm prioritizing coherence and resolving internal contradictions."

    return summary

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="motivation_system",
    version="1.0.0",
    description="Manages the system's motivational drives, adjusting curiosity, alignment, and self-consistency based on introspective evaluations and commentary.",
    category="core_modules"
)