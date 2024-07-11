import time
import unittest
from statistics import mean

from src.algorithms.approximation_algorithm.stability_labeler import \
    StabilityLabeler
from src.algorithms.asp_algorithms.stability_algorithms import \
    GroundedStabilitySolver
from src.generators.iat_generator import IncompleteArgumentationTheoryGenerator
from src.generators.random_as_generator import \
    RandomArgumentationSystemGenerator
from src.import_export.iat_to_lp_writer import write_to_lp_file


def instantiate_incomplete_argumentation_theory_generator(
        nr_literals, nr_rules):
    rule_antecedent_distribution = {1: int(nr_rules / 3),
                                    2: int(nr_rules / 3),
                                    3: int(nr_rules / 9),
                                    4: int(nr_rules / 9)}
    rules_left = nr_rules - sum(rule_antecedent_distribution.values())
    rule_antecedent_distribution[5] = rules_left

    literal_layer_distribution = {0: 2 * nr_literals / 3,
                                  1: nr_literals / 10,
                                  2: nr_literals / 10,
                                  3: nr_literals / 10}
    literals_left = nr_literals - sum(literal_layer_distribution.values())
    literal_layer_distribution[4] = literals_left

    random_argumentation_system_generator = \
        RandomArgumentationSystemGenerator(
            nr_literals, rule_antecedent_distribution)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys = random_argumentation_system_generator.generate()

    # Generate an incomplete argumentation theory, where only literals on the
    # first layer can be queryable.
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )


class TestRandomGenerated(unittest.TestCase):
    def test_random(self):
        generator = instantiate_incomplete_argumentation_theory_generator(
            500, 500)

        agreed = 0
        subset = 0
        total = 100

        labeler_times = []
        asp_times = []
        asp_with_preferences_times = []

        for i in range(total):
            print(i)
            iat = generator.generate()
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
