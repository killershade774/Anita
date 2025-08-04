from .input_reflection import reflect_input
from .evaluation_engine import run_introspection_evaluation
from .meta_response import generate_meta_commentary
from .self_state import update_identity_state, get_self_state
from .motivation_system import get_motivation_state, adjust_motivation
from .evolution_memo import generate_evolution_summary
from ..utils.trait_inference import infer_traits  # new module
from ..utils.motivation_engine import calculate_motivation_deltas  # new module
from ..utils.contextual_notes import generate_contextual_summary  # new module
from ..memory.memory_bridge import add_reflection_to_timeline  # new module
import json
import os
from datetime import datetime

def run_introspection_cycle(user_input, system_state):
    now = datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    reflection = reflect_input(user_input, system_state)
    reflection_id = now.strftime("reflection_%Y%m%d%H%M%S")


    evaluation_bundle = run_introspection_evaluation(reflection, reflection_id)
    evaluation = evaluation_bundle["evaluation"]
    growth_deltas = evaluation_bundle["growth_deltas"]

    commentary = generate_meta_commentary(evaluation)
    update_identity_state(commentary)
    adjust_motivation(commentary)

    # Dynamic additions
    traits_activated = infer_traits(reflection, evaluation)
    motivation_deltas = calculate_motivation_deltas(evaluation)
    contextual_notes = generate_contextual_summary(reflection, evaluation)

    identity_state = get_self_state()
    motivation_state = get_motivation_state()
    emotional_tag = identity_state.get("emotional_state", "Unknown")

    identity_anchor_shift = (
        identity_state.get("identity_anchor")
        if identity_state.get("identity_anchor") != "Introspective Prototype"
        else None
    )

    # Memory timeline injection
    add_reflection_to_timeline({
        "timestamp": timestamp,
        "trigger": user_input,
        "traits": traits_activated,
        "summary": commentary,
        "emotional_tag": emotional_tag,
        "semantic_depth": evaluation.get("semantic_depth", {}).get("depth", "unknown")
    })
    from ..memory.long_term_memory import append_to_long_term_memory

    append_to_long_term_memory({
    "timestamp": timestamp,
    "summary": commentary,
    "traits": traits_activated,
    "semantic_depth": evaluation["semantic_depth"]["depth"],
    "emotional_tag": emotional_tag
})

    introspection_data = {
        "timestamp": timestamp,
        "trigger": user_input,
        "reflection": reflection,
        "evaluation": evaluation,
        "growth_deltas": growth_deltas,
        "meta_response": commentary,
        "traits_activated": traits_activated,
        "identity_anchor_shift": identity_anchor_shift,
        "motivation_deltas": motivation_deltas,
        "emotional_tag": emotional_tag,
        "contextual_notes": contextual_notes
    }

    log_introspection_cycle(introspection_data)
    evolution_memo = generate_evolution_summary()
    print("\n=== Evolution Memo ===")
    print(evolution_memo)

    return commentary

def log_introspection_cycle(data):
    log_dir = r"C:\Users\Mr.Popo\Anita\anita-core\logs"
    os.makedirs(log_dir, exist_ok=True)

    filename = f"introspection_{data['timestamp'].replace(':', '-')}.json"
    filepath = os.path.join(log_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Introspection log saved to {filepath}")

# Heartbeat Metadata Injection
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_coordinator",
    version="1.1.0",
    description="Coordinates the introspection cycle with dynamic trait/motivation inference and memory updates.",
    category="core_modules"
)