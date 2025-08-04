import re

def validate_response(prompt: str, reply: str) -> bool:
    # If prompt looks like a greeting/status check
    greeting_pattern = re.compile(r"(how.*you.*doing|how.*your.*day|good morning|good afternoon|hello)", re.IGNORECASE)
    if greeting_pattern.search(prompt):
        expected_pattern = re.compile(r"(i'?m|i am|doing|been|well|not bad|thank you)", re.IGNORECASE)
        return bool(expected_pattern.search(reply))

    # Add other prompt classes here later (e.g. personal question, factual query, reflection)
    return True  # Default pass if no matching class is found
def contains_unsolicited_advice(reply: str) -> bool:
    patterns = [
        r"(take a break|practice mindfulness|self-care|remember.*you.*matter)",
        r"(gratitude|meditation|sleep|social media)"
    ]
    return any(re.search(p, reply, re.IGNORECASE) for p in patterns)
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="utils_sanity_check",
    version="1.0.0",
    description="Provides sanity checks for model responses, including validation against prompt types and detection of unsolicited advice.",
    category="core_modules"
)