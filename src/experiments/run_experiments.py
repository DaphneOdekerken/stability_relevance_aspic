import os
import pathlib
import time

from multiprocessing import Process, Queue
from queue import Empty

from src.algorithms.approximation_algorithm.stability_labeler import \
    StabilityLabeler
from src.algorithms.asp_algorithms.relevance_algorithms import RelevanceSolver
from src.algorithms.asp_algorithms.stability_algorithms import \
    GroundedStabilitySolver

SECONDS_UNTIL_TIMEOUT = 60
DATASET_PATH = pathlib.Path(__file__).parent.parent.parent / 'dataset'
RESULTS_PATH = pathlib.Path(__file__).parent.parent.parent / 'results'


def run_single_stability_experiment_approximation(iat_path, queue):
    labeler = StabilityLabeler()
    labeler_result = labeler.solve_stability(iat_path)
    nr_stable = labeler_result.nr_stable()
    queue.put(nr_stable)


def run_single_stability_experiment_asp(iat_path, with_preferences, queue):
    asp_algorithm = GroundedStabilitySolver()
    asp_pref_result = asp_algorithm.solve_stability(
        iat_path, with_preferences=with_preferences)
    nr_stable = asp_pref_result.nr_stable()
    queue.put(nr_stable)


def run_single_relevance_experiment_asp(iat_path, with_preferences, queue):
    asp_algorithm = RelevanceSolver()
    asp_pref_result = asp_algorithm.relevance_all_incremental(
        iat_path, with_preferences, 'defended')
    nr_relevant = len(asp_pref_result)
    queue.put(nr_relevant)


def run_experiment_with_timeout(target_function, target_function_args):
    start_time = time.time()
    queue = Queue()
    args = tuple(target_function_args + [queue])
    process = Process(target=target_function, args=args)
    process.start()
    # Wait for the result with a timeout
    try:
        stability_status = queue.get(timeout=SECONDS_UNTIL_TIMEOUT)
        timed_out = 0
        end_time = time.time()
        duration_t = str(end_time - start_time).replace('.', ',')
    except Empty:
        # No result in time limit, terminate
        process.terminate()
        stability_status = ''
        duration_t = ''
        timed_out = 1
    return stability_status, duration_t, timed_out


def run_stability_experiments(dataset_name: str):
    results_csv_name = dataset_name + '_' + 'stability.csv'
    results_csv_path = RESULTS_PATH / results_csv_name
    dataset_items_path = DATASET_PATH / dataset_name
    with open(results_csv_path, 'w') as write_file_h1:
        write_file_h1.write(
            f'Literals;Index;'
            f'ApproxTime;ApproxTimeout;ApproxStatus;'
            f'ASPSimpleTime;ASPSimpleTimeout;ASPSimpleStatus;'
            f'ASPGeneralTime;ASPGeneralTimeout;ASPGeneralStatus\n')

    with os.scandir(dataset_items_path) as entries:
        for iat_file in entries:
            print(iat_file.path)

            approx_status, approx_time, approx_timeout = \
                run_experiment_with_timeout(
                    run_single_stability_experiment_approximation,
                    [iat_file.path])
            print(f'Approximation: {approx_status} | {approx_time} |'
                  f' {approx_timeout}')

            asp_si_status, asp_si_time, asp_si_timeout = \
                run_experiment_with_timeout(
                    run_single_stability_experiment_asp,
                    [iat_file.path, False])
            print(f'ASP Simple: {asp_si_status} | {asp_si_time} |'
                  f' {asp_si_timeout}')

            asp_ge_status, asp_ge_time, asp_ge_timeout = \
                run_experiment_with_timeout(
                    run_single_stability_experiment_asp,
                    [iat_file.path, True])
            print(f'ASP General: {asp_ge_status} | {asp_ge_time} |'
                  f' {asp_ge_timeout}')

            print('\n')

            iat_name_items = iat_file.name.split('_')
            nr_literals = iat_name_items[-2][:-3]
            index = iat_name_items[-1].split('.', 1)[0]

            with open(results_csv_path, 'a') as write_file:
                write_file.write(
                    f'{nr_literals};{index};'
                    f'{approx_time};{approx_timeout};{approx_status};'
                    f'{asp_si_time};{asp_si_timeout};{asp_si_status};'
                    f'{asp_ge_time};{asp_ge_timeout};{asp_ge_status}\n')


def run_relevance_experiments(dataset_name: str):
    results_csv_name = dataset_name + '_' + 'relevance.csv'
    results_csv_path = RESULTS_PATH / results_csv_name
    dataset_items_path = DATASET_PATH / dataset_name
    with open(results_csv_path, 'w') as write_file_h1:
        write_file_h1.write(
            f'Literals;Index;'
            f'ASPSimpleTime;ASPSimpleTimeout;ASPSimpleStatus;'
            f'ASPGeneralTime;ASPGeneralTimeout;ASPGeneralStatus\n')

    with os.scandir(dataset_items_path) as entries:
        for iat_file in entries:
            print(iat_file.path)

            asp_si_status, asp_si_time, asp_si_timeout = \
                run_experiment_with_timeout(
                    run_single_relevance_experiment_asp,
                    [iat_file.path, False])
            print(f'ASP Simple: {asp_si_status} | {asp_si_time} |'
                  f' {asp_si_timeout}')

            asp_ge_status, asp_ge_time, asp_ge_timeout = \
                run_experiment_with_timeout(
                    run_single_relevance_experiment_asp,
                    [iat_file.path, True])
            print(f'ASP General: {asp_ge_status} | {asp_ge_time} |'
                  f' {asp_ge_timeout}')

            print('\n')

            iat_name_items = iat_file.name.split('_')
            nr_literals = iat_name_items[-2][:-3]
            index = iat_name_items[-1].split('.', 1)[0]

            with open(results_csv_path, 'a') as write_file:
                write_file.write(
                    f'{nr_literals};{index};'
                    f'{asp_si_time};{asp_si_timeout};{asp_si_status};'
                    f'{asp_ge_time};{asp_ge_timeout};{asp_ge_status}\n')


if __name__ == '__main__':
    if not RESULTS_PATH.exists():
        RESULTS_PATH.mkdir()

    # for dataset in ['police', 'layered_large', 'random_large']:
    #     run_stability_experiments(dataset)

    for dataset in ['police', 'layered_small', 'random_small']:
        run_relevance_experiments(dataset)
