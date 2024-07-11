import pathlib
import unittest

from src.algorithms.approximation_algorithm.stability_labeler import \
    StabilityLabeler
from src.algorithms.asp_algorithms.stability_algorithms import \
    GroundedStabilitySolver
from src.import_export.iat_from_lp_reader import read_from_lp_file

EXAMPLE_PATH = str(pathlib.Path(__file__).parent.parent.parent / 'dataset' /
                   'examples' / 'police_small.lp')


class TestPoliceExample(unittest.TestCase):
    def test_stability_label(self):
        iat = read_from_lp_file(EXAMPLE_PATH)
        labeler = StabilityLabeler()
        labels = labeler.solve_stability(iat)

        self.assertIn('not_similar_url', labels.stable_unsatisfiable)
        self.assertIn('similar_url', labels.stable_defended)
        self.assertSetEqual(labels.stable_out, set())
        self.assertSetEqual(labels.stable_blocked, set())

    def test_stability_asp(self):
        iat = read_from_lp_file(EXAMPLE_PATH)
        labeler = GroundedStabilitySolver()
        labels = labeler.solve_stability(iat)

        self.assertIn('not_similar_url', labels.stable_unsatisfiable)
        self.assertIn('similar_url', labels.stable_defended)
        self.assertSetEqual(labels.stable_out, set())
        self.assertSetEqual(labels.stable_blocked, set())
