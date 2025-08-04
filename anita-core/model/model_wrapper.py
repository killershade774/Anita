from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import datetime
from ..utils.formatter import build_prompt, post_filter_response
from ..utils.sanity_check import validate_response
from ..utils.heartbeat import update_module_status
from ..memory.memory_logger import write_to_memory, format_entry, episodic_hook

def log_violation(user_input: str, raw_output: str, reason: str = "unknown"):
    """Writes flagged model outputs to violations.log with metadata."""
    timestamp = datetime.datetime.now().isoformat()
    log_entry = (
        f"\n[{timestamp}] Triggered Filter: {reason}\n"
        f"User Input: {user_input}\n"
        f"Model Output:\n{raw_output.strip()}\n{'-'*60}\n"
    )
    with open("violations.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

class TinyLlamaChat:
    def __init__(self, model_name="Qwen/Qwen1.5-1.8B-Chat"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16
        )
        self.model.eval()

    def generate_response(self, prompt, user_input=None, previous_turns=None, max_tokens=400, retry_tokens=800):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.8,
                top_p=0.95,
                do_sample=True
            )
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        misaligned = False
        if user_input:
            misaligned = not validate_response(user_input, decoded)

        truncation = not decoded.strip().endswith((".", "!", "?", "\"", "'"))
        if (truncation or misaligned) and user_input:
            reason = "truncation and misalignment" if truncation and misaligned else ("truncation" if truncation else "misalignment")
            log_violation(user_input, decoded, reason=reason)
            print(f"⚠️ Response may be {reason}. Retrying...")

            retry_prompt = build_prompt(user_input, previous_turns)
            retry_inputs = self.tokenizer(retry_prompt, return_tensors="pt")
            with torch.no_grad():
                retry_outputs = self.model.generate(
                    **retry_inputs,
                    max_new_tokens=retry_tokens,
                    pad_token_id=self.tokenizer.eos_token_id,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True
                )
            decoded = self.tokenizer.decode(retry_outputs[0], skip_special_tokens=True)

        filtered_output = post_filter_response(decoded)

        # Inject memory logging hook
        if user_input and filtered_output.strip():
            entry = format_entry(user_input, filtered_output)
    
        try:
            signals = episodic_hook(user_input, filtered_output)
            entry["signals"] = signals
        except Exception as err:
            print(f"⚠️ Signal generation failed: {err}")
    
        write_to_memory(entry)

        return filtered_output


update_module_status(
    module_name="model_wrapper",
    version="1.0.0",
    description="Wrapper for Qwen model with response validation and retry logic.",
    category="core_modules"
)