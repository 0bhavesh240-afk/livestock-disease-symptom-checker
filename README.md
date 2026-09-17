# Livestock Disease Symptom Checker

A command-line decision-support project for preliminary livestock disease screening. It combines:

- a transparent **rule-based checker** that explains symptom matches;
- a small **Multinomial Naive Bayes classifier** trained from the included curated example data;
- confidence, differential suggestions, and practical next-step guidance.

> **Important:** This is an educational project, not a veterinary diagnostic tool. A qualified veterinarian should assess sick animals, especially when there is sudden death, neurological signs, severe breathing difficulty, or a suspected reportable disease.

## Supported livestock and conditions

| Animal | Conditions included |
| --- | --- |
| Cattle | Foot-and-mouth disease, mastitis, lumpy skin disease, blackleg, brucellosis |
| Sheep / goats | Peste des petits ruminants (PPR), sheep/goat pox, enterotoxemia |
| Poultry | Newcastle disease, coccidiosis, infectious bursal disease |
| Swine | African swine fever, classical swine fever |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m src.cli --list-symptoms
python -m src.cli --animal cattle --symptoms "fever, excessive salivation, mouth sores, lameness"
```

Run interactively:

```bash
python -m src.cli --interactive
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Example result

```text
Rule-based screening
--------------------
1. Foot-and-mouth disease (77% rule match)
   Matched: fever, excessive salivation, mouth sores, lameness
   Next step: Isolate affected animals and contact a veterinarian / local animal-health authority urgently.

Classifier screening
--------------------
1. Foot-and-mouth disease (64.2%)
2. Lumpy skin disease (12.8%)
```

## Project structure

```text
data/disease_profiles.json       Rule definitions and care guidance
data/training_cases.csv          Small labeled training dataset
src/rules.py                     Explainable matching engine
src/classifier.py                Train/predict Naive Bayes model
src/cli.py                       Command-line entry point
tests/                           Automated tests
```

## Design notes

The rule score is weighted: high-specificity signs such as vesicles, skin nodules, or bloody diarrhoea count more than general signs such as fever. The classifier is deliberately small, uses only the Python standard library, and is trained locally from `data/training_cases.csv` when run, so no opaque model file is committed.

## GitHub upload

Upload the full folder (or the supplied ZIP) to a new GitHub repository. Do not upload `.venv/`, cache folders, or generated local model files; `.gitignore` already excludes them.

## Disclaimer

Disease names, symptom patterns, and response advice are simplified for academic demonstration. Disease notification requirements vary by country. Seek immediate local veterinary advice for suspected contagious or notifiable diseases.
