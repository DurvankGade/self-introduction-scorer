# This file contains the hardcoded, structured representation of the scoring rubric.
# This approach is chosen for stability and to avoid brittle CSV parsing.

scoring_guide_data = {
    "Content & Structure": {
        "weight": 40,
        "metrics": {
            "Salutation Level": {
                "max_score": 5,
                "rules": [
                    {"type": "keyword", "keywords": ["i am excited to introduce", "feeling great"], "score": 5, "level": "Excellent"},
                    {"type": "keyword", "keywords": ["good morning", "good afternoon", "good evening", "good day", "hello everyone"], "score": 4, "level": "Good"},
                    {"type": "keyword", "keywords": ["hi", "hello"], "score": 2, "level": "Normal"}
                ]
            },
            "Key word Presence": {
                "max_score": 30, # 20 for must-have, 10 for good-to-have
                "rules": {
                    "must_have": {
                        "list": ["name", "age", "school", "class", "family", "hobbies", "interest", "free time", "cricket"],
                        "score_per_keyword": 4
                    },
                    "good_to_have": {
                        "list": ["about family", "origin", "location", "ambition", "goal", "dream", "interesting thing", "fun fact", "unique", "strengths", "achievements", "science"],
                        "score_per_keyword": 2
                    }
                }
            },
            "Flow": {
                "max_score": 5
            }
        }
    },
    "Speech Rate": {
        "weight": 10,
        "metrics": {
            "Words Per Minute": {
                "max_score": 10,
                "rules": [
                    {"range": (111, 140), "score": 10, "label": "Ideal"},
                    {"range": (141, 160), "score": 6, "label": "Fast"},
                    {"range": (81, 110), "score": 6, "label": "Slow"},
                    {"range": (161, 9999), "score": 2, "label": "Too Fast"},
                    {"range": (0, 80), "score": 2, "label": "Too Slow"}
                ]
            }
        }
    },
    "Language & Grammar": {
        "weight": 20,
        "metrics": {
            "Grammar": {
                "max_score": 10
            },
            "Vocabulary Richness": {
                "max_score": 10,
                "rules": [
                    {"range": (0.9, 1.0), "score": 10},
                    {"range": (0.7, 0.89), "score": 8},
                    {"range": (0.5, 0.69), "score": 6},
                    {"range": (0.3, 0.49), "score": 4},
                    {"range": (0.0, 0.29), "score": 2}
                ]
            }
        }
    },
    "Clarity": {
        "weight": 15,
        "metrics": {
            "Filler Word Rate": {
                "max_score": 15,
                "filler_words": ["um", "uh", "like", "you know", "so", "actually", "basically", "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"],
                "rules": [
                    {"range": (0, 3), "score": 15},
                    {"range": (4, 6), "score": 12},
                    {"range": (7, 9), "score": 9},
                    {"range": (10, 12), "score": 6},
                    {"range": (13, 9999), "score": 3}
                ]
            }
        }
    },
    "Engagement": {
        "weight": 15,
        "metrics": {
            "Sentiment": {
                "max_score": 15,
                "rules": [
                    {"range": (0.9, 1.0), "score": 15},
                    {"range": (0.7, 0.89), "score": 12},
                    {"range": (0.5, 0.69), "score": 9},
                    {"range": (0.3, 0.49), "score": 6},
                    {"range": (0.0, 0.29), "score": 3}
                ]
            }
        }
    }
}