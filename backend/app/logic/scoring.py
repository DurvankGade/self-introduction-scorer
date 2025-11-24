import re
from .scoring_config import scoring_guide_data
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Optional

# Load NLP tools once at startup
lang_tool = language_tool_python.LanguageTool('en-US')
sentiment_analyzer = SentimentIntensityAnalyzer()


# Helper Function


def get_words(text: str) -> list:
    """Return a lowercase word list stripped of punctuation."""
    return re.findall(r'\b\w+\b', text.lower())



# Scoring Functions


def score_content_structure(transcript: str, config: dict):
    """Scores Content & Structure using keyword presence."""
    text = transcript.lower()
    rules = config['metrics']['Key word Presence']['rules']

    must_have_found = sum(1 for kw in rules['must_have']['list'] if kw in text)
    good_to_have_found = sum(1 for kw in rules['good_to_have']['list'] if kw in text)

    score = (
        must_have_found * rules['must_have']['score_per_keyword'] +
        good_to_have_found * rules['good_to_have']['score_per_keyword']
    )

    feedback = (
        f"Found {must_have_found} must-have keywords and "
        f"{good_to_have_found} good-to-have keywords."
    )

    return score, feedback


def score_speech_rate(word_count: int, duration_sec: int, config: dict):
    """Scores Words Per Minute."""
    if not duration_sec or duration_sec == 0:
        return 0, "Duration missing. Cannot calculate speech rate."

    wpm = (word_count / duration_sec) * 60

    for rule in config['metrics']['Words Per Minute']['rules']:
        if rule['range'][0] <= wpm <= rule['range'][1]:
            return rule['score'], f"WPM is {int(wpm)} ({rule['label']})."

    return 0, f"WPM is {int(wpm)}, outside the scoring range."


def score_language_grammar(transcript: str, words: list, config: dict):
    """Scores grammar and vocabulary richness."""
    # Grammar score
    matches = lang_tool.check(transcript)
    errors_per_100 = (len(matches) / len(words)) * 100 if words else 0
    grammar_score = (1 - min(errors_per_100 / 10, 1)) * 10

    # Vocabulary score
    ttr = len(set(words)) / len(words) if words else 0
    vocab_score = 0
    for rule in config['metrics']['Vocabulary Richness']['rules']:
        if rule['range'][0] <= ttr <= rule['range'][1]:
            vocab_score = rule['score']
            break

    total_score = grammar_score + vocab_score
    feedback = (
        f"{len(matches)} grammar errors detected. "
        f"Vocabulary richness (TTR) is {ttr:.2f}."
    )

    return total_score, feedback


def score_clarity(words: list, config: dict):
    """Scores clarity based on filler word usage."""
    filler_words = config['metrics']['Filler Word Rate']['filler_words']
    filler_count = sum(1 for w in words if w in filler_words)
    filler_rate = (filler_count / len(words)) * 100 if words else 0

    for rule in config['metrics']['Filler Word Rate']['rules']:
        if rule['range'][0] <= filler_rate <= rule['range'][1]:
            return rule['score'], f"{filler_count} filler words ({filler_rate:.1f}%)."

    return 0, f"Filler rate is {filler_rate:.1f}%."


def score_engagement(transcript: str, config: dict):
    """Scores engagement using sentiment positivity."""
    sentiment = sentiment_analyzer.polarity_scores(transcript)
    pos = sentiment['pos']

    for rule in config['metrics']['Sentiment']['rules']:
        if rule['range'][0] <= pos <= rule['range'][1]:
            return rule['score'], f"Positivity score is {pos:.2f}."

    return 0, f"Positivity score is {pos:.2f}."



# Main Orchestrator


def calculate_scores(transcript: str, duration_sec: Optional[int]):
    """Runs all scoring modules and computes weighted score."""
    words = get_words(transcript)
    word_count = len(words)

    results = {}

    cs_score, cs_fb = score_content_structure(transcript, scoring_guide_data["Content & Structure"])
    results["Content & Structure"] = {"score": cs_score, "feedback": cs_fb}

    sr_score, sr_fb = score_speech_rate(word_count, duration_sec, scoring_guide_data["Speech Rate"])
    results["Speech Rate"] = {"score": sr_score, "feedback": sr_fb}

    lg_score, lg_fb = score_language_grammar(transcript, words, scoring_guide_data["Language & Grammar"])
    results["Language & Grammar"] = {"score": lg_score, "feedback": lg_fb}

    cl_score, cl_fb = score_clarity(words, scoring_guide_data["Clarity"])
    results["Clarity"] = {"score": cl_score, "feedback": cl_fb}

    en_score, en_fb = score_engagement(transcript, scoring_guide_data["Engagement"])
    results["Engagement"] = {"score": en_score, "feedback": en_fb}

    # Weighted scoring
    overall = 0
    for crit, data in results.items():
        weight = scoring_guide_data[crit]['weight']
        max_score = sum(m['max_score'] for m in scoring_guide_data[crit]['metrics'].values())
        if max_score > 0:
            normalized = data['score'] / max_score
            overall += normalized * weight

    return results, overall, word_count
