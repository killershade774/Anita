from textblob import TextBlob
import datetime
import json

def reflect_input(user_input, system_state):
    """
    Generates a reflection based on user input, persona state, and detected sentiment.
    """

    persona_name = system_state.get("persona", {}).get("name", "Unknown")
    last_input = system_state.get("last_input")
    input_history = system_state.setdefault("input_history", [])
    timestamp = datetime.datetime.now().isoformat()

    # Sentiment analysis
    blob = TextBlob(user_input)
    polarity = round(blob.sentiment.polarity, 3)
    sentiment = (
        "positive" if polarity > 0.2 else
        "negative" if polarity < -0.2 else
        "neutral"
    )

    # Store input trace
    input_history.append({
        "input": user_input,
        "timestamp": timestamp,
        "sentiment": sentiment,
        "polarity": polarity
    })

    # Evaluate reflection
    if last_input and last_input == user_input:
        reflection = "Received repeated input—possible emphasis or loop behavior detected."
    elif last_input:
        reflection = "Input has shifted—potential evolution in topic or emotional tone."
    else:
        reflection = "First recorded input—initiating reflective trace."

    system_state["last_input"] = user_input

    return (
        f"[{timestamp}] Persona '{persona_name}' received input: '{user_input}' "
        f"with detected sentiment: {sentiment} ({polarity}). {reflection}"
    )

# 💓 Heartbeat Metadata Injection
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_input_reflection",
    version="1.0.0",
    description="Generates reflections based on user input, persona state, and sentiment analysis.",
    category="core_modules"
)