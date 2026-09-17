import unittest

from src.rules import match_rules, normalize_symptoms


class RuleTests(unittest.TestCase):
    def test_normalizes_comma_separated_symptoms(self):
        self.assertEqual(normalize_symptoms(" Fever, Mouth-Sores "), {"fever", "mouth sores"})


    def test_fmd_ranks_first_for_characteristic_cattle_signs(self):
        results = match_rules("cattle", "fever, excessive salivation, mouth sores, lameness")
        self.assertEqual(results[0].disease, "Foot-and-mouth disease")
        self.assertGreater(results[0].score, 50)


    def test_unknown_symptoms_return_no_rule_matches(self):
        self.assertEqual(match_rules("cattle", "blue feathers"), [])
