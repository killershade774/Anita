import os
import time
import json
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

MEMORY_FILE = "anita_memory_log.md"
INDEX_FILE = "anita_memory_index.json"
MAX_ENTRIES = 100

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight, great semantic matching

def format_entry(user_input, model_output):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_id = hashlib.md5((user_input + model_output + timestamp).encode()).hexdigest()
    return {
        "id": entry_id,
        "timestamp": timestamp,
        "user": user_input,
        "anita": model_output
    }

def write_to_memory(entry):
    with open("anita_memory_log.md", "a", encoding="utf-8") as f:
        f.write(f"**User:** {entry['user']}\n")
        f.write(f"**Anita:** {entry['anita']}\n")
        
        # Optional signals serialization (line 41 likely refers to this spot)
        f.write(f"**Signals:** {json.dumps(entry.get('signals', {}))}\n\n")

    update_index(entry)

def load_memory_log():
    if not os.path.exists(MEMORY_FILE):
        return []
    entries = []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        raw = f.read().split("## Entry ")[1:]
        for block in raw:
            parts = block.split("**User:** ")
            timestamp = block.split("]")[0].strip(" [")
            if len(parts) == 2:
                user = parts[1].split("**Anita:**")[0].strip()
                anita = parts[1].split("**Anita:**")[1].strip()
                entries.append({"timestamp": timestamp, "user": user, "anita": anita})
    return entries

def update_index(entry):
    text_blob = f"{entry['user']} {entry['anita']}"
    embedding = model.encode(text_blob).tolist()
    
    index_data = [{
        "timestamp": entry.get("timestamp", datetime.now().isoformat()),
        "embedding": embedding,
        "text": text_blob
    }]
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f)

def retrieve_memory(query, top_k=5):
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    query_embedding = model.encode(query)
    scores = []
    for item in index_data:
        score = np.dot(query_embedding, item["embedding"]) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(item["embedding"]))
        scores.append((score, item))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in scores[:top_k]]
def episodic_hook(user_input, model_output):
    """
    Extracts vector-based signals and structural placeholders for future tagging,
    enabling episodic encoding refinement in Anita's memory system.
    """
    return {
        "intent_vector": model.encode(user_input).tolist(),
        "response_vector": model.encode(model_output).tolist(),
        "timestamp": datetime.now().isoformat(),
        "tags": []  # Placeholder for dynamic annotations like ["goal-shift", "contradiction", "emotional-tone"]
    }