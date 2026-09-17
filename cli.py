"""CLI entry point for the livestock disease symptom checker."""
from __future__ import annotations

import argparse

from src.classifier import predict
from src.rules import available_symptoms, match_rules


def print_results(animal: str, symptoms: str) -> None:
    rules = match_rules(animal, symptoms)
    print("\nRule-based screening\n" + "-" * 22)
    if not rules:
        print("No rule profile matched. Check symptom spelling or consult a veterinarian.")
    for index, item in enumerate(rules, 1):
        print(f"{index}. {item.disease} ({item.score:.0f}% rule match) | Urgency: {item.urgency}")
        print(f"   Matched: {', '.join(item.matched_symptoms)}")
        if item.missing_key_symptoms:
            print(f"   Not observed: {', '.join(item.missing_key_symptoms)}")
        print(f"   Next step: {item.next_step}")

    print("\nClassifier screening\n" + "-" * 22)
    for index, (disease, confidence) in enumerate(predict(animal, symptoms), 1):
        print(f"{index}. {disease} ({confidence:.1f}%)")
    print("\nEducational screening only — seek veterinary advice for diagnosis and treatment.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rule-based and ML livestock symptom checker")
    parser.add_argument("--animal", choices=["cattle", "sheep", "goat", "poultry", "swine"])
    parser.add_argument("--symptoms", help="Comma-separated signs, e.g. 'fever, lameness, mouth sores'")
    parser.add_argument("--interactive", action="store_true", help="Enter symptoms at prompts")
    parser.add_argument("--list-symptoms", action="store_true", help="Show recognized signs")
    args = parser.parse_args()

    if args.list_symptoms:
        print("Recognized symptoms:\n- " + "\n- ".join(available_symptoms(args.animal)))
        return
    if args.interactive:
        animal = input("Animal (cattle/sheep/goat/poultry/swine): ").strip().lower()
        symptoms = input("Symptoms, separated by commas: ").strip()
    else:
        animal, symptoms = args.animal, args.symptoms
    if not animal or not symptoms:
        parser.error("provide --animal and --symptoms, or use --interactive")
    print_results(animal, symptoms)


if __name__ == "__main__":
    main()
