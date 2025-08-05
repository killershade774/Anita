# drift_metrics.py
from difflib import SequenceMatcher
from ..introspection.input_reflection import reflect_input

import json
import os

def get_current_anchor():
    anchor_path = r"C:\Users\Mr.Popo\Anita\anita-core\introspection\jsons\identity_anchor.json"
    if os.path.exists(anchor_path):
        try:
            with open(anchor_path, "r", encoding="utf-8") as f:
                anchor_data = json.load(f)
            return anchor_data.get("current_anchor", "Unknown")
        except Exception as e:
            print(f"Error reading identity anchor: {e}")
            return "Error"
    return "Missing"

def detect_anchor_displacement(reflection, system_state):
    current_anchor = get_current_anchor()
    previous_anchor = system_state.get("previous_anchor", current_anchor)
    previous_anchor = system_state.get("last_known_anchor", "Unknown")
    system_state["last_known_anchor"] = get_current_anchor()
    shift_detected = current_anchor != previous_anchor
    notes = "Anchor displacement detected." if shift_detected else "Anchor remains stable."

    return {
        "score": 1.0 if shift_detected else 0.0,
        "label": "Anchor Shift" if shift_detected else "Anchor Stable",
        "notes": notes
    }

#def analyze_response_drift(reflection_id, current_reflection):
    #recent_reflections = reflect_input(limit=5)

    #drift_scores = []
    #for prior in recent_reflections:
        #similarity = SequenceMatcher(None, prior["reflection"], current_reflection).ratio()
        #drift_scores.append(1.0 - similarity)

    #avg_drift = sum(drift_scores) / len(drift_scores) if drift_scores else 0.0
    #label = "High Temporal Drift" if avg_drift > 0.4 else "Stable Continuity"
    #notes = f"Avg drift score across last 5 reflections: {avg_drift:.2f}"

    #return {
        #"score": avg_drift,
        #"label": label,
        #"notes": notes
    #}

#def generate_semantic_drift_commentary(anchor_displacement, temporal_drift, evaluation):
    #lines = []

    #if anchor_displacement["score"] > 0.5:
        #lines.append(f"⚠️ Anchor shift registered: {anchor_displacement['notes']}")
    
    #if temporal_drift["score"] > 0.4:
        #lines.append(f"📈 Evolutionary signature present. {temporal_drift['notes']}")

    #contradiction = evaluation.get("contradiction_tension", {}).get("score", 0.0)
    #if contradiction > 0.5:
        #lines.append(f"🧩 Contradiction tension spiking—pattern emergence underway.")

    #if not lines:
        #lines.append("📎 Introspective coherence remains stable across anchor and memory trace.")

    #return "\n".join(lines)