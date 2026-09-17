"""Explainable, weighted rule matching for livestock disease screening."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "disease_profiles.json"


@dataclass(frozen=True)
class RuleResult:
    disease: str
    animal: str
    score: float
    matched_symptoms: list[str]
    missing_key_symptoms: list[str]
    urgency: str
    next_step: str


def load_profiles(path: Path = PROFILE_PATH) -> list[dict]:
    """Load disease profiles stored separately so domain rules are easy to review."""
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_symptoms(symptoms: str | list[str]) -> set[str]:
    """Convert comma-separated input or a list to normalized symptom names."""
    if isinstance(symptoms, str):
        symptoms = symptoms.split(",")
    return {item.strip().lower().replace("-", " ") for item in symptoms if item.strip()}


def match_rules(animal: str, symptoms: str | list[str], limit: int = 3) -> list[RuleResult]:
    """Return ranked disease profiles for the selected animal and observed symptoms."""
    observed = normalize_symptoms(symptoms)
    animal = animal.strip().lower()
    results: list[RuleResult] = []

    for profile in load_profiles():
        if animal not in profile["animals"]:
            continue
        weights = profile["symptoms"]
        matched = sorted(symptom for symptom in weights if symptom in observed)
        if not matched:
            continue
        total_weight = sum(weights.values())
        matched_weight = sum(weights[symptom] for symptom in matched)
        key = profile.get("key_symptoms", [])
        missing_key = [symptom for symptom in key if symptom not in observed]
        results.append(
            RuleResult(
                disease=profile["disease"], animal=profile["animal_label"],
                score=round(100 * matched_weight / total_weight, 1),
                matched_symptoms=matched, missing_key_symptoms=missing_key,
                urgency=profile["urgency"], next_step=profile["next_step"],
            )
        )
    return sorted(results, key=lambda item: item.score, reverse=True)[:limit]


def available_symptoms(animal: str | None = None) -> list[str]:
    """List recognized symptoms, optionally limited to an animal group."""
    profiles = load_profiles()
    if animal:
        profiles = [p for p in profiles if animal.lower() in p["animals"]]
    return sorted({symptom for profile in profiles for symptom in profile["symptoms"]})
