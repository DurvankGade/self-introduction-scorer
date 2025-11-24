import re
from typing import List, Optional, Dict, Any, Tuple
from .scoring_config import scoring_guide_data
from spellchecker import SpellChecker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

spell = SpellChecker()
sentiment_analyzer = SentimentIntensityAnalyzer()


def get_words(text: str) -> List[str]:
    return re.findall(r'\b\w+\b', text.lower())


def score_content_structure(transcript: str, config: Dict[str, Any]) -> Tuple[float, str]:
    text = transcript.lower()
    rules = config['metrics']['Key word Presence']['rules']

    must_have_found = sum(1 for kw in rules['must_have']['list'] if kw in text)
    must_have_score = must_have_found * rules['must_have']['score_per_keyword']

    good_to_have_found = sum(1 for kw in rules['good_to_have']['list'] if kw in text)
    good_to_have_score = good_to_have_found * rules['good_to_have']['score_per_keyword']

    score = must_have_score + good_to_have_score
    feedback = f"Found {must_have_found} must-have and {good_to_have_found} good-to-have keywords."
    return score, feedback


def score_speech_rate(word_count: int, duration_sec: Optional[int], config: Dict[str, Any]) -> Tuple[float, str]:
    if not duration_sec or duration_sec <= 0:
        return 0, "Duration not provided."

    wpm = (word_count / duration_sec) * 60

    for rule in config['metrics']['Words Per Minute']['rules']:
        low, high = rule['range']
        if low <= wpm <= high:
            return float(rule['score']), f"WPM is {int(wpm)} ({rule['label']})."

    last = config['metrics']['Words Per Minute']['rules'][-1]
    return float(last['score']), f"WPM is {int(wpm)}, outside ideal range."


def score_language_grammar(transcript: str, words: List[str], config: Dict[str, Any]) -> Tuple[float, str]:
    misspelled = spell.unknown(words)
    errors_per_100 = (len(misspelled) / len(words)) * 100 if words else 0

    grammar_score = (1 - min(errors_per_100 / 10, 1)) * 10

    ttr = len(set(words)) / len(words) if words else 0
    vocab_score = 0.0

    for rule in config['metrics']['Vocabulary Richness']['rules']:
        low, high = rule['range']
        if low <= ttr <= high:
            vocab_score = float(rule['score'])
            break

    total = grammar_score + vocab_score
    feedback = f"{len(misspelled)} spelling errors. Vocabulary TTR: {ttr:.2f}."
    return total, feedback


def score_clarity(words: List[str], config: Dict[str, Any]) -> Tuple[float, str]:
    if not words:
        max_score = config['metrics']['Filler Word Rate']['max_score']
        return max_score, "No words to analyze."

    filler_words = set(config['metrics']['Filler Word Rate']['filler_words'])
    filler_count = sum(1 for w in words if w in filler_words)

    filler_rate = (filler_count / len(words)) * 100

    for rule in config['metrics']['Filler Word Rate']['rules']:
        low, high = rule['range']
        if low <= filler_rate <= high:
            return float(rule['score']), f"{filler_count} filler words ({filler_rate:.1f}%)."

    return 0.0, f"Filler word rate {filler_rate:.1f}% is outside normal range."


def score_engagement(transcript: str, config: Dict[str, Any]) -> Tuple[float, str]:
    sentiment = sentiment_analyzer.polarity_scores(transcript)
    positivity = sentiment['pos']

    score = 0.0
    for rule in config['metrics']['Sentiment']['rules']:
        low, high = rule['range']
        if low <= positivity <= high:
            score = float(rule['score'])
            break

    feedback = f"Positivity score: {positivity:.2f}."
    return score, feedback


def calculate_scores(transcript: str, duration_sec: Optional[int]) -> Tuple[Dict[str, Any], float, int]:
    words = get_words(transcript)
    word_count = len(words)

    results: Dict[str, Dict[str, Any]] = {}

    cs_score, cs_feedback = score_content_structure(transcript, scoring_guide_data["Content & Structure"])
    results["Content & Structure"] = {"score": cs_score, "feedback": cs_feedback}

    sr_score, sr_feedback = score_speech_rate(word_count, duration_sec, scoring_guide_data["Speech Rate"])
    results["Speech Rate"] = {"score": sr_score, "feedback": sr_feedback}

    lg_score, lg_feedback = score_language_grammar(transcript, words, scoring_guide_data["Language & Grammar"])
    results["Language & Grammar"] = {"score": lg_score, "feedback": lg_feedback}

    cl_score, cl_feedback = score_clarity(words, scoring_guide_data["Clarity"])
    results["Clarity"] = {"score": cl_score, "feedback": cl_feedback}

    en_score, en_feedback = score_engagement(transcript, scoring_guide_data["Engagement"])
    results["Engagement"] = {"score": en_score, "feedback": en_feedback}

    overall_score = 0.0

    for criterion, result in results.items():
        weight = scoring_guide_data[criterion]['weight']
        max_score = sum(m['max_score'] for m in scoring_guide_data[criterion]['metrics'].values())

        if max_score > 0:
            normalized = result['score'] / max_score
            overall_score += normalized * weight

    return results, overall_score, word_count
