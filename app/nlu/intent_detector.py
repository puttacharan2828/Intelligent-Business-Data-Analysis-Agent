import re

INTENT_KEYWORDS = {
    "aggregation": ["total", "sum", "average", "mean", "maximum", "minimum","highest","lowest","count","how many"],
    "comparison": ["compare", "comparison", "versus", "vs", "difference"],
    "trend": ["trend", "over time", "change", "growth", "decline"],
    "distribution": ["distribution", "spread", "frequency"],
    "relationship": ["relationship", "correlation", "related", "association"],
    "summary": ["summary", "overview", "describe"]
}

def detect_intent(question):
    question = question.lower()

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", question):
                return intent

    return "unknown"
