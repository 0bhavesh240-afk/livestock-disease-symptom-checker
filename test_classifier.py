import unittest

from src.classifier import predict


class ClassifierTests(unittest.TestCase):
    def test_classifier_returns_ranked_predictions(self):
        results = predict("poultry", "green diarrhea twisted neck respiratory distress")
        self.assertEqual(results[0][0], "Newcastle disease")
        self.assertGreater(results[0][1], results[1][1])
