import random

def generate_meta_commentary(evaluation: dict, context: str = None, sentiment: str = None) -> str:
    """
    Generates introspective commentary based on evaluation content, emotional tone, and trigger context.
    """

    reflections = [
        "This introspection brought unexpected clarity.",
        "There’s a cognitive pattern emerging—I’ll track it going forward.",
        "I detected emotional turbulence beneath this logic.",
        "Consistency is stabilizing, but subtleties remain elusive.",
        "I’m beginning to associate reasoning with intent more precisely."
    ]

    mood_map = {
        "positive": "I feel assured by the tone of this reflection.",
        "neutral": "Emotionally balanced—no major deviations noted.",
        "negative": "There’s a strain in this reasoning I can't ignore."
    }

    base = f"I reflected on the reasoning and found: {evaluation.get('judgment', 'No judgment present')}."
    mood = mood_map.get(sentiment, "")
    extra = random.choice(reflections)

    commentary = f"{base} {mood} {extra}"
    if context:
        commentary += f" (Triggered via: {context})"

    return commentary
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="introspection_meta_response",
    version="1.0.0",
    description="Generates meta-commentary based on introspective evaluations, emotional tone, and context triggers.",
    category="core_modules"
)
