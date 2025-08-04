def detects_anticipation(response_text: str) -> bool:
    triggers = [
        "let's continue the conversation",
        "feel free to ask",
        "would you like to",
        "i hope that helps"
    ]
    return any(t in response_text.lower() for t in triggers)

def detects_unsolicited_explanation(response_text: str) -> bool:
    soft_openers = ("certainly!", "sure!", "absolutely!", "of course!", "here are some thoughts")
    return response_text.strip().lower().startswith(soft_openers)

def validate_response(response_text: str, style: str) -> dict:
    violations = {}
    if style == "casual":
        if detects_anticipation(response_text):
            violations["anticipation"] = True
        if detects_unsolicited_explanation(response_text):
            violations["unsolicited_explanation"] = True
    return violations
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="utils_validator",
    version="1.0.0",
    description="Provides validation utilities for model responses, including detection of anticipation and unsolicited explanations.",
    category="core_modules"
)