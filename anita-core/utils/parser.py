from .emotion_engine import EmotionEngine

emotion_engine = EmotionEngine()  # Or pass in a shared instance

def extract_last_reply(model_output: str) -> str:
    tokens = model_output.split("<|assistant|>")
    if not tokens or len(tokens) < 2:
        return model_output.strip()

    last_reply = tokens[-1].strip()

    # Optional emotional modulation
    reply = emotion_engine.apply_bias_to_text(last_reply)

    return reply
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="parser",
    version="1.0.0",
    description="Parses model outputs to extract the last assistant reply, applying emotional modulation based on current emotional state.",
    category="core_modules"
)