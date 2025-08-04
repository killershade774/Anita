import os
import json

MEMORY_CACHE_PATH = r"C:\Users\Mr.Popo\Anita\anita-core\memory\short_term_cache.json"

def get_short_term_memory():
    """
    Retrieves Anita's active short-term memory state.
    """
    if not os.path.exists(MEMORY_CACHE_PATH):
        return {}

    try:
        with open(MEMORY_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Short-term memory retrieval failed: {e}")
        return {}

def update_short_term_memory(update_bundle):
    """
    Merges a new update into Anita's short-term memory state.
    :param update_bundle: dict of key-value pairs to cache
    """
    memory = get_short_term_memory()
    memory.update(update_bundle)

    with open(MEMORY_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

    print("🧠 Short-term memory updated.")

def clear_short_term_memory():
    """
    Resets Anita's short-term memory—useful for new sessions or reboots.
    """
    if os.path.exists(MEMORY_CACHE_PATH):
        try:
            os.remove(MEMORY_CACHE_PATH)
            print("🧹 Short-term memory cleared.")
        except Exception as e:
            print(f"Memory clearance failed: {e}")
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="short_term_memory",
    version="1.0.0",
    description="Manages Anita's short-term memory cache for active context retention.",
    category="core_modules"
)