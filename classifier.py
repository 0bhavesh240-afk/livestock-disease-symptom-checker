"""Small dependency-free Multinomial Naive Bayes classifier for symptom text."""
from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAINING_PATH = ROOT / "data" / "training_cases.csv"


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def train_classifier(path: Path = TRAINING_PATH) -> dict:
    """Build a compact bag-of-words Multinomial Naive Bayes model."""
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    class_counts = Counter(row["disease"] for row in rows)
    word_counts: dict[str, Counter] = defaultdict(Counter)
    total_words = Counter()
    vocabulary: set[str] = set()
    for row in rows:
        disease = row["disease"]
        words = _tokens(f"{row['animal']} {row['symptoms']}")
        word_counts[disease].update(words)
        total_words[disease] += len(words)
        vocabulary.update(words)
    return {"class_counts": class_counts, "word_counts": word_counts,
            "total_words": total_words, "vocabulary": vocabulary, "rows": len(rows)}


def predict(animal: str, symptoms: str | list[str], limit: int = 3) -> list[tuple[str, float]]:
    """Return top disease probabilities for one symptom description."""
    if isinstance(symptoms, list):
        symptoms = " ".join(symptoms)
    model = train_classifier()
    words = _tokens(f"{animal} {symptoms}")
    vocab_size = len(model["vocabulary"])
    log_scores = {}
    for disease, count in model["class_counts"].items():
        score = math.log(count / model["rows"])
        denominator = model["total_words"][disease] + vocab_size
        for word in words:
            score += math.log((model["word_counts"][disease][word] + 1) / denominator)
        log_scores[disease] = score
    maximum = max(log_scores.values())
    unnormalized = {name: math.exp(score - maximum) for name, score in log_scores.items()}
    normalizer = sum(unnormalized.values())
    ranked = sorted(unnormalized.items(), key=lambda pair: pair[1], reverse=True)
    return [(disease, round(value / normalizer * 100, 1)) for disease, value in ranked[:limit]]
