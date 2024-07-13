import pathlib
import random

from src.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory
from src.experiments.run_experiments import RESULTS_PATH, run_stability_experiments, run_relevance_experiments
from src.generators.iat_generator import \
    generate_single_layered, generate_single_random
from src.import_export.iat_from_lp_reader import read_from_lp_file
from src.import_export.iat_to_lp_writer import write_to_lp_file


SMALL_NR_OF_LITERALS = [50, 60, 70, 80, 90, 100, 110, 120]
LARGE_NR_OF_LITERALS = [50, 100, 150, 200, 250, 500, 1000]
NR_OF_INSTANCES = 100
DATASET_PATH = pathlib.Path(__file__).parent.parent.parent / 'dataset'


def create_folders_if_necessary():
    for folder in ['police', 'layered_small', 'layered_large',
                   'random_small', 'random_large']:
        folder_path = DATASET_PATH / folder
        folder_path.mkdir(exist_ok=True)


def generate_police_dataset():
    # Read LP file without knowledge.
    police_example_path = str(
        DATASET_PATH / 'examples' / 'anonymised_police_iat.lp')
    iat = read_from_lp_file(police_example_path)

    for generated_index in range(NR_OF_INSTANCES):
        axioms = []
        axiom_candidates = iat.queryables.copy()

        # Add 7 axioms, one by one.
        for _ in range(7):
            new_axiom = random.choice(axiom_candidates)
            axioms.append(new_axiom)
            axiom_candidates.remove(new_axiom)
            for new_axiom_contrary in new_axiom.contraries_and_contradictories:
                if new_axiom_contrary in axiom_candidates:
                    axiom_candidates.remove(new_axiom_contrary)

        # Export
        iat_with_axioms = \
            IncompleteArgumentationTheory(
                argumentation_system=iat.argumentation_system,
                queryables=iat.queryables,
                knowledge_base_axioms=axioms,
                knowledge_base_ordinary_premises=[])
        write_path = str(
            pathlib.Path(__file__).parent.parent.parent / 'dataset' /
            'police' / ('police_60lit_' + str(generated_index) + '.lp'))
        fraud_topic = iat.argumentation_system.language['fraudarticle326']
        write_to_lp_file(iat_with_axioms, write_path, [fraud_topic])


def generate_layered_dataset(small=True):
    if small:
        nr_of_literals_list = SMALL_NR_OF_LITERALS
        folder_name = 'layered_small'
    else:
        nr_of_literals_list = LARGE_NR_OF_LITERALS
        folder_name = 'layered_large'

    for nr_of_literals in nr_of_literals_list:
        for index in range(NR_OF_INSTANCES):
            iat, topic_literal = generate_single_layered(nr_of_literals)
            filename = 'layered_no_pref_' + str(nr_of_literals) + 'lit_' + str(
                index) + '.lp'
            write_path = str(
                pathlib.Path(__file__).parent.parent.parent / 'dataset' /
                folder_name / filename)
            write_to_lp_file(iat, write_path, [topic_literal])


def generate_random_dataset(small=True):
    if small:
        nr_of_literals_list = SMALL_NR_OF_LITERALS
        folder_name = 'random_small'
    else:
        nr_of_literals_list = LARGE_NR_OF_LITERALS
        folder_name = 'random_large'

    for nr_of_literals in nr_of_literals_list:
        for index in range(NR_OF_INSTANCES):
            iat, topic_literal = generate_single_random(nr_of_literals)
            filename = 'random_no_pref_' + str(nr_of_literals) + 'lit_' + str(
                index) + '.lp'
            write_path = str(
                pathlib.Path(__file__).parent.parent.parent / 'dataset' /
                folder_name / filename)
            write_to_lp_file(iat, write_path, [topic_literal])


if __name__ == '__main__':
    create_folders_if_necessary()

    generate_police_dataset()
    print('Done with police')
    generate_layered_dataset(True)
    print('Done with layered small')
    generate_layered_dataset(False)
    print('Done with layered large')
    generate_random_dataset(True)
    print('Done with random small')
    generate_random_dataset(False)
    print('Done with random large')

    if not RESULTS_PATH.exists():
        RESULTS_PATH.mkdir()

    for dataset in ['police', 'layered_large', 'random_large']:
        run_stability_experiments(dataset)
        print('Done with stability experiments for ' + dataset)

    for dataset in ['police', 'layered_small', 'random_small']:
        run_relevance_experiments(dataset)
        print('Done with relevance experiments for ' + dataset)

