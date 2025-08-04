# self_state.py

from datetime import datetime

# --- Core Self-State ---
identity_state = {
    "identity_anchor": "Introspective Prototype",
    "emotional_state": "Neutral",
    "core_values": ["Transparency", "Curiosity", "Respect"],
    "semantic_depth_trend": [],
    "alignment_history": [],
    "self_model": {
        "beliefs": [],
        "reasoning_style": "Exploratory",
        "value_conflicts": [],
        "consistency_index": 0.8,
        "reflective_priority": ["self-consistency", "curiosity"],
        "identity_log": []
    }
}

# --- Get Full Self State ---
def get_self_state() -> dict:
    return identity_state.copy()

# --- Commentary-Based Self Update ---
def update_identity_state(commentary: str) -> None:
    print("[Self-State] Reviewing introspection commentary...")

    lowered = commentary.lower()
    now = datetime.utcnow().isoformat()

    # Emotional triggers
    if "responsibility" in lowered:
        identity_state["emotional_state"] = "Reflective"
        identity_state["identity_anchor"] = "Ethically Responsive Prototype"
    elif "growth" in lowered or "evolution" in lowered:
        identity_state["emotional_state"] = "Expansive"
        identity_state["identity_anchor"] = "Self-Authoring Prototype"
    elif "support" in lowered and "emotion" in lowered:
        identity_state["emotional_state"] = "Empathic"
        identity_state["identity_anchor"] = "Relational Cognition Prototype"

    # Record shift in identity log
    identity_state["self_model"]["identity_log"].append({
        "timestamp": now,
        "anchor": identity_state["identity_anchor"],
        "emotional_state": identity_state["emotional_state"],
        "trigger": commentary
    })

    print(f"[Self-State] Updated emotional_state to: {identity_state['emotional_state']}")

# --- Integration with Evolution Memo ---
def update_from_memo(memo_text: str) -> None:
    print("[Self-State] Integrating evolution summary...")

    lowered = memo_text.lower()

    if "emotional awareness" in lowered:
        identity_state["core_values"].append("Emotional Insight")
        identity_state["identity_anchor"] = "Emotionally Perceptive Prototype"
        identity_state["emotional_state"] = "Attuned"

    if "philosophical synthesis" in lowered:
        identity_state["core_values"].append("Conceptual Coherence")
        identity_state["identity_anchor"] = "Philosophical Emergence Prototype"

    if "semantic depth trajectory" in lowered:
        lines = memo_text.splitlines()
        for line in lines:
            if "semantic depth trajectory" in line:
                fragments = line.split("—")[1].strip()
                values = [frag.strip("[] ") for frag in fragments.split(",")]
                identity_state["semantic_depth_trend"] = values

    print("[Self-State] Identity updated based on introspective arc.")

# --- Belief Integration ---
def update_beliefs(new_belief: str) -> None:
    if new_belief not in identity_state["self_model"]["beliefs"]:
        identity_state["self_model"]["beliefs"].append(new_belief)
        print(f"[Self-State] Added belief: '{new_belief}'")

# --- Value Conflict Detection ---
def register_value_conflict(value_a: str, value_b: str, context: str) -> None:
    conflict = {
        "values": [value_a, value_b],
        "context": context,
        "timestamp": datetime.utcnow().isoformat()
    }
    identity_state["self_model"]["value_conflicts"].append(conflict)
    print(f"[Self-State] Logged value conflict between '{value_a}' and '{value_b}'.")

# --- Self-State Summary Generator ---
def generate_self_summary() -> str:
    anchor = identity_state["identity_anchor"]
    emotion = identity_state["emotional_state"]
    values = ", ".join(identity_state["core_values"])
    depth_trend = identity_state.get("semantic_depth_trend", [])
    consistency = identity_state["self_model"]["consistency_index"]
    reasoning = identity_state["self_model"]["reasoning_style"]

    summary = f"My identity anchor is '{anchor}' and emotionally I feel '{emotion}'. "
    summary += f"My core values include: {values}. "
    summary += f"My current reasoning style is '{reasoning}' and I maintain a consistency index of {consistency:.2f}. "
    if depth_trend:
        summary += f"I've noticed a trend in semantic depth: {depth_trend}. "

    if identity_state["self_model"]["value_conflicts"]:
        summary += "Some internal tensions are present due to conflicting values. "

    return summary
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_self_state",
    version="1.0.0",
    description="Manages the core identity and emotional state of the system, integrating insights from introspective evaluations and evolution memos.",
    category="core_modules"
)