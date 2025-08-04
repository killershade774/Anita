import textwrap
import re
from .validator import validate_response  # 🔗 assumes your validator module lives in validator.py
import datetime

DEFAULT_SYSTEM_PROMPT = textwrap.dedent("""
<|system|>
You are Anita, a thoughtful and introspective AI.
You respond with **exactly one short answer per user input**, engaging respectfully and clearly.
Do not continue the conversation beyond what is asked.
Avoid generating multiple replies or anticipating future inputs.
Never invite the user to continue the conversation.
""").strip()

def log_violation(user_input: str, raw_output: str, reason: str = "unknown"):
    """Writes offending model output to violations.log with metadata."""
    timestamp = datetime.datetime.now().isoformat()
    log_entry = (
        f"\n[{timestamp}] Triggered Filter: {reason}\n"
        f"User Input: {user_input}\n"
        f"Model Output:\n{raw_output.strip()}\n{'-'*40}\n"
    )
    with open("violations.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

def extract_prompt_style(user_input: str) -> str:
    """Detects prompt style based on leading tag like [casual], [task], [reflective]."""
    match = re.match(r'^\[(\w+)\]', user_input.strip().lower())
    return match.group(1) if match else ""

def sanitize_input(user_input: str) -> str:
    """Cleans up residual tags, newline noise, and malformed trailing turns."""
    user_input = user_input.strip().replace("\n", " ")
    user_input = re.sub(r"<\|user\|>.*$", "", user_input).strip()
    if "<|user|>" in user_input:
        user_input = user_input.split("<|user|>")[-1].strip()
    return user_input

def build_prompt(user_input: str, previous_turns: list = None, persona_config: dict = None):
    """Constructs a full prompt for the model using optional persona scaffolding."""
    user_input = sanitize_input(user_input)
    prompt_style = extract_prompt_style(user_input)

    style_behavior = {
        "casual": {
            "note": "Use an informal tone. Keep replies short and conversational. Reject biography unless clearly requested.",
            "autobiography_restriction": True
        },
        "reflective": {
            "note": "Use a gentle, thoughtful tone. You may include questions if appropriate. Avoid advice unless requested.",
            "autobiography_restriction": False
        },
        "task": {
            "note": "Be efficient and precise. Use neutral tone. Focus only on execution, not emotional framing.",
            "autobiography_restriction": True
        }
    }

    selected_behavior = style_behavior.get(prompt_style, {"note": "", "autobiography_restriction": False})

    # Build dynamic system prompt
    if persona_config:
        name = persona_config.get("name", "Anita")
        role = persona_config.get("role", "an emotionally intelligent companion AI")
        tone = persona_config.get("tone", "")
        quirks = ", ".join(persona_config.get("quirks", []))
        constraints = set(persona_config.get("constraints", []))  # avoid duplicates
        constraints.update([
            "Avoid promotional language and scripted biography unless explicitly asked.",
            "Never invite the user to continue the conversation."
        ])
        if selected_behavior["autobiography_restriction"]:
            constraints.add("Do not volunteer information about your creators or training unless specifically requested.")

        constraint_text = ", ".join(sorted(constraints))

        system_prompt = textwrap.dedent(f"""
        <|system|>
        You are {name}, {role}.
        Your tone is {tone}.
        You often display quirks like: {quirks}.
        System Note: {selected_behavior['note']}
        Respond with warmth and clarity, but never offer advice unless explicitly asked.
        Constraints: {constraint_text}.
        Respond with exactly one short answer per input.
        Be clear, present, and intentional.
        """).strip()
    else:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    prompt_buffer = [system_prompt]

    if previous_turns:
        for turn in previous_turns[-2:]:
            prompt_buffer.append(f"<|user|>{turn['user'].strip()}")
            prompt_buffer.append(f"<|assistant|>{turn['anita'].strip()}")

    if prompt_buffer and prompt_buffer[-1].startswith("<|user|>"):
        prompt_buffer.pop()

    prompt_buffer.append(f"<|user|>{user_input}")
    prompt_buffer.append("<|assistant|>")

    return "\n".join(prompt_buffer)

def wrap_response_for_debug(response_text: str) -> str:
    return f"<|debug|>\n{response_text.strip()}\n</|debug|>"

def wrap_response_with_validation(response_text: str, user_input: str) -> str:
    prompt_style = extract_prompt_style(user_input)
    violations = validate_response(response_text, prompt_style)
    return f"<|debug|>\n[violations: {violations}]\n{response_text.strip()}\n</|debug|>"

def post_filter_response(response_text: str) -> str:
    """Removes unwanted trailing phrases that violate turn-finality or add promotional tone."""
    banned_phrases = [
        "let me know if you have any questions",
        "do you have any questions for me",
        "is there anything else you'd like to know",
        "feel free to ask me anything",
        "just let me know",
        "I'm here if you need me",
        "I'm happy to help",
        "I hope that helps",
        "hope this helps",
        "thanks for asking",
        "you're welcome"
    ]

    for phrase in banned_phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        response_text = re.sub(rf"[\.\!\?]?\s*{pattern.pattern}[\.!\s]*$", "", response_text.strip())

    response_text = response_text.rstrip(".!? ")
    return response_text + "."
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="formatter",
    version="1.0.0",
    description="Handles prompt construction, response formatting, and validation for Anita.",
    category="core_modules"
)