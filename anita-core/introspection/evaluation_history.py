import json
import os
from datetime import datetime

HISTORY_FILE = "anita_evaluation_log.json"

# --- Save Evaluation ---
def log_evaluation(reflection_id: str, evaluation: dict):
    entry = {
        "reflection_id": reflection_id,
        "timestamp": datetime.utcnow().isoformat(),
        "evaluation": evaluation
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Load History ---
def get_all_evaluations():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# --- Compare Against Previous ---
def compare_to_last(evaluation: dict) -> dict:
    history = get_all_evaluations()
    if not history:
        return {"delta": "No prior evaluation to compare."}

    last_eval = history[-1]["evaluation"]
    delta_report = {}

    for key in evaluation:
        if key in last_eval and isinstance(evaluation[key], (float, str)):
            prev = last_eval[key]
            curr = evaluation[key]
            if isinstance(curr, float) and isinstance(prev, float):
                diff = round(curr - prev, 2)
                delta_report[key] = f"Δ {diff:+}"
            elif isinstance(curr, str) and curr != prev:
                delta_report[key] = f"Changed from '{prev}' to '{curr}'"

    return delta_report

from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_evaluation_history",
    version="1.0.0",
    description="Manages logging and comparison of introspection evaluations over time.",
    category="core_modules"
)