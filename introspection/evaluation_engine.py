from datetime import datetime
from .meta_response import generate_meta_commentary  # Stub this function if not yet defined
from .evaluate_consistency import evaluate_consistency
from .evaluation_history import log_evaluation, compare_to_last
from .evolution_memo import trigger_evolution_memo  # Stub this function if not yet defined
import json

def run_introspection_evaluation(reflection_text: str, reflection_id: str, metadata: dict = None) -> dict:
    """
    Runs a structured introspection evaluation, logging results, comparing to previous reflection,
    and optionally triggering memos based on cognitive deltas or emotional variability.
    """

    # Step 1: Run full consistency evaluation
    eval_result = evaluate_consistency(reflection_text)

    # Add timestamp and metadata
    eval_result["timestamp"] = datetime.utcnow().isoformat()
    eval_result["reflection_id"] = reflection_id

    if metadata:
        eval_result["source"] = metadata.get("source", "unspecified")
        eval_result["sentiment"] = metadata.get("sentiment")
        eval_result["polarity"] = metadata.get("polarity")
        eval_result["persona"] = metadata.get("persona")

    # Step 2: Save to history
    log_evaluation(reflection_id, eval_result)

    # Step 3: Compare to previous evaluation
    growth_deltas = compare_to_last(eval_result)

    # Step 4: Trigger evolution memo if a notable change is detected
    if growth_deltas.get("major_shift") or (
        eval_result.get("sentiment") in ["negative", "positive"] and abs(eval_result.get("polarity", 0)) > 0.5
    ):
        trigger_evolution_memo(reflection_id, eval_result)

    # Step 5: Generate meta-commentary
    meta_thought = generate_meta_commentary(
        evaluation=eval_result,
        context=eval_result.get("source"),
        sentiment=eval_result.get("sentiment")
    )

    # Step 6: Return full introspection bundle
    return {
        "evaluation": eval_result,
        "growth_deltas": growth_deltas,
        "meta_commentary": meta_thought,
        "milestone_triggered": growth_deltas.get("major_shift", False)
    }

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_evaluation_engine",
    version="1.0.0",
    description="Runs structured introspection evaluations, logs results, compares to history, and generates meta-commentary.",
    category="core_modules"
)