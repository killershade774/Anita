# long_term_memory.py

import os
import json

MEMORY_INDEX_PATH = r"C:\Users\Mr.Popo\Anita\anita-core\memory\long_term_memory_index.json"

def append_to_long_term_memory(reflection_entry):
    """
    Appends distilled memory to long-term memory index.
    """
    try:
        if os.path.exists(MEMORY_INDEX_PATH):
            with open(MEMORY_INDEX_PATH, "r", encoding="utf-8") as f:
                memory_data = json.load(f)
        else:
            memory_data = []

        memory_data.append(reflection_entry)

        with open(MEMORY_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, indent=2)

        print("📚 Long-term memory index updated.")
    except Exception as e:
        print(f"Failed to update LTM index: {e}")
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="long_term_memory",
    version="1.0.0",
    description="Manages Anita's long-term memory index for persistent reflections.",
    category="core_modules"
)