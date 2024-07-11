import pathlib
import unittest

from src.algorithms.approximation_algorithm.stability_labeler import \
    StabilityLabeler
from src.algorithms.asp_algorithms.relevance_algorithms import RelevanceSolver
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

    def test_relevance_asp(self):
        asp_algorithm = RelevanceSolver()
        asp_pref_result = asp_algorithm.relevance_all_incremental(
            EXAMPLE_PATH, False, 'unsatisfiable')
        gt_unsatisfiable = set()
        self.assertSetEqual(asp_pref_result, gt_unsatisfiable)

        asp_algorithm = RelevanceSolver()
        asp_pref_result = asp_algorithm.relevance_all_incremental(
            EXAMPLE_PATH, False, 'defended')
        gt_defended = {'too_cheap', 'not_trusted', 'typosquatting'}
        self.assertSetEqual(asp_pref_result, gt_defended)

        asp_algorithm = RelevanceSolver()
        asp_pref_result = asp_algorithm.relevance_all_incremental(
            EXAMPLE_PATH, False, 'out')
        gt_out = {'not_too_cheap', 'not_typosquatting'}
        self.assertSetEqual(asp_pref_result, gt_out)

        asp_algorithm = RelevanceSolver()
        asp_pref_result = asp_algorithm.relevance_all_incremental(
            EXAMPLE_PATH, False, 'blocked')
        gt_blocked = {'too_cheap', 'typosquatting', 'trusted'}
        self.assertSetEqual(asp_pref_result, gt_blocked)
