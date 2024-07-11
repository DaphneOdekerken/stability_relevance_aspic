import time
import unittest
from statistics import mean

from src.algorithms.approximation_algorithm.stability_labeler import \
    StabilityLabeler
from src.algorithms.asp_algorithms.stability_algorithms import \
    GroundedStabilitySolver
from src.generators.iat_generator import \
    generate_single_layered
from src.import_export.iat_to_lp_writer import write_to_lp_file


class TestLayeredGenerated(unittest.TestCase):
    def test_layered(self):
        agreed = 0
        subset = 0
        total = 100

        labeler_times = []
        asp_times = []
        asp_with_preferences_times = []

        for i in range(total):
            print(i)
            iat, topic_candidates = generate_single_layered(500)
            iat_path = 'temp.lp'
            write_to_lp_file(iat, iat_path)

            start_time = time.time()
            labeler = StabilityLabeler()
            labeler_result = labeler.solve_stability(iat_path)
            end_time = time.time()
            labeler_time = end_time - start_time
            print(labeler_result)
            labeler_times.append(labeler_time)
            print('%.2f' % labeler_time)

            start_time = time.time()
            asp_algorithm = GroundedStabilitySolver()
            asp_result = asp_algorithm.solve_stability(iat_path)
            end_time = time.time()
            asp_time = end_time - start_time
            print(asp_result)
            asp_times.append(asp_time)
            print('%.2f' % asp_time)

            start_time = time.time()
            asp_algorithm = GroundedStabilitySolver()
            asp_pref_result = asp_algorithm.solve_stability(
                iat_path, with_preferences=True)
            end_time = time.time()
            asp_pref_time = end_time - start_time
            print(asp_pref_result)
            asp_with_preferences_times.append(asp_pref_time)
            print('%.2f' % asp_pref_time)

            self.assertTrue(labeler_result.is_subset_of(asp_result))
            self.assertTrue(asp_result == asp_pref_result)

            if labeler_result == asp_result:
                agreed += 1
                print('They agree.')
            elif labeler_result.is_subset_of(asp_result):
                print('Approximation found a subset of stable items.')
                subset += 1

        print(f'Agreement in {agreed} out of {total} generated iats.')
        print(f'Sound approximation in {subset} out of {total} generated '
              f'iats.')
        print(f'Neither in {total - agreed - subset} out of {total}.')
        print(f'Average labeler time: {mean(labeler_times)} seconds.')
        print(f'Average ASP time: {mean(asp_times)} seconds.')
        print(f'Average ASP time with preferences:'
              f' {mean(asp_with_preferences_times)} seconds.')
