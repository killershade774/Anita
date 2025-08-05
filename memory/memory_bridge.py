import os
import json

MEMORY_DIR = r"C:\Users\Mr.Popo\Anita\anita-core\memory\memory_snapshots"

def add_reflection_to_timeline(reflection_entry):
    """
    Adds a reflection summary to Anita's persistent timeline memory.
    :param reflection_entry: dict with keys like timestamp, trigger, traits, summary, emotional_tag, semantic_depth
    """
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    timestamp = reflection_entry.get("timestamp", "unknown").replace(":", "-")
    filename = f"memory_{timestamp}.json"
    filepath = os.path.join(MEMORY_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(reflection_entry, f, indent=2)
    
    print(f"🧠 Memory snapshot added: {filepath}")

def load_timeline_history(limit=None):
    """
    Loads past reflection snapshots, optionally limited to most recent N entries.
    :param limit: int, optional limit on entries returned
    :return: list of reflection dictionaries sorted by timestamp descending
    """
    if not os.path.exists(MEMORY_DIR):
        return []

    files = sorted(os.listdir(MEMORY_DIR), reverse=True)
    entries = []
    
    for fname in files[:limit] if limit else files:
        with open(os.path.join(MEMORY_DIR, fname), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                entries.append(data)
            except:
                continue
    
    return entries
from ..memory.memory_logger import write_to_memory, format_entry  

def add_reflection_to_timeline(reflection_entry):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    timestamp = reflection_entry.get("timestamp", "unknown").replace(":", "-")
    filename = f"memory_{timestamp}.json"
    filepath = os.path.join(MEMORY_DIR, filename)

    # Write JSON snapshot
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(reflection_entry, f, indent=2)

    print(f"🧠 Memory snapshot added: {filepath}")

    # Write to journal (optional)
    user_text = reflection_entry.get("trigger", "")
    anita_text = reflection_entry.get("summary", "")
   

    journal_entry = format_entry(user_text, anita_text)
    write_to_memory(journal_entry)
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="memory_bridge",
    version="1.0.0",
    description="Bridges short-term and long-term memory, managing reflection timeline snapshots.",
    category="core_modules"
)