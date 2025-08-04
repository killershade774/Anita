from textblob import TextBlob

class SentimentParser:
    def __init__(self):
        pass

    def analyze_text(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Range: [-1, 1]
        subjectivity = blob.sentiment.subjectivity  # Range: [0, 1]

        sentiment_tag = self.map_sentiment_tag(polarity, subjectivity)
        confidence = round(abs(polarity) * (1 - subjectivity), 2)

        return {
            'tag': sentiment_tag,
            'intensity': round(abs(polarity), 2),
            'confidence': confidence,
            'raw': {'polarity': polarity, 'subjectivity': subjectivity}
        }

    def map_sentiment_tag(self, polarity, subjectivity):
        if polarity > 0.5:
            return "joyful"
        elif polarity > 0.2:
            return "hopeful"
        elif polarity > -0.2:
            return "neutral"
        elif polarity > -0.5:
            return "melancholy"
        else:
            return "distressed"
        
from ..utils.heartbeat import update_module_status

update_module_status(
    module_name="sentiment_parser",
    version="1.0.0",
    description="Analyzes text to determine sentiment, intensity, and confidence using TextBlob.",
    category="core_modules"
)