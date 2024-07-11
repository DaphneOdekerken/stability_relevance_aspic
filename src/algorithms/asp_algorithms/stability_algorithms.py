import clingo
import pathlib

from src.algorithms.stability_result import StabilityResult

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class GroundedStabilitySolver:
    def __init__(self):
        self.last_model = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def solve_stability(self, iat_file, with_preferences: bool = False):
        self.last_model = None

        control = clingo.Control(arguments=['--enum-mode=cautious'])
        control.load(str(iat_file))
        control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'derivable.dl'))
        if with_preferences:
            control.load(str(PATH_TO_ENCODINGS /
                             'grounded_stability_with_preferences.dl'))
        else:
            control.load(str(PATH_TO_ENCODINGS / 'grounded_stability.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'filter_status.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)

        stability_result = StabilityResult()
        if self.last_model:
            for stable_literals in self.last_model:
                literal_name = stable_literals.arguments[0].name
                status = stable_literals.name
                stability_result.add_to_result(literal_name, status)

        return stability_result


if __name__ == '__main__':
    example = pathlib.Path(__file__).parent.parent.parent.parent / 'dataset' \
              / 'examples' / 'small.lp'

    print('\nWith preferences')
    solver = GroundedStabilitySolver()
    result = solver.solve_stability(example, with_preferences=True)
    print(result)

    print('\nWithout preferences')
    solver = GroundedStabilitySolver()
    result = solver.solve_stability(example, with_preferences=False)
    print(result)
