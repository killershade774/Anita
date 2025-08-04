import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Define model details
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_DIR = "models/tinyllama"
REVISION = "main"  # You could pin a specific commit or tag

def ensure_model_cached(force_update=False):
    if not os.path.exists(MODEL_DIR) or force_update:
        print(f"\n📡 Downloading model '{MODEL_NAME}' to '{MODEL_DIR}'...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR, revision=REVISION)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR, revision=REVISION)
        print("✅ Model downloaded.\n")
    else:
        print(f"📁 Using cached model at '{MODEL_DIR}'.")

def load_model():
    ensure_model_cached()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
    return tokenizer, model